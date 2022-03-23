#!/usr/bin/env python3
"""o3skim is a tool for data reduction for ozone applications.
"""
import argparse
import logging
import sys

import cf_xarray as cfxr
import o3skim
import xarray as xr


class StripArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.strip())


# Script logger setup
logger = logging.getLogger("skim_tco3")

# Parser for script inputs
parser = argparse.ArgumentParser(
    prog=f"o3skim", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument(
    "-v", "--verbosity", type=str, default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Sets the logging level (default: %(default)s)")
parser.add_argument(
    "-o", "--output", type=str, default='toz-skimmed.nc', action=StripArgument,
    help="Output file for skimmed data (default: %(default)s)")
parser.add_argument(
    "-n", "--variable_name", type=str, action=StripArgument,
    default='atmosphere_mole_content_of_ozone', 
    help="Variable or standard_name to skim (default: %(default)s)")
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


def main():
    args = parser.parse_args()
    run_command(**vars(args))
    sys.exit(0)  # Shell return 0 == success


def run_command(paths, operations, variable_name, **options):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, options["verbosity"]),
        format="%(asctime)s %(name)-24s %(levelname)-8s %(message)s",
    )

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    logger.info("Data loading from %s", paths)
    kwargs = dict(data_vars='minimal', concat_dim='time', combine='nested')
    dataset = xr.open_mfdataset(paths, **kwargs)

    # Extraction of variable as dataset
    logger.info("Variable %s loading", variable_name)
    ozone = dataset.cf[[variable_name]]

    # Variable name standardization
    logger.info("Renaming var %s to 'toz'/'toz_zm", variable_name)    
    if any([x in operations for x in ['lat_mean', 'lon_mean']]):
        ozone = ozone.cf.rename({variable_name: 'toz_zm'})
    else:
        ozone = ozone.cf.rename({variable_name: 'toz'})

    # Processing of skimming operations
    logger.info("Data skimming using %s", operations)
    skimmed = o3skim.process(ozone, operations)

    # Saving
    logger.info("Staving result into %s", options["output"])
    skimmed.to_netcdf(options["output"])

    # End of program
    logger.info("End of program")
    dataset.close()
    ozone.close()
    skimmed.close()



if __name__ == '__main__':
    main()
