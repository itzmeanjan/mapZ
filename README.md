# mapZ
A Geospatial Application

# Documentation

    - So, you interested in building a mapping application ?
    - Yes
    - Okay, I'm gonna take you through each and every step. All you need to do is to follow me.
    - You ready ?
    - Definitely

## Initial SetUp
    First thing first, you need world map data ( here we'll be using shapefiles ) to build a map of world. We'll use [GADM](https://gadm.org) as map data source. Here is the [data](https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip), which we'll require.

    So I've written small bash script for you to download and unzip that data.

    ```bash
    #!/usr/bin/bash
    # script downloads shape files from GADM, make sure you're connected to internet
    wget https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip
    # unzips downloaded zip into multiple layered shape files, which will be later on used for inflating features into database
    unzip gadm36_levels_shp.zip
    ```
