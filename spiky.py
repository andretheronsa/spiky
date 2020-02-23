#!/usr/bin/env python3

from argparse import ArgumentParser as arparse
from glob import glob
import geopandas as gpd
from pathlib import Path
import logging
from shapely import geometry
from pygc import great_distance as gd


'''
Company: Kartoza
Project: GeoPackage spike remover - interview test
Author: Andre Theron (andretheronsa@gmail.com)
Created: February 2020
Requires: Python version 3.4+ for Pathlib
'''


def cmd_line_parse():
    '''Parse command line input and returns argument object'''

    example = "example: python3 ./spiky.py /home/input/"
    parser = arparse(description='Remove spikes from a GeoPackage polygons',
                     epilog=example)
    parser.add_argument('indir',
                        type=str,
                        default='/home/work/',
                        help="Directory containing GeoPackage files")
    parser.add_argument('-m',
                        type=int,
                        default=10,
                        help="Maximum angle of spikes (deg)")
    parser.add_argument('-a',
                        type=int,
                        default=1,
                        help="Max area change after spike removal (%)")
    args = parser.parse_args()
    return(args)


def calculate_angle(a: geometry.point,
                    b: geometry.point,
                    c: geometry.point) -> float:
    '''Calculate the absolute angle of point b towards point a and c
        WGS84 Geographic coordinates required
    '''
    # Calculate heading (reverse azimuth) between ab and cb
    ab = gd(start_latitude=a.y,
            start_longitude=a.x,
            end_latitude=b.y,
            end_longitude=b.x)['reverse_azimuth']
    cb = gd(start_latitude=c.y,
            start_longitude=c.x,
            end_latitude=b.y,
            end_longitude=b.x)['reverse_azimuth']
    b_angle = abs(ab - cb)
    return b_angle


def despike(polygon: geometry.polygon,
            min_angle: int) -> geometry.polygon:
    '''Removes vertices from shapely polygon with neighbouring angles > max'''

    # Polygon always has a single exterior and can have multiple interior rings
    coord_dict = {"exterior": [list(polygon.exterior.coords)]}
    if len(list(polygon.interiors)) > 0:
        coord_dict["interior"] = [i for i in list(polygon.interior.coords)]

    # Iterate over outer and inner ring(s)
    for side in coord_dict.items():
        for linear_ring in coord_dict[side]:
            # Add 2nd last point to list's 0th index to find 1st angle
            linear_ring.insert(0, linear_ring[-2])

            # Create dict of xy: angles - middle angle is calculated
            angles_dict = {}
            for i in range(len(linear_ring)-2):
                point_a = geometry.point.Point(linear_ring[i])
                point_b = geometry.point.Point(linear_ring[i+1])
                point_c = geometry.point.Point(linear_ring[i+2])
                b_angle = calculate_angle(point_a, point_b, point_c)
                angles_dict[point_b] = b_angle

            # Remove vertices with angles < angle
            for vertex, angle in angles_dict.items():
                if angle < min_angle:
                    angles_dict.pop(vertex)

        # Rebuild polygon
        new_poly = angle
    return new_poly


def optimize_angle(polygon: geometry.polygon,
                   max_angle: int,
                   max_area_delta: int) -> geometry.polygon:
    '''Find spikes in a polygon.

    Spikes are defined as a vertex forming a sharp angle
    (up to specified max angle) with neighbouring vertices
    and can be removed without significanbtly reducing the
    polygon area.
    '''

    angle = 0
    while angle < max_angle:
        orig_area = polygon.area
        despiked_polygon = despike(polygon, angle)
        new_area = despiked_polygon.area
        area_delta = min(orig_area, new_area) / max(orig_area, new_area)
        if area_delta > max_area_delta:
            return polygon
        else:
            polygon = despiked_polygon
            angle += 1


def main(in_dir: str,
         max_angle: int,
         max_area_delta: int):
    '''Main function
    Handles file input and performs quality checks.
    Finds all polygons from all GeoPackages.
    Feeds polygons to the iterative despike subroutines.
    Collects polygons and rebuilds geoseries and GeoPackages
    Writes out de-spiked data.
    '''

    # Read all valid GeoPackages in in_dir
    package_list = glob(in_dir + "*.gpkg")
    for package_file in package_list:
        package_path = Path(package_file).absolute()
        package_gdf = gpd.read_file(package_path)

        # Check geopackage contents
        if any(package_gdf.is_empty):
            logging.warning(f"{package_file} contains empty geometries-skip")
            continue
        elif not any(package_gdf.is_valid):
            logging.warning(f"{package_file} contains invalid geometries-skip")
            continue

        # Ensure gpkg is geographic coordinates - to use great circle formulae
        projection = package_gdf.crs
        if not projection.is_geographic:
            logging.warning(f"{package_file} is not in geographic coordinates")
            continue
        elif projection.name != 'WGS 84':
            logging.warning(f"{package_file} uses datum other than WGS84")
            continue

        # Process all polygons in geopackage
        new_package_list = []
        for polygon in package_gdf["geometry"]:

            # Despike polygon exterior and interior - ignore points/lines
            if type(polygon) == geometry.polygon.Polygon:
                despiked_layer = optimize_angle(polygon,
                                                max_angle,
                                                max_area_delta)
                new_package_list.append(despiked_layer)
            else:
                new_package_list(polygon)

            # Rebuild geoseries

        # Rebuild GeoPackage - project back and save
        despiked_gdf = new_package_list
        despiked_gdf_proj = despiked_gdf.poject(projection)
        despiked_gdf_proj.tofile(package_path.with_suffix("_despike.gpkg"),
                                 driver="GPKG")


if __name__ == "__main__":
    args = cmd_line_parse()
    main(in_dir=args.in_dir,
         max_angle=args.m,
         max_area_delta=args.a)
