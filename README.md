# 📸 EXIF Reader

Welcome to EXIF Reader, your new best friend for peeking behind the curtain of your digital images.

## 🚀 What's This All About?

EXIF Reader is a snazzy Python app that lets you dive deep into the hidden data of your photos. Ever wondered where that vacation snap was taken? Or what camera settings you used for that perfect sunset shot? EXIF Reader's got your back!

## 👀 App Preview

Here's a sneak peek of what EXIF Reader looks like in action:

![EXIF Reader Screenshot](https://github.com/abport/EXIF_Reader/blob/main/exif_reader_amin_beheshti.png)

## ✨ Features

- 🖼️ **Image Preview**: See your photo right in the app.
- 📂 **Batch Processing**: Add multiple photos or entire folders at once.
- 🗺️ **GPS Data**: View coordinates and even see the location on a map.
- 🏙️ **Reverse Geocoding**: Turn those mysterious coordinates into actual addresses.
- 🧹 **EXIF Removal**: Want to keep your photo info private? Wipe that EXIF data clean!

## 📸 Supported Image Formats

EXIF Reader supports a wide range of image formats, including:

- JPEG (.jpg, .jpeg, .jpe)
- JPEG 2000 (.jp2)
- TIFF (.tiff, .tif)
- GIF (.gif)
- BMP (.bmp)
- PNG (.png)
- WebP (.webp)
- Various RAW formats:
  - Canon (.cr2)
  - Nikon (.nef)
  - Olympus (.orf)
  - Sony (.sr2, .arw)
  - Samsung (.srw)
  - Adobe Digital Negative (.dng)
  - Panasonic (.rw2)
  - Fujifilm (.raf)
  - Pentax (.pef)

## 🛠️ Installation

1. Clone this repo:
   ```
   git clone https://github.com/abport/exif-reader.git
   ```
2. Navigate to the project directory:
   ```
   cd exif-reader
   ```
3. Install the required packages:
   ```
   pip install Pillow exifread geopy GPSPhoto piexif
   ```
4. Run the app:
   ```
   python exif_reader.py
   ```

Note: Make sure you have Python and pip installed on your system before running these commands.

## 🎮 How to Use

1. Launch the app and use the "File" menu to add photos or folders.
2. Click on a photo in the list to view its EXIF data.
3. Use the buttons at the bottom to:
   - Show the photo location on a map
   - Get a human-readable address for the GPS coordinates
   - Remove all EXIF data (use with caution!)

## 🤝 Contributing

Got ideas to make EXIF Reader even cooler? We're all ears! Feel free to fork the repo, make your changes, and send us a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Shoutout to the awesome `exifread`, `geopy`, and `piexif` libraries!
- Thanks to all the open-source contributors who make projects like this possible.

## 🐛 Found a Bug?

If you've spotted a bug or have a feature request, please open an issue. We appreciate your feedback!

Happy EXIF reading! 📸✨
