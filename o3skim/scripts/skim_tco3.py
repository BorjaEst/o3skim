#!/usr/bin/env python3
"""
o3skim is a tool for data reduction for ozone applications.
"""
import argparse
import logging
import sys

import iris
import o3skim

# Script logger setup
logger = logging.getLogger("o3norm")

# Parser for script inputs
parser = argparse.ArgumentParser(
    prog=f"o3skim", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument(
    "-v", "--verbosity", type=str, default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Sets the logging level (default: %(default)s)")
parser.add_argument(
    "-o", "--output", type=str, default='.',
    help="Folder for output files (default: %(default)s)")
parser.add_argument(
    "paths", nargs='+', type=str, action='store',
    help="Paths to netCDF files with the data to skim")

# Available operations group
operations = parser.add_argument_group('operations')
operations.add_argument(
    "--lon_mean", action='append_const',
    dest='operations', const='lon_mean',
    help="Longitudinal mean across the dataset")
operations.add_argument(
    "--lat_mean", action='append_const',
    dest='operations', const='lat_mean',
    help="Latitudinal mean across the dataset")
operations.add_argument(
    "--year_mean", action='append_const',
    dest='operations', const='year_mean',
    help="Time average accross the year")


def main():
    args = parser.parse_args()
    run_command(**vars(args))
    sys.exit(0)  # Shell return 0 == success


def run_command(paths, operations, **options):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, options["verbosity"]),
        format="%(asctime)s %(name)-24s %(levelname)-8s %(message)s",
    )

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    logger.info("Data loading from %s", paths)
    dataset = iris.load_cube(paths, "atmosphere_mole_content_of_ozone")

    # Processing of skimming operations
    logger.info("Data skimming using %s", operations)
    skimmed = o3skim.process(dataset, operations)

    # Saving
    logger.info("Staving result into %s", options["output"])
    iris.save(skimmed, options["output"])

    # End of program
    logger.info("End of program")


if __name__ == '__main__':
    main()
