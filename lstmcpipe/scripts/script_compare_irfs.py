import os
import logging
import argparse
import matplotlib.pyplot as plt
from lstmcpipe.plots.plot_irfs import plot_summary_from_file

parser = argparse.ArgumentParser(description="Produce IRFs comparative plots")

# Required arguments
parser.add_argument('--filelist', '-f',
                    type=str,
                    nargs='*',
                    dest='filelist',
                    help='List of IRF files',
                    )

parser.add_argument('--outfile', '-o', action='store', type=str,
                    dest='outfile',
                    help='Path of the outfile',
                    default='compare_irfs.png',
                    )

args = parser.parse_args()

def main(filelist, outfile):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("lstchain MC DL2 to IRF - sensitivity curves")

    log.info("Starting lstmcpipe compare irfs script")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    for file in filelist:
        log.log(f"Plotting IRFs from file {file}")
        label = os.path.basename(file)
        plot_summary_from_file(file, axes=axes, label=label)


    plt.savefig(outfile, dpi=300, bbox_inches='tight')


if __name__ == '__main__':

    main(args.filelist, args.outfile)

