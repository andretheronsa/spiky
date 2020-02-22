#!/usr/bin/env python3

from glob import glob
import geopandas as gpd
from pathlib import Path
import logging
import sys

'''
Company: Kartoza
Project: GeoPackage spike remover - interview test
Author: Andre Theron (andretheronsa@gmail.com)
Created: February 2020
Requires: Python version 3.4+ for Pathlib
'''


def test_gpkg(gpkg: gpd) -> bool:
    '''Test if GeoPackage is valid for de-spiking.'''
    if gpkg.is_valid:
        return True
    else:
        return False


def calculate_angle(a: dict, b: dict, c: dict) -> float:

    return angle


def remove_spikes(gpkg: gpd, angle: int) -> gpd:
    '''Removes vertices with neighbouring angles exceeding input angle'''
    
    # Remember to remove first element in polygon
    return gpkg


def calc_area(gpkg: gpd) -> int:
    '''Write a GeoPackage file.'''
    area = gpkg.area
    return area


def iterate(gpkg: gpd, max_angle: int, max_area_delta: int):
    angle = 0
    new_layers = []
    for gpkg_layer in gpkg:
        while angle < max_angle:
            orig_area = calc_area(gpkg_layer)
            new_gpkg = remove_spikes(gpkg, angle)
            new_area = calc_area(new_gpkg)
            area_delta = min(orig_area, new_area) / max(orig_area, new_area)
            if area_delta > max_area_delta:
                new_layers.append(orig_area)
            else:
                angle += 1
    final_gpkg = new_layers  # Should append all layers
    return final_gpkg


def main(in_dir: str = '/home/input/',
         max_angle: int = 10,
         max_area_delta: int = 1):
    '''Main program'''
    gpkg_list = glob(in_dir + "*.gpkg")
    for gpkg_file in gpkg_list:
        gpkg_path = Path(gpkg_file)
        gpkg_gpd = gpd.read_file(gpkg_path)
        if not test_gpkg(gpkg_gpd):
            logging.error(f"{gpkg_file} not a valid GeoPackage file for Spiky")
            sys.exit(1)
        despiked_gpkg = iterate(gpkg_gpd, max_angle, max_area_delta)
        despiked_gpkg.tofile(gpkg_path.with_suffix("_despike.gpkg"),
                             driver="GPKG")


if __name__ == "__main__":
    main()
