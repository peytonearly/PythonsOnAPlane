from oled import oled_setup, display_plot
from read_gps import get_coords
from tracker import openskyAPICurrStatus, plotPlanes


def run():
    oled_setup()
    coords = get_coords()
    dictionary = openskyAPICurrStatus(coords.lat, coords.lon)
    coord_list = plotPlanes(coords.lat, coords.lon, dictionary)
    display_plot(coord_list)


if __name__ == '__main__':
    run()
