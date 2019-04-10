#!/usr/bin/python3


def tiles_required_at_certain_zoom_level(tiles_at_zoomed_out_condition, zoom_level):
    # returns number of tiles required to cover world at a certain zoom level
    return tiles_at_zoomed_out_condition*((2**2)**zoom_level)


def units_per_pixel(degrees, pixels, zoom_lvl):
    # how many degrees per pixel at a certain zoom level
    return (degrees/pixels)/(2**zoom_lvl)


def generate_next_tiles_along_x(start_at, x_extent, y_extent, x_index, y_index, tiles_with_index):
    # generates all tiles along X axis and stores them in a dictionary
    while(1):
        if(start_at[0] >= 180):
            break
        # extent of a tile
        value = [start_at, (start_at[0] + x_extent, start_at[1] - y_extent)]
        tiles_with_index.update({'{},{}'.format(x_index, y_index): [
                                value[0][0], value[1][1], value[1][0], value[0][1]]})
        x_index += 1
        # increasing value of longitude, because we're generating here tiles along X axis.
        start_at = (start_at[0]+x_extent, start_at[1])
    return [0, y_index+1]  # next tile's row-column id.


# generates a single tile only
def generate_next_tile_along_y(start_at, x_extent, y_extent, x_index, y_index, tiles_with_index):
    # holds extent of the tile which we're currently generating
    value = [start_at, (start_at[0] + x_extent, start_at[1] - y_extent)]
    tiles_with_index.update({'{},{}'.format(x_index, y_index): [
                            value[0][0], value[1][1], value[1][0], value[0][1]]})  # stores tiles in dictionary
    # returns where to start next along X and along Y respectively
    return [(start_at[0]+x_extent, start_at[1]), (start_at[0], start_at[1]-y_extent)]


def get_tile_extent(zoom_lvl, start_at, tile_width, tile_height, degree_along_x, degree_along_y):
    # extent along X axis for each tile
    x_extent = units_per_pixel(degree_along_x, tile_width, zoom_lvl)*tile_width
    y_extent = units_per_pixel(
        degree_along_y, tile_height, zoom_lvl)*tile_height  # extent along Y axis for each tile
    x_index, y_index = 0, 0
    tiles_with_index = {}
    while(1):
        next_start_point_along_x, start_at = generate_next_tile_along_y(
            start_at, x_extent, y_extent, x_index, y_index, tiles_with_index)
        x_index, y_index = generate_next_tiles_along_x(
            next_start_point_along_x, x_extent, y_extent, x_index+1, y_index, tiles_with_index)  # next tiles row and column id, returned from this function call
        if(start_at[1] <= -90):
            break
    # returns a dictionary holding row-column id as key and corresponding tile extent as value.
    return tiles_with_index


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler :)')
    exit(0)
