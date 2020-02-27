from spiky import spiky
import pytest


def test_cmd_line_parse():
    test_args = ["/test/file.gpkg", "-a 21", "-v"]
    args = spiky.cmd_line_parse(test_args)
    assert isinstance(args.inputfile, spiky.Path)
    assert args.angle == 21.0
    assert args.verbose


def test_calculate_angle_right_angled_triangle():
    null_island = (0, 0)
    north_pole = (180, 90)
    equator_90_east = (90, 0)
    angle = spiky.calculate_angle(null_island, north_pole, equator_90_east)
    assert angle == 90.0


def test_calculate_angle_same_neighbour_angle_zero():
    neighbour = (32.01, -22.7)
    center = (33, 22.1)
    angle = spiky.calculate_angle(neighbour, center, neighbour)
    assert angle == 0.0


def test_despike_list_close_ring():
    ring = [(33.1, 29), (32.4, 29), (32.4, 24), (33.1, 24), (33.1, 29)]
    despike_ring = spiky.despike_list(ring)
    assert despike_ring[0] == despike_ring[-1]


def test_despike_list_pad_line():
    line = [(33.1, 29), (32.1, 28), (32.1, 27), (32.1, 26)]
    despike_line = spiky.despike_list(line)
    assert line == despike_line


def test_despike_list_point_ignore():
    line = [(33.1, 29)]
    despike_line = spiky.despike_list(line)
    assert line == despike_line


def test_despike_shape_output_type():
    point = spiky.geometry.Point(2, 3)
    new_point = spiky.despike_shape(point)
    poly = spiky.geometry.Polygon(shell=[(22, 31), (24.2, 26), (19.2, 18.2)])
    new_poly = spiky.despike_shape(poly)
    assert isinstance(new_point, type(point))
    assert isinstance(new_poly, type(poly))


@pytest.fixture
def complex_spiked_gdf():
    test_data = spiky.Path("./tests/fixtures/inner-spiky-polygons.gpkg")
    gdf = spiky.gpd.read_file(test_data)
    return gdf


@pytest.fixture
def complex_despiked_gdf():
    test_data = spiky.Path("./tests/fixtures/inner-spiky-polygons_ds.gpkg")
    gdf = spiky.gpd.read_file(test_data)
    return gdf


def test_verify_gdf(complex_spiked_gdf):
    verified = spiky.verify_gdf(complex_spiked_gdf)
    assert verified


def test_despike_gdf_complex_spiked_polygon(complex_despiked_gdf):
    spiked_data = spiky.Path("./tests/fixtures/inner-spiky-polygons.gpkg")
    package_gdf = spiky.gpd.read_file(spiked_data)
    despiked = spiky.despike_gdf(spiked_data)
    assert complex_despiked_gdf.equals(despiked)
