#!/usr/bin/python3

try:
    from xml.etree.ElementTree import SubElement, parse as parse_xml
    from mapnik import Map, load_map, render_to_file, Box2d
    from sys import argv
    from os import getcwd, unlink, mkdir
    from os.path import exists, join
    from subprocess import run
    from tile_extent_determinator import get_tile_extent
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def format_style_sheet(xml_doc, layer_name, element_name, element_attrs, element_text, target_xml):
    # formats template XML stylesheet during runtime.
    et = parse_xml(xml_doc)  # parsing XML document
    for i in et.getroot().findall('Layer'):
        # iterates over all available layers in XML and selects those which is mentioned in layer_name parameter
        if(not layer_name):
            break  # if layer_name is exhausted, just break loop
        if(i.attrib.get('name') in layer_name):
            # remove that layer which is found and to be processed
            layer_name.remove(i.attrib.get('name'))
            target_elem = i.find('Datasource')  # this is our target element
            if(not target_elem):
                # if something goes wrong with target Layer Name, denote failure
                return False
            # creating a new element, which is child of our target `Datasource` element
            subelement = SubElement(target_elem, element_name)
            subelement.text = element_text  # setting text for newly added element
            subelement.set(*element_attrs)  # sets attribute of new element
    if(exists(target_xml)):
        unlink(target_xml)
    et.write(target_xml)  # writes to another XML stylesheet
    return True


def tile_generator(zoom_lvl, tile_width, tile_height, style_sheet, target_storage_path):
    print('\n\t[+]Generating tiles in zoom level -- {}\n'.format(zoom_lvl))
    tiles = get_tile_extent(zoom_lvl, (-180, +90), tile_width, tile_height,
                            360, 180)
    if(not tiles):
        return False
    for key, value in tiles.items():
        map_obj = Map(tile_width, tile_height,
                      '+proj=longlat +datum=WGS84 +no_defs ')
        if(not format_style_sheet(style_sheet, ['layer1', 'layer2', 'layer3', 'layer4', 'layer5', 'layer6'], 'Parameter', [
                'name', 'extent'], '{}, {}, {}, {}'.format(*value), 'tmp.xml')):
            return False
        print(
            '\t\t[+]Rendering tile {} - {} - {} ...'.format(zoom_lvl, *key.split(',')))
        load_map(map_obj, 'tmp.xml')  # loads generated XML style sheet
        map_obj.zoom_to_box(Box2d(*value))
        render_to_file(map_obj, join(target_storage_path, '{}_{}_{}.png'.format(
            zoom_lvl, *key.split(','))), 'png256')
    # removes temporary XML file, which was generated from template XML
    unlink('tmp.xml')
    return True


def input_validator():
    # validates input, which was provided during invokation of function
    init_zoom_lvl, max_zoom_lvl = argv[1:]
    try:
        init_zoom_lvl = int(init_zoom_lvl)
        max_zoom_lvl = int(max_zoom_lvl)
    except ValueError as e:
        print('[!]Error : {}'.format(str(e)))
        return ()
    if((init_zoom_lvl < 0 or init_zoom_lvl > 18) or (max_zoom_lvl < 0 or max_zoom_lvl > 18)):
        print('[!]Zoom level value should be in range of 0 to 10')
        return ()
    for i in range(init_zoom_lvl, max_zoom_lvl+1):
        if(not exists('map_tile_renderer_style_sheet_{}.xml'.format(i))):
            print('[!]Style Sheet not available for zoom-level -- {} !\n'.format(i))
            return ()
    return init_zoom_lvl, max_zoom_lvl


def app(tile_width, tile_height):
    if(len(argv) != 3):
        # now it can generate only those tiles, which are specified using their zoom_level
        print(
            '[+]Usage : ./{} init-zoom-level max-zoom-level\n\t[*] init-zoom-level = 0 to 10\n\t[*] max-zoom-level = 0 to 10\n'.format(argv[0]))
        return
    # if command line input argument is not okay, it'll fail simply
    try:
        init_zoom_lvl, max_zoom_lvl = input_validator()
    except ValueError:
        return
    target_storage_path = join(getcwd(), 'tiles')
    if(not exists(target_storage_path)):
        mkdir(target_storage_path)
    print('[+]Generating all tiles with starting zoom level {} & max zoom level {}\n'.format(init_zoom_lvl, max_zoom_lvl))
    for i in range(init_zoom_lvl, max_zoom_lvl+1):
        if(not tile_generator(i, tile_width, tile_height, 'map_tile_renderer_style_sheet_{}.xml'.format(i), target_storage_path)):
            print('\t[!]Illegal Tile extent value !')
            return
    print('[+]Success')
    return


if __name__ == '__main__':
    run('clear')
    try:
        app(256, 128)
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
