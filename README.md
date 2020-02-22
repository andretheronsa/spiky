![build-status](https://img.shields.io/docker/pulls/mashape/kong.svg)
![docs](https://readthedocs.org/projects/docs/badge/?version=latest)
![Tests](https://github.com/andretheronsa/spiky/workflows/Python%20package/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689f88a473764cd888550434c908644a)](https://app.codacy.com/manual/andretheronsa/spiky?utm_source=github.com&utm_medium=referral&utm_content=andretheronsa/spiky&utm_campaign=Badge_Grade_Dashboard)

# Spiky

Program that removes spikes from a GeoPackage polygon

### Spike definition:
* A single outlier vertex between two vertices that forms an acute angle to them
* Removing the outlier should not change the polygon area significantly

### Notes:
* A spike at the first vertex in a polygon is removed.
* Spike could be inward or outward
* Geographical location should not affect spike detection (poles / equator)
* Topology and geometry should be preserved - no simplifying

### Operation:
* Accepts input *.gpkg file containing one, or more polygons
* Iteratively checks for spikes by increasing the angle untill the max angle is reached or the polygon area changes
* Optionally accepts 3 paramters
    - Max angle
    - Max area delta
* Writes out *_despike.gpkg file with spikes removed to same folder as input

### Limitations
* Does not work with line data

## Getting started
* Pull docker image (See below)

The latest Docker image is available at: [Dockerhub](https://hub.docker.com/repository/docker/andretheronsa/spiky)

Pull image with:

```shell
docker pull andretheronsa/spiky:latest
```

Run program with:

```shell
docker run --rm spiky:latest -v :/home/
```

## Docs

Latest docs are available at: [Readthedocs](https://spiky.readthedocs.io/en/latest/?)

## Tests

Testing is done with Pytest using Github actions: 

## Author

Andre Theron
andretheronsa@gmail.com