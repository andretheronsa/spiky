[![Build](https://images.microbadger.com/badges/version/andretheronsa/spiky.svg)](https://microbadger.com/images/andretheronsa/spiky)
![Docs](https://readthedocs.org/projects/docs/badge/?version=latest)
![Tests](https://github.com/andretheronsa/spiky/workflows/Python%20package/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689f88a473764cd888550434c908644a)](https://app.codacy.com/manual/andretheronsa/spiky?utm_source=github.com&utm_medium=referral&utm_content=andretheronsa/spiky&utm_campaign=Badge_Grade_Dashboard)

# Spiky

Spiky removes spikes from GeoPackage polygons

## Overview

### Spike definition:
* A single outlier vertex between two vertices that forms an acute angle to them
* A polygon can have more than one spike
* Spikes could be inward or outward
* Spikes can be on exterior of one or more interior boundaries of a polygon  
* Geographical location and scale should not affect spike detection
* Topology and geometry should be preserved - no simplifying

### Operation:
* Accepts a positional argument for filename
* Optionally accepts a max spike angle parameter (-a: float)  
* Writes out new file(s) (*_ds.gpkg) to same folder as input

![alt text](Isolated.png "Title")

### Limitations
* Does not work with line, multiline, or multipolygon geometries
* Does not consider geometries with dimensions higher than 2d (z, m)
* Input must be in geographic coordinates referenced to WGS84

## Getting started

### Docker

The simplest way of using the tool is to run the Docker image

The latest Docker image is available at: [Dockerhub](https://hub.docker.com/repository/docker/andretheronsa/spiky)

1. Pull image with:
```shell
docker pull andretheronsa/spiky:latest
```
2. Run program and mount directory with file as a volume: 
```shell
docker run -v /home/user/input/:/home/work/ spiky:latest spiky-polygons.gpkg
```
3. Outputs will be written to the same folder with '_ds' appended. 

### Local Python environment

Alternatively the tool can be downloaded and run with Python (3.5+).  
Required modules should be installed with pip.  
It is highly recommended to use Python Virtual environments (or similar tool) to avoid conflicts.  
Pip install on Windows will fail due to missing wheels for Geopandas dependencies - [alternative](https://geopandas.org/install.html).  

1. Pull code from git:
```shell
git clone https://github.com/andretheronsa/spiky.git
```
2. Enter folder and activate virtual environment (venv used in this case):
```shell
cd spiky/
python -m venv venv
./venv/Scripts/active

```
4. Install packages:
```shell
python3 -m pip install -r requirements.txt
```
5. Run program with arguments:
```shell
python3 spiky.py /home/user/spiky-polygon.gpkg -a 1
```
6. Outputs will be written to the same folder with '_ds' appended.

## Docs

Latest docs are available at: [Readthedocs](https://spiky.readthedocs.io/en/latest/?)

## Tests

Testing is done with Pytest and automated during master deploy using Github actions:

## TODO

* Enable line, multiline, or multipolygon geometries

## Author

Andre Theron
andretheronsa@gmail.com