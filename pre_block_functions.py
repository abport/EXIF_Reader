import os
import socket
import exifread
from geopy.geocoders import Nominatim
from GPSPhoto import gpsphoto
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

geolocator = Nominatim(user_agent="Amin-Exif")


EXTENSIONS = ('.jpg', '.jpeg', '.jpe', '.jp2', '.tiff', '.tif', '.gif', '.bmp', '.png', '.webp', '.cr2', '.nef', '.orf', '.sr2', '.srw', '.dng',
              '.rw2', '.raf', '.pef', '.arw')


def get_exifread(filename):
    with open(filename, 'rb') as f:
        tags = exifread.process_file(f)
    return tags


# Get the data from image file and return a dictionary
def gps_lat_long(filepath):
    data = gpsphoto.getGPSData(filepath)
    return (data['Latitude'], data['Longitude']) if data else None


def convert_gps_to_loc(latlong):
    location = geolocator.reverse(latlong)
    mytext = location.address
    return mytext


def walk_dir_onefolder(root_dir):
    file_list = []
    for file in os.listdir(root_dir):
        path = os.path.join(root_dir, file).lower()
        if os.path.isfile(path) and path.endswith(EXTENSIONS):
            file_list.append(path)
    return file_list


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size


def convert_bytes(size, unit=None):
    units = {'bytes': 0, 'KB': 1, 'MB': 2, 'GB': 3}
    size_in_bytes = int(size)
    unit = unit if unit in units else 'bytes'
    quotient, remainder = divmod(size_in_bytes, 1024)
    if quotient == 0:
        return f"{size_in_bytes} bytes"
    return f"{quotient}.{remainder // 100:02d} {unit}"


def test_connection():
    try:
        socket.create_connection(('google.com', 80))
        return True
    except socket.gaierror:
        return False
