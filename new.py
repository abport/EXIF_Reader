import os
import argparse
from exif import Image

def get_exif_data(image_path):
    try:
        with Image.open(image_path) as image:
            exif_data = image.get_exif()
            return exif_data
    except FileNotFoundError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {e}"

def parse_args():
    parser = argparse.ArgumentParser(description="Get EXIF data from an image file")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    image_path = args.image_path
    verbose = args.verbose

    exif_data = get_exif_data(image_path)
    if isinstance(exif_data, dict):
        for key, value in exif_data.items():
            if verbose:
                print(f"{key}: {value}")
            else:
                print(f"{key}: {value.printable}")
    else:
        print(exif_data)
