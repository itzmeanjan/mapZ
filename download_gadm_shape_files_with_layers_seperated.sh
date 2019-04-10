#!/usr/bin/bash

# script downloads shape files from GADM, make sure you're connected to internet
wget https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip
# unzips downloaded zip into multiple layered shape files, which will be later on used for inflating features into database
unzip gadm36_levels_shp.zip
