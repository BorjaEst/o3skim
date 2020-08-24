"""This module offers some utils for code management"""
from contextlib import contextmanager
import os
import yaml
import netCDF4
import xarray as xr


@contextmanager
def cd(newdir):
    """Changes the directory inside a 'with' context"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def load(yaml_file):
    """Loads the .yaml file with the sources configurations"""
    with open(yaml_file, "r") as ymlfile:
        return yaml.load(ymlfile)


def create_empty_netCDF(fname):
    """Creates a new empty netCDF file"""
    root_grp = netCDF4.Dataset(fname, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    root_grp.close()


def to_netcdf(path, name, dataset):
    """Creates or appends data to named netcdf files"""
    years, dsx = zip(*dataset.groupby("time.year"))
    fnames = [path + "/" + name + "_%s.nc" % y for y in years]
    [create_empty_netCDF(fn) for fn in fnames if not os.path.isfile(fn)]
    xr.save_mfdataset(dsx, fnames, mode='a')
