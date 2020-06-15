#!/usr//bin/env python

import os
import tables
import argparse
from distutils.util import strtobool
from astropy.table import Table
from hiperta_r0_to_dl1lstchain import main as reorganize_dl1_hiperta

parser = argparse.ArgumentParser(description="Test the hipecta to lstchain dl1 file converted")

parser.add_argument('--infile', '-i',
                    type=str,
                    dest='infile',
                    help='Output of `hiperta_r1_dl1 file to test',
                    )

parser.add_argument('--outdir', '-o',
                    type=str,
                    dest='outdir',
                    help='Path where to store the dl1_reorganized_* file.',
                    default='./'
                    )

parser.add_argument('--config', '-c',
                    type=str,
                    dest='config',
                    help='Configuration file for hiperta_r1_dl1 script'
                    )

parser.add_argument('--debug_mode', '-d',
                    type=lambda x: bool(strtobool(x)),
                    dest='debug_mode',
                    help='Activate debug mode (add cleaned mask in the output hdf5). Set by default to False',
                    default=False
                    )

args = parser.parse_args()


def test_reorganize_dl1hiperta_to_dl1lstchain():
    """
    Test the re-organiser script does not change dl1_hipecta file.
    """
    # We know in advance the output names
    # gamma.h5 --> dl1_gamma.h5 (after hiperta_r1_dl1) --> dl1_reorganized_gamma.h5 (after reorganizer script).
    assert args.infile.find('dl1_') == 0
    base_filename = args.infile[4:]
    output_reorganized_filename = os.path.join(args.outdir, "dl1_reorganized_" + os.path.basename(base_filename))
    if not os.path.isfile(output_reorganized_filename):
        reorganize_dl1_hiperta(args.infile,
                               output_reorganized_filename,
                               config=args.config,
                               keep_file=True,
                               debug_mode=args.debug_mode)

    hf = tables.open_file(args.infile, mode='r')
    hf_reorg = tables.open_file(output_reorganized_filename, mode='r')

    dl1 = hf.root.dl1
    dl1_reorg = hf_reorg.root.dl1

    try:
        tel_ids = [tel['telId'][0] for tel in dl1]
    except:
        tel_ids = [i[0] + 1 for i in enumerate(dl1)]

    params_hipecta = [Table(tel.parameters.read()) for tel in dl1]
    tels_reorg = Table(dl1_reorg.event.telescope.parameters.LST_LSTCam.read())

    # Check all the events from the hipecta file have been copied correctly
    for i, tel in enumerate(tel_ids):
        assert len(params_hipecta[i]) == len(tels_reorg[tels_reorg['tel_id'] == tel]['tel_id'])

    # check log intensity
    # check wl is w / l
    # check images
