#!/usr/bin/env python

# E. Garcia, Avr '21
#
# DL2 to IRFs stage for the R0 to IRFs full MC production workflow.
#
#
# As all the previous stages, this script make use of the lstchain entry points to batch each workflow stage.
#

import os
import glob
import shutil
from lstmcpipe.io.data_management import check_and_make_dir_without_verification


def check_dl2_files(dl2_dir, pointlike, gamma_off):
    """
    Search DL2 testing files for each of the desired particles depending on the IRF configuration (point-like
    and gamma-offset).

    Parameters
    ----------
    dl2_dir: str
        General path to DL2 directory, not formatted with the particle.
    pointlike: bool
        IRF configuration parameter to indicate point-like or diffuse gammas.
    gamma_off:
        IRF configuration parameter with the gamma-offset.

    Returns
    -------
    dl2_particle_paths: dict
        Dictionary containing the path to the DL2 testing files depending on the desired IRF configuration

    """
    # Make particle loop depending on gamma point like
    particles_irfs = ['electron', 'proton']
    if pointlike:
        particles_irfs.append('gamma')
    else:
        particles_irfs.append('gamma-diffuse')

    dl2_particle_paths = {}
    for particle in particles_irfs:
        dl2_particle_paths[particle] = {}

        if particle == 'gamma':
            particle_dir_dl2 = os.path.join(dl2_dir.format(particle), f'{gamma_off}')
        else:
            particle_dir_dl2 = dl2_dir.format(particle)

        if os.path.isdir(particle_dir_dl2):
            dl2_particle_paths[particle] = \
                glob.glob(os.path.join(particle_dir_dl2,
                                       '*testing.h5')
                          )[0]
        else:
            print(f'DL2 {particle} directory cannot be found or does not exists:\n {particle_dir_dl2}')
            exit(-1)

    return dl2_particle_paths


def dl2_to_irfs(dl2_directory, config_file, log_from_dl1_dl2, irf_point_like=True, irf_gamma_offset='off0.0deg',
                source_env=None, wait_jobs_dl1dl2=None, prod_id=None):
    """
    Batches interactively the lstchain `lstchain_create_irf_files` entry point.

    Parameters
    ----------
    dl2_directory: str
        Base path to DL2 directory, (not formatted with the particle type yet).
    config_file: str
        Path to a configuration file. If none is given, a standard configuration is applied
    irf_point_like: bool
        MC prod configuration argument to create IRFs: {True: gamma, False: gamma-diffuse}.
    irf_gamma_offset: str
        MC prod configuration argument to create IRFs: off0.0deg (for ON/OFF obs) or off0.4deg (for wobble obs).
    source_env: str
        path to a .bashrc file to source (can be configurable for custom runs @ mc_r0_to_dl3 script) to activate
        a certain conda environment.
    log_from_dl1_dl2: dict
        Dictionary with dl2 output path. Files are not yet here, but path and full name are needed to batch the job.
    wait_jobs_dl1dl2: str
        Comma separated string with the job ids of previous stages (dl1_to_dl2 stage) to be passed as dependencies to
        the create_irfs_files job to be batched.
    prod_id: str
        prod_id defined within config_MC_prod.yml file

    Returns
    -------
    log_dl2_to_irfs: dict
        Dictionary-wise log containing {'job_id': 'batched_cmd'} items
    list_job_id_dl2_irfs: str
        Job-ids of the batched job to be passed to the last (MC prod check) stage of the workflow.
    """
    allowed_gamma_off = ['off0.0deg', 'off0.4deg']
    if irf_gamma_offset not in allowed_gamma_off:
        print(f'Please select a valid gamma_offset to compute the IRFS: {" or ".join(allowed_gamma_off)}')
        exit(-1)

    if irf_point_like:
        output_irfs_dir = os.path.join(dl2_directory.replace('/DL2/', '/IRF/').replace('/{}/', '/'),
                                       irf_gamma_offset)
    else:
        output_irfs_dir = os.path.join(dl2_directory.replace('/DL2/', '/IRF/').replace('/{}/', '/'),
                                       'diffuse')

    log_dl2_to_irfs = {}
    list_job_id_dl2_irfs = []

    if log_from_dl1_dl2 == {}:  # Empty dict and thus no dl2 path files
        dl2_particle_paths = check_dl2_files(
            dl2_directory,
            irf_point_like,
            irf_gamma_offset)

        # Comprehension list to find gamma or gamma-diffuse
        gamma_kind = [g for g in dl2_particle_paths.keys() if g.startswith('gamma')][0]

        gamma_file = dl2_particle_paths[gamma_kind]
        proton_file = dl2_particle_paths['proton']
        electron_file = dl2_particle_paths['electron']

        irf_kind = gamma_kind

    else:
        proton_file = log_from_dl1_dl2['proton']['dl2_test_path']
        electron_file = log_from_dl1_dl2['electron']['dl2_test_path']

        if irf_point_like and irf_gamma_offset == 'off0.0deg':
            gamma_file = log_from_dl1_dl2['gamma_off0.0deg']['dl2_test_path']
            irf_kind = irf_gamma_offset
        elif irf_point_like and irf_gamma_offset == 'off0.4deg':
            gamma_file = log_from_dl1_dl2['gamma_off0.4deg']['dl2_test_path']
            irf_kind = irf_gamma_offset
        else:
            gamma_file = log_from_dl1_dl2['gamma-diffuse']['dl2_test_path']
            irf_kind = 'diffuse'

    if irf_point_like:
        point_like = '--point-like'
    else:
        point_like = ''

    # Final outfile name with IRF kind
    if prod_id is None:
        output_filename_irf = os.path.join(output_irfs_dir, 'irf.fits.gz')
    else:
        if irf_point_like:
            output_filename_irf = os.path.join(
                output_irfs_dir,
                'irf_' + prod_id.replace('.', '') + f'_gamma_point-like_{irf_gamma_offset.replace(".", "")}.fits.gz'
            )
        else:
            output_filename_irf = os.path.join(
                output_irfs_dir,
                'irf_' + prod_id.replace('.', '') + f'_gamma_diffuse.fits.gz'
            )

    cmd = f'lstchain_create_irf_files {point_like} -g {gamma_file} -p {proton_file} -e {electron_file}' \
          f' -o {output_filename_irf}'
    if config_file is not None:
        cmd += f' --config={config_file}'

    # TODO dry-run option ?
    # if dry_run:
    #     print(cmd)

    print(f'\tOutput dir IRF {irf_kind}: {output_irfs_dir}')

    check_and_make_dir_without_verification(output_irfs_dir)

    jobe = os.path.join(output_irfs_dir, f"job_dl2_to_irfs_gamma_{irf_kind}.e")
    jobo = os.path.join(output_irfs_dir, f"job_dl2_to_irfs_gamma_{irf_kind}.o")

    batch_cmd = f'sbatch --parsable -p short --dependency=afterok:{wait_jobs_dl1dl2} -J IRF_{irf_kind}' \
                f' -e {jobe} -o {jobo} --wrap="{source_env} {cmd}"'

    job_id_dl2_irfs = os.popen(batch_cmd).read().strip('\n')

    log_dl2_to_irfs[job_id_dl2_irfs] = batch_cmd
    list_job_id_dl2_irfs.append(job_id_dl2_irfs)

    # Copy config into working dir
    if config_file is not None or config_file is not '':
        shutil.copyfile(config_file, os.path.join(output_irfs_dir, os.path.basename(config_file)))

    list_job_id_dl2_irfs = ','.join(list_job_id_dl2_irfs)

    return log_dl2_to_irfs, list_job_id_dl2_irfs
