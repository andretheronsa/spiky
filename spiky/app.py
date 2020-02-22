#!/usr/bin/env python3

import geopandas as gpd
from pathlib import Path
import logging

############################################################
# Company: Kartoza                                         #
# Project: Geopackage spike remover - interview test       #
# Author: Andre Theron (andretheronsa@gmail.com)           #
# Created: February 2020                                   #
# Requires: Python version 3.4 for Pathlib                 #
############################################################


def read_gpkg(filepath: Path) -> gpd:
    '''Read a geopackage file.'''
    gpkg = gpd.read_file(filepath)
    return gpkg


def write_gpkg(gpkg: gpd, filepath: Path) -> bool:
    '''Write a geopackage file.'''
    gpkg.tofile(filepath, driver="GPKG")
    return True


def main():
    '''Main program logic'''
    logging.info("Program starting")


if __name__ == "__main__":
    main()
