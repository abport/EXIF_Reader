import os
import os.path
import os.path
import socket
import exifread
from geopy.geocoders import Nominatim
# importing required modules
from GPSPhoto import gpsphoto
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_exifread(filename):
    f = open(filename, 'rb')
    tags = exifread.process_file(f, details=False)
    return tags


# Get the data from image file and return a dictionary
def gps_lat_long(filepath):
    data = gpsphoto.getGPSData(filepath)
    pp = []
    if data:
        pp = (data['Latitude'], data['Longitude'])
    return pp


def convert_gps2loc(latlong):
    geolocator = Nominatim(user_agent="Amin-Exif")
    location = geolocator.reverse(latlong)
    mytext = location.address
    return mytext


def walk_dir_onefolder(root_dir):
    """
    walks the specified directory root and all its subdirectories
    and returns a list containing all files with the extensions
    """
    file_list = []
    dir_list = [root_dir]
    root_dir = dir_list.pop()
    for path in os.listdir(root_dir):
        path = os.path.join(root_dir, path).lower()
        if os.path.isfile(path) and (
                path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg') or path.endswith(
            '.tiff') or path.endswith('.heic') or path.endswith('.cr2')):
            file_list.append(path)
        elif os.path.isdir(path):
            dir_list.append(path)
    return file_list


def walk_dir(root_dir):
    """
    walks the specified directory root and all its subdirectories
    and returns a list containing all files with the extensions
    """
    file_list = []
    towalk = [root_dir]
    while towalk:
        root_dir = towalk.pop()
        for path in os.listdir(root_dir):
            path = os.path.join(root_dir, path).lower()
            if os.path.isfile(path) and (
                    path.endswith('.jpg') or path.endswith('.png') or path.endswith('.jpeg') or path.endswith(
                '.tiff') or path.endswith('.heic') or path.endswith('.cr2')):
                file_list.append(path)
            elif os.path.isdir(path):
                towalk.append(path)
    return file_list


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size


def convert_bytes(size, unit=None):
    if unit == "KB":
        the_file_size = (str(round(size / 1024, 3)) + ' Kilobytes')
        return the_file_size
    elif unit == "MB":
        the_file_size = (str(round(size / (1024 * 1024), 3)) + ' Megabytes')
        return the_file_size
    elif unit == "GB":
        the_file_size = (str(round(size / (1024 * 1024 * 1024), 3)) + ' Gigabytes')
        return the_file_size
    else:
        the_file_size = (str(size) + ' bytes')
        return the_file_size


def test_connection():
    try:
        socket.create_connection(('google.com', 80))
        return True
    except OSError:
        return False
