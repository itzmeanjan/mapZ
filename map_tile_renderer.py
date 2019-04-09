#!/usr/bin/python3

try:
    import mapnik as my_map
    from sys import argv
    from os.path import exists
    from subprocess import run
    import tile_extent_determinator as tile_ex
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def find_center_point_of_tile(extent):
    return ((extent[0]+extent[1])/2, (extent[2]+extent[3])/2)


def tile_generator(x_val, y_val, zoom_lvl, degree_along_x, degree_along_y, num_of_tiles_to_start_with, tile_width, tile_height, style_sheet, output_file):
    num_of_tiles = tile_ex.tiles_required_at_certain_zoom_level(
        num_of_tiles_to_start_with, zoom_lvl)
    print('[+]No.of tiles required => {}'.format(num_of_tiles))
    extent = tile_ex.get_tile_extent(zoom_lvl, (-180, +90), tile_width, tile_height,
                                     degree_along_x, degree_along_y).get('{},{}'.format(x_val, y_val), [])
    print(extent)
    if(not extent):
        return False
    center = find_center_point_of_tile(extent)
    print('[+]Center point of Tile : {}, {}'.format(*center))
    map_obj = my_map.Map(tile_width, tile_height,
                         '+proj=longlat +datum=WGS84 +no_defs ')
    with open(style_sheet, 'r') as fd:
        content = fd.read()
    with open('tmp.xml', 'w') as fd:
        fd.write(content.format('{},{},{},{}'.format(*extent)))
    my_map.load_map(map_obj, 'tmp.xml')
    map_obj.zoom_to_box(my_map.Box2d(*extent))
    my_map.render_to_file(map_obj, output_file, 'png')
    # if(find_file('tmp.xml')):
    #	unlink('tmp.xml')
    return True


def main(tile_width, tile_height):
    if(len(argv) != 7):
        print('[+]Usage : ./{} zoom-level x-value y-value number-of-tiles-to-start-with style-sheet image-file-name\n\t[*] zoom-level = 0 to 10\n\t[*] number-of-tiles-to-start-with = 2^x , where x= 0,1,2,3 .... \n'.format(argv[0]))
        return
    zoom_lvl, x_val, y_val, num_of_tiles_to_start_with, style_sheet, image_file = argv[1:]
    zoom_lvl = int(zoom_lvl)
    x_val = int(x_val)
    y_val = int(y_val)
    num_of_tiles_to_start_with = int(num_of_tiles_to_start_with)
    if(zoom_lvl < 0 or zoom_lvl > 10):
        print('[!]Zoom level value should be in range of 0 to 10\n')
        return
    t = True
    i = 0
    while(t):
        tmp = 2**i
        if(tmp == num_of_tiles_to_start_with):
            t = False
        if(tmp > num_of_tiles_to_start_with):
            t = False
            i = -1
        i += 1
    if(i < 1):
        print('[!]Minimum number of tiles required to cover World at zoomed out condition needs to be 2^x where x=0,1,2,3 ....\n')
        return
    if(not exists(style_sheet)):
        print('[!]Style Sheet not available !\n')
        return
    print('[+]Generating tile ({},{}) with zoom level {} ...'.format(x_val, y_val, zoom_lvl))
    if(not tile_generator(x_val, y_val, zoom_lvl, 360, 180, num_of_tiles_to_start_with, tile_width, tile_height, style_sheet, image_file)):
        print('[!]Illegal Tile extent value !')
        return
    print('[+]Rendered tile ({},{}) with zoom-level {} to file \'{}\'\n'.format(x_val,
                                                                                y_val, zoom_lvl, image_file))
    return


if __name__ == '__main__':
    run('clear')
    try:
        main(256, 144)
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
