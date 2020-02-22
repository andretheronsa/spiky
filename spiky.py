#!/usr/bin/env python3

import argparse
import geopandas as gpd
from pathlib import Path
import logging
import sys
import numpy

############################################################
# Company: Kartoza                                         #
# Project: GeoPackage spike remover - interview test       #
# Author: Andre Theron (andretheronsa@gmail.com)           #
# Created: February 2020                                   #
# Requires: Python version 3.4+ for Pathlib                 #
############################################################


def cmd_line_parse():
    '''Parse command line input and returns argument object'''
    example = "example: python3 ./spiky.py polygon.gpkg"
    parser = argparse.ArgumentParser(
        description='Program that removes spikes from a GeoPackage polygon',
        formatter_class=argparse.RawTextHelpFormatter, epilog=example)
    parser.add_argument('infile',
                        type=str,
                        help="Input GeoPackage file to be de-spiked")
    args = parser.parse_args()
    return(args)


def read_gpkg(filepath: Path) -> gpd:
    '''Read a GeoPackage file.'''
    if filepath.exists:
        gpkg = gpd.read_file(filepath)
    else:
        logging.error("GeoPackage file not found")
        sys.exit(1)
    return gpkg


def test_gpkg(gpkg: gpd) -> bool:
    '''Test if GeoPackage is valid for Spike.'''
    return True


def write_gpkg(gpkg: gpd, filepath: Path) -> bool:
    '''Write a GeoPackage file.'''
    gpkg.tofile(filepath, driver="GPKG")
    return True


def calc_angles(gpkg: gpd) -> dict:
    '''Write a GeoPackage file.'''


def calc_legs(gpkg: gpd) -> dict:
    '''Write a GeoPackage file.'''


def calc_area(gpkg: gpd) -> float:
    '''Write a GeoPackage file.'''


def main():
    '''Main program'''
    logging.info("Program starting")


if __name__ == "__main__":
    main()
