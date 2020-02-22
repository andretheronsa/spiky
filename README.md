![build-status](https://img.shields.io/docker/pulls/mashape/kong.svg)
![docs](https://readthedocs.org/projects/docs/badge/?version=latest)
![Tests](https://github.com/andretheronsa/spiky/workflows/Python%20package/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689f88a473764cd888550434c908644a)](https://app.codacy.com/manual/andretheronsa/spiky?utm_source=github.com&utm_medium=referral&utm_content=andretheronsa/spiky&utm_campaign=Badge_Grade_Dashboard)

# Spiky

Program that removes spikes from a GeoPackage polygon

### Spike definition:
* A single outlier vertex between two vertices that forms an acute angle to them
* Distance from outlier to neighbouring vertices are similar 
* Removing the outlier should not change the polygon area significantly

### Notes:
* A spike at the first vertex in a polygon is removed.
* Spike could be inward or outward
* Geographical location should not affect spike detection (Poles / Equator)
* Topology and geometry should be preserved

### Operation:
* Accepts input *.gpkg file containing one, or more polygons
* Writes out *_despike(n).gpkg file with spikes removed to same folder as input
* Iteratively checks for spikes by increasing the angle, distance ratio untill the max angle is reached or the polygon area changes
* Optionally accepts 3 paramters
    - Max angle
    - Distance ratio
    - Acceptable area delta

### Limitations
* Does not work with lines

## Getting started
* Pull docker image (See below)

## Docker

The latest Docker image is available at: [Dockerhub](https://hub.docker.com/repository/docker/andretheronsa/spiky)

Pull image with:

```shell
docker pull andretheronsa/spiky
```
## Docs

Latest docs are available at: [Readthedocs](https://spiky.readthedocs.io/en/latest/?)

## Tests

Testing is done with Pytest using Github actions: 

## Author

Andre Theron
andretheronsa@gmail.com