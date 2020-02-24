#!/usr/bin/env python3

'''Spiky

Spiky removes spikes from GeoPackage shapes.

Args:
    inputfile: Input GeoPackage file (path or file in cwd)

Kwargs:
    -a, --angle: Maximum angle of spikes (degrees)

Output:
    Geopackage in folder of inputfile with '_ds' suffix: {inputfile}_ds.gpkg

Example:
    $ spiky.py spiky-polygon.gpkg -a 1
'''

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
from pathlib import Path

import geopandas as gpd
from pygc import great_distance as gd
from shapely import geometry

# Configure logger - currently only prints to console
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def cmd_line_parse():
    '''Parses command line input and returns argument object'''
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
    args = parser.parse_args()
    return(args)


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


def despike_coords(coord_list: list,
                   angle: float) -> list:
    '''Removes spikes from a coord list.

    Spikes are vertices with neighbouring angles < min.  
    Coordinates can be line or ring.

    Args:
        coord_list: Input list of xy tuples to be despiked.
        angle: Maximum angle of spikes (degrees).

    Returns:
        Despiked coord list.

    '''
    # Check if coordlist is enclosing ring - Pad initial point with end
    if coord_list[0] == coord_list[-1]:
        coord_list.insert(0, coord_list[-2])
        ring = True
        logging.debug(f"Coordlist is ring")

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
        new_coord_list.insert(0, coord_list[0])
    return new_coord_list


def despike(shape: geometry, angle: float) -> geometry:
    '''Removes spikes from various shapely geometries.

    Deconstructs shape's CoordSequences into lists.  
    Runs despike_list() on these and rebuilds the shape.  
    Currently supports only Polygons.  
    Line, MultiLine and Multipolygon are possible.  

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
                new_coords = despike_coords(list(coords), angle)
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


def main(inputfile: Path, angle: float):
    '''Despikes all shapes in a GeoPackage.

    Handles file i/o, quality checks and despikes.

    Args:
        inputfile: Input GeoPackage file (path or file in cwd)
        angle: Maximum angle of spikes (degrees).

    Raises:
        ValueError: If GeoPackage file contains invalid shapes.

    '''
    package_gdf = gpd.read_file(inputfile)
    crs = package_gdf.crs

    # Check geopackage contents
    if any(package_gdf.is_empty):
        raise ValueError("GeoPackage contains empty geometry.")
    elif not any(package_gdf.is_valid):
        raise ValueError("GeoPackage contains invalid geometry.")
    elif not crs.is_geographic:
        raise ValueError("GeoPackage CRS not geographic.")
    elif crs.name != 'WGS 84':
        raise ValueError("GeoPackage CRS not WGS84.")

    # Despike geometry column of geodataframe in place
    logging.info(f"Despike with max angle: {angle} - infile: {inputfile.name}")
    package_gdf["geometry"] = package_gdf["geometry"].apply(lambda s:
                                                            despike(s, angle))
    outfile = inputfile.parent / (inputfile.stem + "_ds.gpkg")
    package_gdf.to_file(outfile, driver="GPKG")
    logging.info(f"Despike complete - outfile: {outfile.name}")


if __name__ == "__main__":
    args = cmd_line_parse()
    main(inputfile=args.inputfile, angle=args.angle)
