#!/usr/bin/env python3

'''Spiky

Spiky removes spikes from GeoPackage shapes.

Args:
    inputfile: Input GeoPackage file (path or file in cwd)

Kwargs:
    -a, --angle: Maximum angle of spikes (degrees)
    -v, --verbose: Print debug log messages

Output:
    Geopackage in folder of inputfile with '_ds' suffix: {inputfile}_ds.gpkg

Example:
    $ spiky.py spiky-polygon.gpkg -a 1
'''

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
import logging
from pathlib import Path

import geopandas as gpd
from pygc import great_distance as gd
from shapely import geometry
import sys


def conf_logger(verbose: bool):
    ''''Configure Spiky's logging level'''
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=level,
                        datefmt='%Y-%m-%d %H:%M:%S')


def cmd_line_parse(args) -> Namespace:
    '''Parses command line input and returns argument object

    Returns:
        args

    '''
    example = "example: ./spiky.py spiky-polygon.gpkg -a 0.5"
    parser = ArgumentParser(description='Remove spikes from GeoPackage.',
                            epilog=example,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("inputfile",
                        type=lambda p: Path(p).absolute(),
                        help="Input GeoPackage file (path or file in cwd)")
    parser.add_argument("-a",
                        "--angle",
                        metavar='',
                        type=float,
                        default=1.0,
                        help="Maximum angle of spikes (degrees)")
    parser.add_argument("-v",
                        "--verbose",
                        action='store_true',
                        help="Print all log messages")
    return parser.parse_args(args)


def calculate_angle(a: tuple,
                    b: tuple,
                    c: tuple) -> float:
    '''Calculates the absolute geographic angle of point b
    with regards to neighbouring points a and c.

    Points should be in WGS84 Geographic coordinates.

    Args:
        a: Neighbouring point a (xy tuple).
        b: Center point b (xy tuple).
        c: Neighbouring point c (xy tuple).

    Returns:
        The absolute angle.

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


def despike_list(coord_list: list,
                 angle: float = 1) -> list:
    '''Removes spikes from a coord list.

    Spikes are vertices with neighbouring angles < min.
    Coordinates can be line or ring.

    Args:
        coord_list: Input list of xy tuples to be despiked.
        angle: Maximum angle of spikes (degrees).

    Returns:
        Despiked coord list.

    '''
    # Check if coordlist is point/list/ring - Pad initial point with end
    if len(coord_list) <= 2:
        logging.debug("Coordlist contains only two points - can't despike")
        return coord_list
    elif coord_list[0] == coord_list[-1]:
        ring = True
        coord_list.insert(0, coord_list[-2])
        logging.debug("Coordlist is ring")
    else:
        ring = False
        logging.debug("Coordlist is line")

    # Create list without spikes
    new_coord_list = []
    for count in range(len(coord_list)-2):
        point_a = coord_list[count]
        point_b = coord_list[count+1]
        point_c = coord_list[count+2]
        b_angle = calculate_angle(point_a, point_b, point_c)
        if b_angle > angle:
            new_coord_list.append(point_b)
        else:
            logging.debug(f"Spike vertex detected: {point_b}")

    # Ensure ring encloses again - otherwise pad line ends
    if ring:
        new_coord_list.append(new_coord_list[0])
    else:
        new_coord_list.insert(0, coord_list[0])
        new_coord_list.append(coord_list[-1])
    return new_coord_list


def despike_shape(shape: geometry, angle: float = 1) -> geometry:
    '''Removes spikes from various shapely geometries.

    Deconstructs shape's CoordSequences into lists,
    despikes the lists and rebuilds the shape.

    Currently supports only Polygons but Line, MultiLine
    and Multipolygon are possible.

    Args:
        shape: Input shapely geometry.
        angle: Maximum angle of spikes (degrees).

    Returns:
        Despiked shape.

    '''
    logging.debug(f"{shape.type} detected")
    if shape.type == "Polygon":
        # Polygons have coords for exterior and list for interior(s)
        poly_dict = {"outer": [shape.exterior.coords]}
        if len(list(shape.interiors)) > 0:
            logging.debug(f"Polygon interior geometries detected")
            poly_dict["inner"] = [i.coords for i in shape.interiors]

        # Despike all CoordinateSequence lists in obj and rebuild poly
        new_poly_dict = {}
        for side in poly_dict.keys():
            new_coord_list = []
            for coords in poly_dict[side]:
                new_coords = despike_list(list(coords), angle)
                new_coord_list.append(new_coords)
            new_poly_dict[side] = new_coord_list

        if "inner" in poly_dict:
            new_shape = geometry.Polygon(shell=new_poly_dict["outer"][0],
                                         holes=new_poly_dict["inner"])
        else:
            new_shape = geometry.Polygon(shell=new_poly_dict["outer"][0])

    # elif shape.type == "MultiPolygon":
    # elif shape.type == "Line":
    # elif shape.type == "MultiLine":
    else:
        logging.warning(f"{shape.type} cannot be despiked yet - ignore")
        new_shape = shape
    return new_shape


def despike_gdf(package_gdf: gpd.GeoDataFrame,
                angle: float = 1,
                verbose: bool = False) -> gpd.GeoDataFrame:
    '''Despikes all shapes in a GeoDataFrame.

    Args:
        package_gdf: Input GeoPackage object
        angle: Maximum angle of spikes (degrees).

    Returns:
        Despiked GeoPackage object

    '''
    conf_logger(verbose)
    verify_gdf(package_gdf, package_gdf.name)
    logging.info(f"Despike with max angle: {angle}")
    package_gdf["geometry"] = package_gdf["geometry"].apply(
        lambda s: despike_shape(s, angle))
    verify_gdf(package_gdf, package_gdf.name + "_ds")
    logging.info(f"Despike complete")
    return package_gdf


def verify_gdf(package_gdf: gpd.GeoDataFrame, name: str = "File") -> bool:
    '''Verifies GeoPandas GeoDataframe validity.

    Args:
        shape: Input geopandas GeoDataframe.

    Returns:
        bool: True if file is valid.

    Raises:
        ValueError: If GeoDataframe file is not valid for Spiky.

    '''
    crs = package_gdf.crs
    if any(package_gdf.is_empty):
        raise ValueError(f"{name} contains empty geometry.")
    elif not any(package_gdf.is_valid):
        raise ValueError(f"{name} contains invalid geometry.")
    elif not crs.is_geographic:
        raise ValueError(f"{name} CRS not geographic.")
    elif crs.name != 'WGS 84':
        raise ValueError(f"{name} CRS not WGS84.")
    else:
        logging.info(f"{name} is valid")
        return True


if __name__ == "__main__":
    args = cmd_line_parse(sys.argv[1:])
    package_gdf = gpd.read_file(args.inputfile)
    despiked = despike_gdf(package_gdf=package_gdf,
                           angle=args.angle,
                           verbose=args.verbose)
    outfile = args.inputfile.parent / (args.inputfile.stem + "_ds.gpkg")
    package_gdf.to_file(outfile, driver="GPKG")
