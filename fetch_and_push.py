#!/usr/bin/python3

try:
    from database_inflater import inflate_into_db
    from osgeo import ogr as geo
    from subprocess import run
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


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
            tmp.append([feature.items().get('GID_{}'.format(i), 'NA'),
                        feature.items().get('NAME_{}'.format(i), 'NA'),
                        feature.GetGeometryRef().ExportToWkt()])
            # holds data in temp variable
            # data format -- [feature_id, feature_name, outline]
        if(inflate_into_db('world_features', 'username', 'password', {i: tmp})):
            # finally inflates into database
            print('[+]Success')
    return


if __name__ == '__main__':
    try:
        run('clear')
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
