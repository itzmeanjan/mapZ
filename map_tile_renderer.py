#!/usr/bin/python3

try:
    from xml.etree.ElementTree import SubElement, parse as parse_xml
    from mapnik import Map, load_map, render_to_file, Box2d
    from os import unlink
    from sys import argv
    from os.path import exists
    from subprocess import run
    from tile_extent_determinator import get_tile_extent, tiles_required_at_certain_zoom_level
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def format_style_sheet(xml_doc, layer_name, element_name, element_attrs, element_text, target_xml):
    # formats template XML stylesheet during runtime.
    et = parse_xml(xml_doc)  # parsing XML document
    target_elem = None
    for i in et.getroot().findall('Layer'):
        # iterates over all available layers in XML and selects one using layer_name attribute
        if(i.attrib.get('name') == layer_name):
            target_elem = i.find('Datasource')  # this is our target element
            break  # in case of success, just break loop
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


def tile_generator(x_val, y_val, zoom_lvl, degree_along_x, degree_along_y, num_of_tiles_to_start_with, tile_width, tile_height, style_sheet, output_file):
    num_of_tiles = tiles_required_at_certain_zoom_level(
        num_of_tiles_to_start_with, zoom_lvl)
    print('[+]No.of tiles required => {}'.format(num_of_tiles))
    extent = get_tile_extent(zoom_lvl, (-180, +90), tile_width, tile_height,
                             degree_along_x, degree_along_y).get('{},{}'.format(x_val, y_val), [])
    print(extent)
    return True
    if(not extent):
        return False
    map_obj = Map(tile_width, tile_height,
                  '+proj=longlat +datum=WGS84 +no_defs ')
    format_style_sheet(style_sheet, 'layer1', 'Parameter', [
                       'name', 'extent'], 'something', 'tmp.xml')
    load_map(map_obj, 'tmp.xml')  # loads XML style sheet
    map_obj.zoom_to_box(Box2d(*extent))
    render_to_file(map_obj, output_file, 'png')
    # removes temporary XML file, which was generated from template XML
    unlink('tmp.xml')
    return True


def input_validator():
    # validates input, which was provided during invokation of function
    zoom_lvl, x_val, y_val, num_of_tiles_to_start_with, style_sheet, image_file = argv[1:]
    try:
        zoom_lvl = int(zoom_lvl)
        x_val = int(x_val)
        y_val = int(y_val)
        num_of_tiles_to_start_with = int(num_of_tiles_to_start_with)
    except ValueError as e:
        print('[!]Error : {}'.format(str(e)))
        return ()
    if(zoom_lvl < 0 or zoom_lvl > 10):
        print('[!]Zoom level value should be in range of 0 to 10')
        return ()
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
        return ()
    if(not exists(style_sheet) or not style_sheet.endswith('.xml')):
        print('[!]Style Sheet not available !\n')
        return ()
    return (zoom_lvl, x_val, y_val, num_of_tiles_to_start_with, style_sheet, image_file)


def main(tile_width, tile_height):
    if(len(argv) != 7):
        print('[+]Usage : ./{} zoom-level x-value y-value number-of-tiles-to-start-with style-sheet image-file-name\n\t[*] zoom-level = 0 to 10\n\t[*] number-of-tiles-to-start-with = 2^x , where x= 0,1,2,3 .... \n'.format(argv[0]))
        return
    try:
        # if some argument is not okay, it'll fail simply
        zoom_lvl, x_val, y_val, num_of_tiles_to_start_with, style_sheet, image_file = input_validator()
    except ValueError:
        return
    print('[+]Generating tile ({},{}) with zoom level {} ...'.format(x_val, y_val, zoom_lvl))
    if(not tile_generator(x_val, y_val, zoom_lvl, 360, 180, num_of_tiles_to_start_with, tile_width, tile_height, style_sheet, image_file)):
        print('[!]Illegal Tile extent value !')
    return


if __name__ == '__main__':
    run('clear')
    try:
        main(256, 144)
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
