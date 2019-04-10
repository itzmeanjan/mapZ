#!/usr/bin/python3

try:
    from database_inflater import inflate_into_db
    from osgeo import ogr as geo
    from subprocess import run
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def app(path='/home/anjan/Documents/my_programs/still_working/python_codes/gis_data/gadm_world_data/gadm36_{}.shp', file_id=[0, 1, 2, 3, 4, 5]):
    # path, path to gadm shapefiles
    # gadm has 6 layers, shape files hold corresponding layer number too
    data_set = {}
    for i in file_id:
        print('[+]Working on `{}`'.format(path.format(i)))
        datasource = geo.Open(path.format(i))  # datasource opened
        # layer fetched, only a single layer present in a shape file
        layer = datasource.GetLayer(0)
        tmp = []
        for j in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(j)  # gets feature by id
            tmp.append([feature.items().get('GID_{}'.format(i)),
                        feature.items().get('NAME_{}'.format(i)),
                        feature.GetGeometryRef().ExportToWkt()])
            # holds data in temp variable
            # data format -- [feature_id, feature_name, outline]
        data_set.update({i: tmp})  # pushes into dictionary
    print(data_set)
    return
    if(inflate_into_db('world_features', 'postgres', '@njan5m3dB', data_set)):
        # finally inflate into database
        print('[+]Done')
    return


if __name__ == '__main__':
    try:
        run('clear')
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
