#!/usr/bin/env python3

'''Spiky

Program that removes spikes from GeoPackage shapes.

Company: Kartoza
Project: GeoPackage spike remover - interview test
Author: Andre Theron (andretheronsa@gmail.com)
Created: February 2020
Requires: Python version 3.4+ for Pathlib

Example:
    $ python spiky.py /home/work/ -a 1
'''


from argparse import ArgumentParser as arparse
import logging
from pathlib import Path
import sys

import geopandas as gpd
from pygc import great_distance as gd
from shapely import geometry

def cmd_line_parse():
    '''Parse command line input and returns argument object'''
    example = "example: python3 ./spiky.py /home/input/ -a 2"
    parser = arparse(description='Remove spikes from a GeoPackage polygons',
                     epilog=example)
    parser.add_argument("filename",
                        nargs='?',
                        type=str,
                        default='/home/work/',
                        help="Directory containing GeoPackage files")
    parser.add_argument("-a",
                        type=float,
                        default=1.0,
                        help="Maximum angle of spikes (deg)")
    args = parser.parse_args()
    return(args)


def calculate_angle(a: tuple,
                    b: tuple,
                    c: tuple) -> float:
    '''Calculate the absolute angle of point b with regards to
    neighbouring points a and c.

    Points in WGS84 Geographic coordinates required.

    :param a: Neighbouring point a (xy tuple)
    :param b: Center point b (xy tuple)
    :param c: Neighbouring point c (xy tuple)
    :type a: tuple
    :type b: tuple
    :type c: tuple
    :return: Returns absolute angle
    :rtype: float
    '''
    heading_ab = gd(start_latitude=a[1],
                    start_longitude=a[0],
                    end_latitude=b[1],
                    end_longitude=b[0])['reverse_azimuth']
    heading_cb = gd(start_latitude=c[1],
                    start_longitude=c[0],
                    end_latitude=b[1],
                    end_longitude=b[0])['reverse_azimuth']
    b_angle = abs(heading_ab - heading_cb)
    return b_angle


def despike_coords(coord_list: list,
                   angle: float) -> list:
    '''Removes spikes from a coord list.

    Spikes are vertices with neighbouring angles < min.
    Coordinates can be line or ring.

    :param coord_list: Input list of xy tuples to be despiked
    :param angle: Maximum angle that defines a spike (deg)
    :type coord_list: list
    :type angle: float
    :return: Returns despiked coord list
    :rtype: list
    '''
    # Check if coordlist is enclosing ring
    if coord_list[0] == coord_list[-1]:
        ring = True
        # Pad initial point with end of ring
        coord_list.insert(0, coord_list[-2])

    # Create list without spikes
    new_coord_list = []
    for count in range(len(coord_list)-2):
        point_a = coord_list[count]
        point_b = coord_list[count+1]
        point_c = coord_list[count+2]
        b_angle = calculate_angle(point_a, point_b, point_c)
        if b_angle > angle:
            new_coord_list.append(point_b)

    if ring:
        # Ensure ring encloses again
        new_coord_list.append(new_coord_list[0])
    else:
        # Put back first and last point if line
        new_coord_list.insert(0, coord_list[0])
        new_coord_list.insert(0, coord_list[0])
    return new_coord_list


def despike(shape: geometry, angle: float) -> geometry:
    '''Removes spikes various shapely geometries using despike_coords().

    Currently supports only Polygon geometries.
    Line, MultiLine and Multipolygon should be possible.

    :param shape: Input shapely geometry
    :param angle: Maximum angle that defines a spike (deg)
    :type shape: geometry
    :type angle: float
    :return: Returns despiked shape
    :rtype: geometry
    '''
    if shape.type == "Polygon":
        # Polygons have coords for exterior and list for interior(s)
        poly_dict = {"outer": [shape.exterior.coords]}
        if len(list(shape.interiors)) > 0:
            poly_dict["inner"] = [i.coords for i in shape.interiors]

        # Despike all CoordinateSequence lists in obj and rebuild poly
        new_poly_dict = {}
        for side in poly_dict.keys():
            new_coord_list = []
            for coords in poly_dict[side]:
                new_coords = despike_coords(list(coords), angle)
                new_coord_list.append(new_coords)
            new_poly_dict[side] = new_coord_list

        if "inner" in poly_dict:
            new_shape = geometry.Polygon(shell=new_poly_dict["outer"][0],
                                         holes=new_poly_dict["inner"])
        else:
            new_shape = geometry.Polygon(shell=new_poly_dict["outer"][0])

    # elif shape.type == "MultiPolygon":
    # elif shape.type == "line":
    # elif shape.type == "MultiLine":
    else:
        logging.warning(f"{shape.type} cannot be despiked yet - ignore")
        new_shape = shape
    return new_shape


def main(filename: str, angle: float):
    '''Main function that handles file input and performs quality checks.
    Finds all shapes within GeoPackage, despikes and save to GeoPackages.
    '''
    package_path = Path(filename).absolute()
    package_gdf = gpd.read_file(package_path)
    crs = package_gdf.crs

    # Check geopackage contents
    if any(package_gdf.is_empty):
        logging.warning(f"{package_path.name} geometry empty - skip")
        sys.exit(1)
    elif not any(package_gdf.is_valid):
        logging.warning(f"{package_path.name} geometry invalid - skip")
        sys.exit(1)
    elif not crs.is_geographic:
        logging.warning(f"{package_path.name} coordinates not geographic")
        sys.exit(1)
    elif crs.name != 'WGS 84':
        logging.warning(f"{package_path.name} CRS not WGS84")
        sys.exit(1)

    # Despike geometry column of geodataframe in place
    package_gdf["geometry"] = package_gdf["geometry"].apply(lambda s:
                                                            despike(s, angle))
    outfile = package_path.parent / (package_path.stem + "_ds.gpkg")
    package_gdf.to_file(outfile, driver="GPKG")


if __name__ == "__main__":
    args = cmd_line_parse()
    main(filename=args.filename, angle=args.a)
