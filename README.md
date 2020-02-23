![build-status](https://img.shields.io/docker/pulls/mashape/kong.svg)
![docs](https://readthedocs.org/projects/docs/badge/?version=latest)
![Tests](https://github.com/andretheronsa/spiky/workflows/Python%20package/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689f88a473764cd888550434c908644a)](https://app.codacy.com/manual/andretheronsa/spiky?utm_source=github.com&utm_medium=referral&utm_content=andretheronsa/spiky&utm_campaign=Badge_Grade_Dashboard)

# Spiky

Program that removes spikes from a GeoPackage polygon

## Overview

### Spike definition:
* A single outlier vertex between two vertices that forms an acute angle to them
* Removing the outlier should not change the polygon area significantly

### Notes:
* A spike at the first vertex in a polygon is removed
* A polygon can have more than one spike
* Spikes could be inward or outward
* Spikes can be on exterior of one or more interior boundries of the polygon
* Geographical location should not affect spike detection (poles / equator)
* Topology and geometry should be preserved - no simplifying

### Operation:
* Accepts input *.gpkg file containing one, or more geometries
* Iteratively checks for spikes on polygon geometries by increasing the angle until the max angle is reached or the polygon area changes significantly
* Optionally accepts 2 paramters:
    - Max angle
    - Max area delta
* Writes out *_despike.gpkg file with spikes removed to same folder as input

### Limitations
* Does not work with line data
* Does not consider geometries with dimensions higher than 2d
* Input must be in geographic coordinates referenced to WGS84

## Getting started

### Docker

The simplest way of using the tool is to run the Docker image

The latest Docker image is available at: [Dockerhub](https://hub.docker.com/repository/docker/andretheronsa/spiky)

1. Pull image with:
```shell
docker pull andretheronsa/spiky:latest
```
2. Run program by mapping folder containing '.dpkg' files to be despiked as volume to /home/work/:
```shell
docker run spiky:latest -v /home/user/input/:/home/input/
```

3. Outputs will be written to the same folder with '_despiked' appended.

### Local Python environment

Alternatively the tool can be downloaded and run with Python (3.5+).  
Required modules should be installed with pip.  
It is highly reccomended to use Python Virtual environments (or similar tool) to avoid conflicts.  
Pip install on Windows will fail due to missing wheels for Geopandas dependencies - [alternative](https://geopandas.org/install.html).  

1. Pull code from git
```shell
git clone 
```
2. Enter folder and activate virtual environment (venv used in this case)
```shell
cd spiky/
python -m venv venv
./venv/Scripts/active

```
4. Install packages
```shell
python3 -m pip install -r requirements.txt
```
5. Run program with folder containing '.dpkg' files to be despiked
```shell
python3 spiky.py /home/user/files
```
6. Outputs will be written to the same folder with '_despiked' appended.

## Docs

Latest docs are available at: [Readthedocs](https://spiky.readthedocs.io/en/latest/?)

## Tests

Testing is done with Pytest and automated during master deploy using Github actions: 

## Author

Andre Theron
andretheronsa@gmail.com