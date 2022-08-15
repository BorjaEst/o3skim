import logging

import xarray as xr
from o3skim import config, utils

## Application logger
logger = logging.getLogger(__name__)


VARIABLE_NAME = "equivalent_thickness_at_stp_of_atmosphere_ozone_content"


def load_tco3(model_path):
    """Loads and returns a CCMI-1 NIWA DataArray model and the dataset
    attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset
    """

    # Loading of DataArray and attributes
    logger.info("Loading CCMI-1 NIWA data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Clean non cf attributes
    logger.debug(f"Removing all non CF convention attributes")
    utils.delete_non_CFConvention_attributes(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Removing all variable except '{VARIABLE_NAME}'")
    dataset = utils.drop_vars_except(dataset, VARIABLE_NAME)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{config.TCO3_VAR}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: config.TCO3_VAR})
    dataset[config.TCO3_VAR].attrs.update(
        {"standard_name": config.TCO3_STANDARD_NAME}
    )

    # Deletion of not used coordinates
    logger.debug(f"Removing unused coords from '{list(dataset.coords)}'")
    dataset = utils.drop_unused_coords(dataset)

    # Loading cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    logger.debug(f"Loading time variable '{dataset.cf['time'].name}'")
    dataset.cf["time"].load()
    if "bounds" in dataset.cf["time"].attrs:
        dataset[dataset.cf["time"].attrs["bounds"]].load()

    # Convert cftime variables to support mean operations
    logger.debug(f"Converting time variable '{dataset.cf['time'].name}'")
    attrs = dataset['time'].attrs
    dataset['time'] = dataset.indexes['time'].to_datetimeindex()
    dataset['time'].attrs = attrs

    # Return standard loaded tco3 dataset
    return dataset
