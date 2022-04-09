#!/usr//bin/env python3

import os
import logging
from pathlib import Path
from lstmcpipe.workflow_management import save_log_to_file


log = logging.getLogger(__name__)


def batch_merge_dl1(
    dict_paths,
    batch_config,
    logs,
    jobid_from_splitting,
    workflow_kind="lstchain",
):
    """
    Function to batch the onsite_mc_merge_and_copy function once the all the r0_to_dl1 jobs (batched by particle type)
    have finished.

    Batch 8 merge_and_copy_dl1 jobs ([train, test] x particle) + the move_dl1 and move_dir jobs (2 per particle).

    Parameters
    ----------
    dict_paths : dict
        Core dictionary with {stage: PATHS} information
    batch_config : dict
        Dictionary containing the (full) source_environment and the slurm_account strings to be passed
        to `merge_dl1` and `compose_batch_command_of_script` functions.
    workflow_kind : str
        Defines workflow kind (lstchain, ctapipe, hiperta)
    logs: dict
        Dictionary with logs files
    jobid_from_splitting:

    Returns
    -------
    jobids_for_train : str
         Comma-sepparated str with all the job-ids to be passed to the next
         stage of the workflow (as a slurm dependency)

    """
    log_merge = {}
    all_jobs_merge_stage = []
    debug_log = {}

    log.info("==== START {} ====".format("batch merge_and_copy_dl1_workflow"))
    # TODO Lukas: merging option will come inside the
    #  dict_paths["merge_dl1"]["merging_options"]
#    if isinstance(smart_merge, str):
#        merge_flag = "lst" in smart_merge
#    else:
#        merge_flag = smart_merge
#    log.debug("Merge flag set: {}".format(merge_flag))

    for particle in dict_paths:
        job_logs, jobid_debug = merge_dl1(
            particle["input"],
            particle["output"],
            merging_options={
                "no_image": particle.get("no_image", True),
                "smart": particle.get("smart", False),
            },
            batch_configuration=batch_config,
            wait_jobs_split=jobid_from_splitting,
            workflow_kind=workflow_kind,
        )

        log_merge.update(job_logs)
        all_jobs_merge_stage.append(jobid_debug)

    jobids_for_train = ','.join(all_jobs_merge_stage)

    save_log_to_file(log_merge, logs["log_file"], "merge_dl1")
    save_log_to_file(debug_log, logs["debug_file"], workflow_step="merge_dl1")

    log.info("==== END {} ====".format("batch merge_and_copy_dl1_workflow"))

    return jobids_for_train


def merge_dl1(
        input_dir,
        output_file,
        batch_configuration,
        wait_jobs_split="",
        merging_options={},
        workflow_kind="lstchain",
):
    """

    Parameters
    ----------
    input_dir: str
    output_file: str
    batch_configuration: dict
    wait_jobs_split: str
    merging_options: dict
    workflow_kind: str

    Returns
    -------
    log_merge: dict
    jobid_merge: dict

    """
    source_environment = batch_configuration["source_environment"]
    slurm_account = batch_configuration["slurm_account"]

    flag_no_image = merging_options["no_image"]
    flag_smart_merge = merging_options["smart"]

    log_merge = {}

    cmd = "sbatch --parsable -p short"
    if slurm_account != "":
        cmd += f" -A {slurm_account}"
    if wait_jobs_split != "":
        cmd += " --dependency=afterok:" + wait_jobs_split

    jobo = Path(output_file).parent.joinpath("merging-output.o")
    jobe = Path(output_file).parent.joinpath("merging-error.e")

    cmd += (
        f' -J merge -e {jobe} -o {jobo} --wrap="{source_environment} '
    )

    # Close " of wrap
    if workflow_kind == "lstchain":
        cmd += f'lstchain_merge_hdf5_files -d {input_dir} -o {output_file} --no-image"'

    elif workflow_kind == "hiperta":
        # HiPeRTA workflow still uses --smart flag (lstchain v0.6.3)
        cmd += (
            f"lstchain_merge_hdf5_files -d {input_dir} -o {output_file} --no-image {flag_no_image} "
            f'--smart {flag_smart_merge}"'
        )
    else:  # ctapipe case
        if flag_no_image:
            cmd += f'ctapipe-merge --input-dir {input_dir} --output {output_file} --skip-images --skip-simu-images"'
        else:
            cmd += f'ctapipe-merge --input-dir {input_dir} --output {output_file}"'

    jobid_merge = os.popen(cmd).read().strip("\n")
    log_merge.update({jobid_merge: cmd})

    log.info(f"Submitted batch job {jobid_merge}")

    return log_merge, jobid_merge