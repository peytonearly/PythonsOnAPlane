#%%
import requests
import json
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from PIL import Image

'''
Function Definitions
'''

# Function for taking in user inputs for latitude and longitude (unused currently)
def LatLonInput():
    lat = False
    lon = False

    # Make sure inputs are within proper range
    while not lat:
        try:
            tempLat = float(input("Enter your latitude: "))  # Gather latitude
        except ValueError: # If user doesn't input a number catch the fault and have them try again
            print("ERROR: Latitude must be a numerical value between -90 and 90 degrees. ")
            continue
        if tempLat < -90 or tempLat > 90:
            # Check that input is within latitude range
            print("ERROR: Latitude must be a numerical value between -90 and 90 degrees. ")
        else:
            # If input passes all checks, assign input to latitude var
            lat = tempLat

    while not lon:
        try:
            tempLon = float(input("Enter your longitude: ")) # Gather longitude
        except ValueError: # If user doesn't input a number catch the fault and have them try again
            print("ERROR: Longitude must be a numerical value between -180 and 180 degrees. ")
            continue
        if tempLon < -180 or tempLon > 180:
            # Check that input is within longitude range
            print("ERROR: Longitude must be a numerical value between -180 and 180 degrees. ")
        else:
            # If input passes all checks, assign input to longitude var 
            lon = tempLon

    # print(lat, lon) # Print collected values to make sure they are being collected properly
    return lat, lon

# Function for finding IATA code from latitude and longitude
def getIATA(lat, lon):
    url = "http://iatageo.com/getCode/" + str(lat) + "/" + str(lon)
    req = requests.get(url)
    return json.dumps(req.json(), sort_keys=True)

# Function for converting distance in miles to latitudinal equivalence
def changeM2Lat(M):
    R = 3960 # Radius of the earth
    rad2deg = 180/math.pi
    return (M/R)*rad2deg

# Function for converting distance in miles to longitudinal equivalence
def changeM2Lon(lat, M):
    R = 3960 # Radius of the earth
    deg2rad = math.pi/180
    rad2deg = 180/math.pi
    r = R*math.cos(lat*deg2rad)
    return (M/r)*rad2deg

def openskyAPICurrStatus(lat, lon):
    # Test lat and lon of Boulder, CO
    lat = 40.016869
    lon = -105.279617
    
    # Test lat and lon of LAX
    # lat = 33.9416
    # lon = -118.4085

    M = 25 # Preset search distance to 25 miles
    # Find minimum and maximum latitude and longitude given M value
    minLat = lat-changeM2Lat(M)
    minLon = lon-changeM2Lon((lat + changeM2Lat(M)) if lat > 0 else (lat-changeM2Lat(M)), M)
    maxLat = lat+changeM2Lat(M)
    maxLon = lon+changeM2Lon((lat + changeM2Lat(M)) if lat > 0 else (lat-changeM2Lat(M)), M)

    # Request parameters for OpenSky api
    request_parameters = {
        "lamin": str(minLat),
        "lomin": str(minLon),
        "lamax": str(maxLat),
        "lomax": str(maxLon)
    }
    url = "https://opensky-network.org/api/states/all"
    req = requests.get(url, params=request_parameters) # Access api

    plane_library = json.loads(req.text)

    # Export returned api data as json file
    with open("opensky.json", "w") as outfile:
        json.dump(plane_library, outfile)
    
    return plane_library

# Function for exporting returned api data to be used in Raspberry Pi
def screenOut(baseLat, baseLon, lat, lon):
    # Test lat and lon of Boulder, CO
    lat = 40.016869
    lon = -105.279617
    
    # Test lat and lon of LAX
    # lat = 33.9416
    # lon = -118.4085

    M = 25 # Preset search distance to 25 miles
    # Find minimum and maximum latitude and longitude given M value
    minLat = baseLat-changeM2Lat(M)
    maxLat = baseLat+changeM2Lat(M)
    minLon = baseLon-changeM2Lon((baseLat + changeM2Lat(M)) if baseLat > 0 else (baseLat-changeM2Lat(M)), M)
    maxLon = baseLon+changeM2Lon((baseLat + changeM2Lat(M)) if baseLat > 0 else (baseLat-changeM2Lat(M)), M)

    # Pre-allocate modified latitude and longitude vectors
    modLat = []
    modLon = []

    # Normalize latitude and longitude values to fit in 64x48 pixel Raspberry Pi OLED
    for i in lat:
        # Latitude array
        modLat.append(int(48 * ((i-minLat)/(maxLat-minLat))))
    for i in lon:
        # Longitude array
        modLon.append(int(64 * ((i-minLon)/(maxLon-minLon))))
    
    # Arrange modified data into latitude, longitude pairs
    out = []
    for i in range(len(lat)):
        out.append([modLat[i], modLon[i]])
    
    # Export data for use in Raspberry Pi
    f = open("rpdata.txt", "w")
    f.write(str(out))
    f.close()
    return out

# Function for plotting planes 
def plotPlanes(lat, lon, dictionary):
    # Test lat and lon of Boulder, CO
    lat = 40.016869
    lon = -105.279617
    
    # Test lat and lon of LAX
    # lat = 33.9416
    # lon = -118.4085

    M = 25 # Preset search distance to 25 miles
    # Find minimum and maximum latitude and longitude given M value
    minLat = lat-changeM2Lat(M)
    minLon = lon-changeM2Lon((lat + changeM2Lat(M)) if lat > 0 else (lat-changeM2Lat(M)), M)
    maxLat = lat+changeM2Lat(M)
    maxLon = lon+changeM2Lon((lat + changeM2Lat(M)) if lat > 0 else (lat-changeM2Lat(M)), M)

    latCoords = []
    lonCoords = []
    altitude = []
    trueTrack = []

    # Select active flights from returned data
    for x in dictionary["states"]:
        if x[7]:
            latCoords.append(float(x[6]))
            lonCoords.append(float(x[5]))
            altitude.append(float(x[7]))
            trueTrack.append(float(x[10] if x[10] else 0))

    # Call screenOut function
    out = screenOut(lat, lon, latCoords, lonCoords)

    # Determine output figure size
    BBox = [minLon, maxLon, minLat, maxLat]
    fig, ax = plt.subplots(figsize = (8,7))

    for x in range(len(lonCoords)):
        ax.scatter(lonCoords[x], latCoords[x], zorder = 1, alpha = 1, s = 50, c = '#000000', marker = (3, 0 , trueTrack[x]))
    
    ax.scatter(lon, lat, s = 20, c = '#FF0000', marker = "o")

    ax.scatter(lon, lat, s = 1000, edgecolors = '#0000FF', marker = "o", facecolors = 'none')
    ax.scatter(lon, lat, s = 10000, edgecolors = '#0000FF', marker = "o", facecolors = 'none')
    ax.scatter(lon, lat, s = 45000, edgecolors = '#0000FF', marker = "o", facecolors = 'none')
    ax.scatter(lon, lat, s = 100000, edgecolors = '#0000FF', marker = "o", facecolors = 'none')
    ax.scatter(lon, lat, s = 190000, edgecolors = '#0000FF', marker = "o", facecolors = 'none')

    ax.set_title('Planes Above Me')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])  

    plt.savefig('planesPlot.png')
    plt.show()
    return out

'''
Main Function
'''

if __name__ == '__main__':
    dictionary = openskyAPICurrStatus(0,0)
    plotPlanes(0, 0, dictionary)
