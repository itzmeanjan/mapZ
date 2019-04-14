# mapZ
A Geospatial Application, which I'm still working on

# Documentation

   :eyes: : So, you interested in building a mapping application ?
   
   :eyes: : Yes
   
   :eyes: : Okay, I'm gonna take you through each and every step. All you need to do is to follow me.
   
   :eyes: : You ready ?
   
   :eyes: : Definitely
   
   
## Platform and Tools used
   I'm going to use [*Fedora Linux*](https://getfedora.org/) for implementing this whole process.
   
   For database implementation I'll use *PostgreSQL*.
   ```shell
    postgres (PostgreSQL) 10.7
   ```
   
   GeoSpatial Data to be stored and processed using *PostGIS*.
   ```shell
    Name         : postgis
    Version      : 2.4.3
   ```
   
   A lot of *Python* scripts are going to be used for automating tile generation and database population procedure.
   ```shell
   Python 3.7.3
   ```
   
   *NPM* used for installing different *JavaScript* dependencies.
   ```shell
    >> npm --version
    6.4.1
   ```
   
   *Express* app to be written for implementing Tile Map Server.
   ```shell
    >> node --version
    v10.15.0
    >> npm info express
    express@4.16.4
   ```
   
   *Mapnik* used for rendering map tiles.
   ```shell
   >> mapnik --version
    3.0.20
   ```
   Well that's it :smile:.

## Initial SetUp
   First thing first, you need world map data ( here we'll be using shapefiles ) to build a map of world. We'll use [GADM](https://gadm.org) as map data source. Here is the [data](https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip), which we'll require.

   So I've written small bash script for you to download and unzip that data. Well you're free to do that on your own too.

   ```bash
   #!/usr/bin/bash
   # script downloads shape files from GADM, make sure you're connected to internet
   wget https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip
   # unzips downloaded zip into multiple layered shape files, which will be later on used for inflating features into database
   unzip gadm36_levels_shp.zip
   ```
   
   Now let's setup a [PostgreSQL](https://postgresql.org/) database with [postgis](https://postgis.net/) extension enabled.
   Make sure you've installed PostgreSQL database properly on your system. I found [it](http://www.glom.org/wiki/index.php?title=Initial_Postgres_Configuration) helpful. 
   
   Login to PostgreSQL.
   
   ```bash
    >> psql --username=your-user-name-for-postgresql # which is generally postgres
   ```
   
   Create a database named *world_features*.
   
   ```bash
    >> create database world_features;
   ```
   
   Now simply quit i.e. logout from *psql* prompt.
   
   ```bash
    >> \q
   ```
   
   Relogin to use newly created database.
   
   ```bash
    >> psql --username=your-user-name-for-postgresql --dbname=world_features
   ```
   
   Let's enable *postgis extension* for this database. Make sure you've installed *postgis* first.
   
   ```bash
    >> create extension postgis;
   ```
   
   And initial setup is done. Now we gonna automate things :wink:.
   

## Database Population
   :eyes: : That shapefile we downloaded, has 6 layers. So we'll be creating 6 different tables, where we're going to store that huge map data. 
   
   :eyes: : :worried:
   
   :eyes: : Hey wait, we're going to automate that whole thing. Now happy ???
   
   :eyes: : :relaxed:
   
   Alright so let's automate. And don't forget to grab a cup of :coffee:, cause this gonna be a bit longer.
   
   See we're going to process almost few hundreds of thousands features ( mostly polygon / multipolygon geometry ), using *geo.Open('/path-to-gadm36_0.shp').GetLayer(0).GetFeature(j).GetGeometryRef().ExportToWkt()*, where j is feature count. So of course this gonna be time consuming.
   
   
   ```python
   
    def app(path='/path-to-file/gadm36_{}.shp', file_id=[0, 1, 2, 3, 4, 5]):
        # path, path to gadm shapefiles
        # gadm has 6 layers, shape files hold corresponding layer number too
        print('[+]Now grab a cup of coffee, cause this gonna be a little longer ...\n')
        for i in file_id:
            print('[+]Working on `{}`'.format(path.format(i)))
            datasource = geo.Open(path.format(i))  # datasource opened
            # layer fetched, only a single layer present in a shape file
            layer = datasource.GetLayer(0)
            tmp = []
            for j in range(layer.GetFeatureCount()):
                feature = layer.GetFeature(j)  # gets feature by id
                gid = 'NA'
                name = 'NA'
                # there might be some fields present in shapefile, which is None
                if(feature.items().get('GID_{}'.format(i)) is not None):
                    # To handle so, I'm adding these two checks, otherwise those might be causing problem during database population
                    gid = feature.items().get('GID_{}'.format(i))
                if(feature.items().get('NAME_{}'.format(i)) is not None):
                    name = feature.items().get('NAME_{}'.format(i))
                tmp.append([gid, name,
                        feature.GetGeometryRef().ExportToWkt()])
                # holds data in temp variable
                # data format -- [feature_id, feature_name, outline]
            if(inflate_into_db('world_features', 'username', 'password', {i: tmp})):
                # finally inflate into database
                print('[+]Success')
    return
   ```
   
   Don't forget to change username and password, required for database login, before running [this](https://github.com/itzmeanjan/mapZ/blob/master/fetch_and_push.py) script.
   
   ```python
    if(inflate_into_db('world_features', 'username', 'password', {i: tmp})):
           # finally inflate into database
           print('[+]Success')
   ```
   
   Simply run [this](https://github.com/itzmeanjan/mapZ/blob/master/fetch_and_push.py) script and it'll be done.
   
   ```shell
    >>  python3 fetch_and_push.py 
   ```
   
   And it's done. Wanna check ?
   
   Login to *postgresql*.
   
   ```shell
    >> psql --username=your-user-name-for-postgresql --dbname=world_features
   ```
   
   Type in *psql* prompt.
   
   ```sql
    >> select feature_id, feature_name from world_features_level_0 where feature_id = 'IND';
    feature_id | feature_name 
    ------------+--------------
    IND        | India
    (1 row)
   ```
   
   And this is the structure of table, which the script built for us. All *6 tables* has same structure.
   
   ```sql
    >> \d world_features_level_0;
                   Table "public.world_features_level_0"
        Column    |       Type        | Collation | Nullable | Default 
    --------------+-------------------+-----------+----------+---------
    feature_id   | character varying |           | not null | 
    feature_name | character varying |           | not null | 
    outline      | geography         |           |          | 
    Indexes:
        "world_features_level_0_pkey" PRIMARY KEY, btree (feature_id)
        "world_features_level_0_index" gist (outline)
   ```
   
  
## Tile Generation
   This gonna be way more time consuming than previous one. I'm still working on it. I'll be back :sunglasses:.
   
   
   
## Tile Map Server
   The *Tile Map Server*, built using [NodeJS](https://nodejs.org/en/) i.e. [ExpressJS](http://expressjs.com/) Framework resides [here](https://github.com/itzmeanjan/mapZ/tree/master/tms).
   
   Get into *tms* directory and run following command, which will download all dependencies, required for running this express app.
   
   ```shell
      >> npm install
   ```
   
   
   This *Express* app will be working in local network. Make necessary changes, so that it can be discovered from Internet.
   ```javascript
      app.listen(8000, '0.0.0.0', () => {
      // tms listens at 0.0.0.0:8000, so that it can be accessed via both localhost and devices present in local network
      console.log('[+]Tile Map Server listening at - `0.0.0.0: 8000`\n');
   });
   ```
   
   Tile Map Server will be accepting *GET* request in  */tile/:zoom/:row/:col.png*   path, where *zoom* is Zoom Level value, *row* is Row ID( tile identifier along X-axis ) and *col* is Column ID( tile identifier along Y-axis ).
   
   ```javascript
      app.get('/tile/:zoom/:row/:col.png', (req, res) => {
      . 
      . // lots of code
      .
      });
   ```
   
   Ready to run Tile Map Server ?
   
   ```shell
   >>  node index.js
   ```
   
   As you can see on terminal its running. Just head to [this url](http://localhost:8000/tile/0/0/0.png), and you get to see a tile, which you built during that *very long* running tile generation procedure.
   
   
   ![Working Tile Map Server](https://github.com/itzmeanjan/mapZ/blob/master/screenshot_1.png)
   


   
   
