from ublox_gps import UbloxGps
import serial

port = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
gps = UbloxGps(port)


def get_coords():
    coords = gps.geo_coords()
    return coords


if __name__ == '__main__':
    coords = get_coords()
    print(coords.lat, coords.lon)
