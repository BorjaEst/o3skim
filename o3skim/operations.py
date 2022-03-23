"""Module in charge of implementing the o3skim operations."""
import logging

import cf_xarray as cfxr
import xarray as xr


logger = logging.getLogger("o3skim.operations")
xr.set_options(keep_attrs=True)


def run(dataset, operation):
    """Main entry point for operation call on o3skimming functions:

        :lon_mean:  Longitudinal mean across the dataset.
        :lat_mean:  Latitudinal mean across the dataset.
        :year_mean: Time coordinate averaged by year.

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :param operation: Operation name to perform.
    :type operation: str

    :return: Dataset after processing the specified operation.
    :rtype: :class:`xarray.Dataset`
    """
    if operation == "lon_mean":
        return lon_mean(dataset)
    elif operation == "lat_mean":
        return lat_mean(dataset)
    else:
        err = "Bad selected operation: {}"
        raise KeyError(err.format(operation))


def lon_mean(dataset):
    logger.debug("Calculating mean over model longitude")
    dataset = dataset.cf.mean("longitude")
    # Dirty code: cell-methods patch
    # See https://github.com/xarray-contrib/cf-xarray/discussions/314
    dataset['toz_zm'].attrs['cell_methods'] += " longitude: mean"
    return dataset


def lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    dataset = dataset.cf.mean("latitude")
    # Dirty code: cell-methods patch 
    # See https://github.com/xarray-contrib/cf-xarray/discussions/314
    dataset['toz_zm'].attrs['cell_methods'] += " latitude: mean"
    return dataset
