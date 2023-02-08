import ntpath
import webbrowser
# from tkinter import *
import tkinter
from tkinter import Tk, mainloop, END, Label, Button, Canvas, filedialog, Frame, StringVar, Listbox, Scrollbar, Entry, Text, WORD, Menu, LEFT
from PIL import Image, ImageTk

import aguibackend


def callback(url):
    webbrowser.open_new(url)


def alert_popup(title, message, path):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400  # popup window width
    h = 200  # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()


def aboutmsg():
    alert_popup("About EXIF Reader", "Version: 1.0", "Coded by: Amin Beheshti")


# Get file name from path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def list_images():
    delete_all_texboxes()

    window.call('wm', 'attributes', '.', '-topmost', True)
    files = filedialog.askopenfilename(multiple=True, title="Select File(s)", filetypes=(
        ("Image Files", "*.jpg *.jpeg *.png *.tiff *.heic *.cr2"), ("All Files", "*.*")))

    var = window.splitlist(files)
    filePaths = []
    for f in var:
        filePaths.append(f)

    for row in filePaths:
        row = row.lower()
        if (row.endswith('.jpg')) or (row.endswith('.png')) or (row.endswith('.jpeg')) or (row.endswith('.tiff')) or (
                row.endswith('.heic')) or (row.endswith('.cr2')):
            list1.insert(END, row)


def add_one_folder():
    folder_selected = filedialog.askdirectory()
    delete_all_texboxes()
    files = aguibackend.walk_dir_onefolder(folder_selected)

    list1.delete(0, END)
    var = window.splitlist(files)

    filePaths = []
    for f in var:
        filePaths.append(f)

    for row in filePaths:
        list1.insert(END, row)


def add_folder():
    folder_selected = filedialog.askdirectory()
    delete_all_texboxes()
    files = aguibackend.walk_dir(folder_selected)

    list1.delete(0, END)
    var = window.splitlist(files)

    filePaths = []
    for f in var:
        filePaths.append(f)

    for row in filePaths:
        list1.insert(END, row)


# Delete all textbox
def delete_all_texboxes():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
    e8.delete(0, END)
    e9.delete(0, END)
    e10.delete(0, END)
    e11.delete(0, END)
    e12.delete(0, END)
    lastmodified.delete(0, END)
    entry_software.delete(0, END)
    entry_hostcomputer.delete(0, END)
    entry_yposition.delete(0, END)
    entry_filesize.delete(0, END)
    e13.delete(0, END)
    e14.delete(0, END)
    e15.delete(0, END)
    e16.delete(0, END)
    e17.delete(0, END)
    e18.delete(0, END)
    e19.delete(0, END)
    entry_shsvalue.delete(0, END)
    e20.delete(0, END)
    entry_aperture.delete(0, END)
    e23.delete(0, END)
    e24.delete(0, END)
    e25.delete(0, END)
    entry_lightsource.delete(0, END)
    entry_brightness.delete(0, END)
    entry_whitebalance.delete(0, END)
    entry_focal.delete(0, END)
    entry_colorspace.delete(0, END)
    entry_lensmaker.delete(0, END)
    entry_lensmodel.delete(0, END)
    entry_lenspec.delete(0, END)
    entry_scenetype.delete(0, END)
    entry_scenecaptype.delete(0, END)
    entry_sensingmethod.delete(0, END)
    entry_exifver.delete(0, END)
    t1.delete('1.0', END)


def get_selected_row(event):
    global selected_tuple

    index = list1.curselection()
    selected_tuple = list1.get(index)

    if index:

        getting_imagefilesize = aguibackend.get_file_size(selected_tuple)
        imagefilesize = aguibackend.convert_bytes(getting_imagefilesize, "MB")

        st_row = selected_tuple.lower()
        render = ""
        heic_format = ""
        if (st_row.endswith('.jpg')) or (st_row.endswith('.png')) or (st_row.endswith('.jpeg')) or (
                st_row.endswith('.tiff')):
            # Preview The Selected Image
            load = Image.open(selected_tuple)
            load.thumbnail((247, 247))
            render = ImageTk.PhotoImage(load)
        elif st_row.endswith('.heic'):
            var.set("Preview Not Available!")
            heic_format = "High Efficiency Image File Format"
        elif st_row.endswith('.cr2'):
            var.set("Preview Not Available!")
            heic_format = "Canon Raw Version 2"

        labelimg.config(image=render)
        labelimg.image = render

        # Display File Name Under the Image
        filen = path_leaf(selected_tuple)

        img_exif_tags = aguibackend.get_exifread(selected_tuple)

        imgfnamexif = ""
        imgwidthexif = ""
        imgheightexif = ""
        imgtypexif = ""
        imgxres = ""
        imgyres = ""
        imgresu = ""
        imgorient = ""
        imgartist = ""
        imgcopyright = ""
        imgexifsoft = ""
        imgdateo = ""
        imgdated = ""
        imgexifhpc = ""
        yposition = ""
        scenetype = ""
        scenecaptype = ""
        sensingmethod = ""
        imgbrightness = ""
        imgexifver = ""
        brand = ""
        model = ""
        exposuretime = ""
        focallength = ""
        fstop = ""
        iso = ""
        shsvalue = ""
        imgaperture = ""
        imgcolorspace = ""
        lightsource = ""
        lensmaker = ""
        lensmodel = ""
        lenspec = ""
        flash = ""
        exp_bv = ""
        exp_prg = ""
        metering = ""
        whitebalance = ""
        datelastmodified = ""
        thumbnail_file_type = ""

        if not img_exif_tags:

            delete_all_texboxes()
            t1.insert(END, "No EXIF Data Detected")

        else:

            if img_exif_tags:
                try:
                    if 'EXIF ExifImageWidth' in img_exif_tags:
                        imgwidthexif = img_exif_tags['EXIF ExifImageWidth']
                except KeyError:
                    pass
                try:
                    if 'EXIF ExifImageLength' in img_exif_tags:
                        imgheightexif = img_exif_tags['EXIF ExifImageLength']
                except KeyError:
                    pass
                try:
                    if 'Image XResolution' in img_exif_tags:
                        imgxres = img_exif_tags['Image XResolution']
                except KeyError:
                    pass
                try:
                    if 'Image YResolution' in img_exif_tags:
                        imgyres = img_exif_tags['Image YResolution']
                except KeyError:
                    pass
                try:
                    if 'Image ResolutionUnit' in img_exif_tags:
                        imgresu = img_exif_tags['Image ResolutionUnit']
                except KeyError:
                    pass
                try:
                    if 'Image Orientation' in img_exif_tags:
                        imgorient = img_exif_tags['Image Orientation']
                except KeyError:
                    pass
                # checking if image is copyrighted
                try:
                    if 'Image Artist' in img_exif_tags:
                        imgartist = img_exif_tags['Image Artist']
                except KeyError:
                    pass
                try:
                    if 'Image Copyright' in img_exif_tags:
                        imgcopyright = img_exif_tags['Image Copyright']
                except KeyError:
                    pass
                try:
                    if 'Image Software' in img_exif_tags:
                        imgexifsoft = img_exif_tags['Image Software']
                except KeyError:
                    pass
                try:
                    if 'EXIF DateTimeOriginal' in img_exif_tags:
                        imgdateo = img_exif_tags['EXIF DateTimeOriginal']
                except KeyError:
                    pass
                try:
                    if 'EXIF DateTimeDigitized' in img_exif_tags:
                        imgdated = img_exif_tags['EXIF DateTimeDigitized']
                except KeyError:
                    pass

                try:
                    if 'Image HostComputer' in img_exif_tags:
                        imgexifhpc = img_exif_tags['Image HostComputer']
                except KeyError:
                    pass
                try:
                    if 'Image YCbCrPositioning' in img_exif_tags:
                        yposition = img_exif_tags['Image YCbCrPositioning']
                except KeyError:
                    pass
                try:
                    if 'Image Make' in img_exif_tags:
                        brand = img_exif_tags['Image Make']
                except KeyError:
                    pass
                try:
                    if 'Image Model' in img_exif_tags:
                        model = img_exif_tags['Image Model']
                except KeyError:
                    pass
                try:
                    if 'EXIF FNumber' in img_exif_tags:
                        fstop = img_exif_tags['EXIF FNumber']
                except KeyError:
                    pass
                try:
                    if 'EXIF ExposureTime' in img_exif_tags:
                        exposuretime = img_exif_tags['EXIF ExposureTime']
                except KeyError:
                    pass
                try:
                    if 'EXIF ShutterSpeedValue' in img_exif_tags:
                        shsvalue = img_exif_tags['EXIF ShutterSpeedValue']
                except KeyError:
                    pass
                try:
                    if 'EXIF ISOSpeedRatings' in img_exif_tags:
                        iso = img_exif_tags['EXIF ISOSpeedRatings']
                except KeyError:
                    pass
                try:
                    if 'EXIF ExposureBiasValue' in img_exif_tags:
                        exp_bv = img_exif_tags['EXIF ExposureBiasValue']
                except KeyError:
                    pass
                try:
                    if 'EXIF FocalLength' in img_exif_tags:
                        focallength = img_exif_tags['EXIF FocalLength']
                except KeyError:
                    pass
                try:
                    if 'EXIF LightSource' in img_exif_tags:
                        lightsource = img_exif_tags['EXIF LightSource']
                except KeyError:
                    pass
                try:
                    if 'EXIF ColorSpace' in img_exif_tags:
                        imgcolorspace = img_exif_tags['EXIF ColorSpace']
                except KeyError:
                    pass

                try:
                    if 'EXIF ApertureValue' in img_exif_tags:
                        imgaperture = img_exif_tags['EXIF ApertureValue']
                except KeyError:
                    pass
                try:
                    if 'EXIF MeteringMode' in img_exif_tags:
                        metering = img_exif_tags['EXIF MeteringMode']
                except KeyError:
                    pass
                try:
                    if 'EXIF SceneType' in img_exif_tags:
                        scenetype = img_exif_tags['EXIF SceneType']
                except KeyError:
                    pass
                try:
                    if 'EXIF SceneCaptureType' in img_exif_tags:
                        scenecaptype = img_exif_tags['EXIF SceneCaptureType']
                except KeyError:
                    pass
                try:
                    if 'EXIF SensingMethod' in img_exif_tags:
                        sensingmethod = img_exif_tags['EXIF SensingMethod']
                except KeyError:
                    pass
                try:
                    if 'EXIF Flash' in img_exif_tags:
                        flash = img_exif_tags['EXIF Flash']

                except KeyError:
                    pass
                try:
                    if 'EXIF LensMake' in img_exif_tags:
                        lensmaker = img_exif_tags['EXIF LensMake']
                except KeyError:
                    pass
                try:
                    if 'EXIF LensModel' in img_exif_tags:
                        lensmodel = img_exif_tags['EXIF LensModel']
                except KeyError:
                    pass
                try:
                    if 'EXIF LensSpecification' in img_exif_tags:
                        lenspec = img_exif_tags['EXIF LensSpecification']
                except KeyError:
                    pass
                try:
                    if 'EXIF WhiteBalance' in img_exif_tags:
                        whitebalance = img_exif_tags['EXIF WhiteBalance']
                except KeyError:
                    pass
                try:
                    if 'Image DateTime' in img_exif_tags:
                        datelastmodified = img_exif_tags['Image DateTime']
                except KeyError:
                    pass
                try:
                    if 'EXIF BrightnessValue' in img_exif_tags:
                        imgbrightness = img_exif_tags['EXIF BrightnessValue']
                except KeyError:
                    pass
                try:
                    if 'EXIF ExifVersion' in img_exif_tags:
                        imgexifver = img_exif_tags['EXIF ExifVersion']
                except KeyError:
                    pass
                try:
                    if 'EXIF ExposureProgram' in img_exif_tags:
                        exp_prg = img_exif_tags['EXIF ExposureProgram']
                except KeyError:
                    pass
                try:
                    if 'Thumbnail Compression' in img_exif_tags:
                        thumbnail_file_type = img_exif_tags['Thumbnail Compression']
                except KeyError:
                    pass
            delete_all_texboxes()

        e1.insert(END, filen)
        e2.insert(END, imgwidthexif)
        e3.insert(END, imgheightexif)

        if heic_format:
            e4.insert(END, heic_format)
        elif thumbnail_file_type:
            e4.insert(END, thumbnail_file_type)

        e5.insert(END, imgxres)
        e6.insert(END, imgyres)
        e7.insert(END, imgresu)
        e8.insert(END, imgorient)
        e9.insert(END, imgartist)
        e10.insert(END, imgcopyright)
        e11.insert(END, imgdateo)
        e12.insert(END, imgdated)
        lastmodified.insert(END, datelastmodified)
        entry_software.insert(END, imgexifsoft)
        entry_hostcomputer.insert(END, imgexifhpc)
        entry_yposition.insert(END, yposition)
        entry_filesize.insert(END, imagefilesize)

        e15.insert(END, brand)
        e16.insert(END, model)
        e17.insert(END, fstop)
        e19.insert(END, iso)
        e18.insert(END, exposuretime)
        entry_shsvalue.insert(END, shsvalue)
        e20.insert(END, exp_bv)
        entry_aperture.insert(END, imgaperture)
        e23.insert(END, metering)
        e24.insert(END, exp_prg)
        e25.insert(END, flash)
        entry_lightsource.insert(END, lightsource)
        entry_brightness.insert(END, imgbrightness)
        entry_whitebalance.insert(END, whitebalance)
        entry_focal.insert(END, focallength)
        entry_colorspace.insert(END, imgcolorspace)
        entry_lensmaker.insert(END, lensmaker)
        entry_lensmodel.insert(END, lensmodel)
        entry_lenspec.insert(END, lenspec)
        entry_scenetype.insert(END, scenetype)
        entry_scenecaptype.insert(END, scenecaptype)
        entry_sensingmethod.insert(END, sensingmethod)
        entry_exifver.insert(END, imgexifver)

        # Get Geo details (lat and long) and display in textbox
        img_lat_long = aguibackend.gps_lat_long(selected_tuple)
        e13.delete(0, END)
        e14.delete(0, END)

        if img_lat_long:
            e13.insert(END, img_lat_long[0])
            e14.insert(END, img_lat_long[1])
            t1.insert(END, "To Convert the GPS Coordinates to a Human Readable Location, Click the Button")


# Convert Lat and Long to Readable Address (Reverse Geocoding)
def gps2loc():
    img_lat_long = aguibackend.gps_lat_long(selected_tuple)
    if img_lat_long:
        t1.delete('1.0', END)
        if aguibackend.test_connection():
            location = aguibackend.convert_gps2loc(img_lat_long)

            if location:
                t1.insert(END, location)
        else:
            t1.insert(END, "Cannot Connect to The Internet!\nPlease Check your Internet Connection Settings...")


def open_in_browser():
    img_lat_long = aguibackend.gps_lat_long(selected_tuple)
    if img_lat_long:
        webbrowser.open('https://www.google.com/maps?q=' + str(img_lat_long[0]) + "," + str(img_lat_long[1]))


WIDTH = 900
HEIGHT = 700
# Starts here
window = Tk()
window.wm_title("EXIF Reader by Amin Beheshti")
# Set App icon  
window.iconbitmap(r'exif.ico')

canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

frame = Frame(window, bg='#113255')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

var = StringVar()
var.set("Image Preview")
labelimg = Label(frame, textvariable=var)
labelimg.place(relx=0.73, rely=0.003, relwidth=0.269, relheight=0.27)

list1 = Listbox(frame)
list1.place(relx=0.73, rely=0.274, relwidth=0.258, relheight=0.67)

# Link a scrollbar to the canvas
vsb = Scrollbar(frame, orient="vertical", command=list1.yview)
vsb.place(relx=0.988, rely=0.274, relheight=0.691, relwidth=0.012)
list1.configure(yscrollcommand=vsb.set)

hsb = Scrollbar(frame, orient="horizontal", command=list1.xview)
hsb.place(relx=0.73, rely=0.944, relheight=0.021, relwidth=0.258)
list1.configure(xscrollcommand=hsb.set)

list1.bind('<<ListboxSelect>>', get_selected_row)

statusbartext = StringVar()
statusbartext.set("Let's get connected on Instagram: @aminbeheshti_com")
satusbar = Label(frame, textvariable=statusbartext, bg="#0099df", anchor="w", justify=LEFT, fg="#ffffff",
                 cursor="hand2")
satusbar.place(relx=0, rely=0.965, relwidth=1, relheight=0.035)
satusbar.bind("<Button-1>", lambda e: callback("https://instagram.com/aminbeheshti_com/"))

labelimgname = StringVar()
labelimgname.set("File Name:")
labelwidth = Label(frame, textvariable=labelimgname, bg='#4ad295', anchor="w", justify=LEFT)
labelwidth.place(relx=0, rely=0.003, relwidth=0.15, relheight=0.033)

img_filename = StringVar()
e1 = Entry(frame, textvariable=img_filename)
e1.place(relx=0.15, rely=0.003, relwidth=0.2135, relheight=0.033)

image_file_size = StringVar()
image_file_size.set("File Size:")
image_filesize = Label(frame, textvariable=image_file_size, bg='#4ad295', anchor="w", justify=LEFT)
image_filesize.place(relx=0, rely=0.037, relwidth=0.15, relheight=0.033)

img_filesize = StringVar()
entry_filesize = Entry(frame, textvariable=img_filesize)
entry_filesize.place(relx=0.15, rely=0.037, relwidth=0.2135, relheight=0.033)

image_dateo_exif = StringVar()
image_dateo_exif.set("Date/Time Original:")
image_dateo = Label(frame, textvariable=image_dateo_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_dateo.place(relx=0, rely=0.071, relwidth=0.15, relheight=0.033)

img_dateo = StringVar()
e11 = Entry(frame, textvariable=img_dateo)
e11.place(relx=0.15, rely=0.071, relwidth=0.2135, relheight=0.033)

image_dated_exif = StringVar()
image_dated_exif.set("Date/Time Digitized:")
image_dated = Label(frame, textvariable=image_dated_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_dated.place(relx=0, rely=0.105, relwidth=0.15, relheight=0.033)

img_dated = StringVar()
e12 = Entry(frame, textvariable=img_dated)
e12.place(relx=0.15, rely=0.105, relwidth=0.2135, relheight=0.033)

image_lastmodified_exif = StringVar()
image_lastmodified_exif.set("Last Modified Date:")
image_lastmodified = Label(frame, textvariable=image_lastmodified_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_lastmodified.place(relx=0, rely=0.139, relwidth=0.15, relheight=0.033)

img_lastmodified = StringVar()
lastmodified = Entry(frame, textvariable=img_lastmodified)
lastmodified.place(relx=0.15, rely=0.139, relwidth=0.2135, relheight=0.033)

image_author_exif = StringVar()
image_author_exif.set("Author:")
image_author = Label(frame, textvariable=image_author_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_author.place(relx=0, rely=0.173, relwidth=0.15, relheight=0.033)

img_author = StringVar()
e9 = Entry(frame, textvariable=img_author)
e9.place(relx=0.15, rely=0.173, relwidth=0.2135, relheight=0.033)

image_copyright_exif = StringVar()
image_copyright_exif.set("Copyright:")
image_copyright = Label(frame, textvariable=image_copyright_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_copyright.place(relx=0, rely=0.207, relwidth=0.15, relheight=0.033)

img_copyright = StringVar()
e10 = Entry(frame, textvariable=img_copyright)
e10.place(relx=0.15, rely=0.207, relwidth=0.2135, relheight=0.033)

image_software_exif = StringVar()
image_software_exif.set("Software:")
image_software = Label(frame, textvariable=image_software_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_software.place(relx=0, rely=0.241, relwidth=0.15, relheight=0.033)

img_software = StringVar()
entry_software = Entry(frame, textvariable=img_software)
entry_software.place(relx=0.15, rely=0.241, relwidth=0.2135, relheight=0.033)

image_hpc_exif = StringVar()
image_hpc_exif.set("Host Computer:")
image_hpc = Label(frame, textvariable=image_hpc_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_hpc.place(relx=0, rely=0.275, relwidth=0.15, relheight=0.033)

img_hpc = StringVar()
entry_hostcomputer = Entry(frame, textvariable=img_hpc)
entry_hostcomputer.place(relx=0.15, rely=0.275, relwidth=0.2135, relheight=0.033)

image_type = StringVar()
image_type.set("Image Type:")
filetype = Label(frame, textvariable=image_type, bg='#4ad295', anchor="w", justify=LEFT)
filetype.place(relx=0.3655, rely=0.003, relwidth=0.15, relheight=0.033)

img_type = StringVar()
e4 = Entry(frame, textvariable=img_type)
e4.place(relx=0.5155, rely=0.003, relwidth=0.2135, relheight=0.033)

image_width = StringVar()
image_width.set("Image Width:")
labelwidth = Label(frame, textvariable=image_width, bg='#4ad295', anchor="w", justify=LEFT)
labelwidth.place(relx=0.3655, rely=0.037, relwidth=0.15, relheight=0.033)

img_width_exif = StringVar()
e2 = Entry(frame, textvariable=img_width_exif)
e2.place(relx=0.5155, rely=0.037, relwidth=0.2135, relheight=0.033)

image_height = StringVar()
image_height.set("Image Height:")
labelheight = Label(frame, textvariable=image_height, bg='#4ad295', anchor="w", justify=LEFT)
labelheight.place(relx=0.3655, rely=0.071, relwidth=0.15, relheight=0.033)

img_height_exif = StringVar()
e3 = Entry(frame, textvariable=img_height_exif)
e3.place(relx=0.5155, rely=0.071, relwidth=0.2135, relheight=0.033)

image_orient_exif = StringVar()
image_orient_exif.set("Orientation:")
image_orient = Label(frame, textvariable=image_orient_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_orient.place(relx=0.3655, rely=0.105, relwidth=0.15, relheight=0.033)

img_orient = StringVar()
e8 = Entry(frame, textvariable=img_orient)
e8.place(relx=0.5155, rely=0.105, relwidth=0.2135, relheight=0.033)

image_xres_exif = StringVar()
image_xres_exif.set("Horizontal Resolution:")
image_xres = Label(frame, textvariable=image_xres_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_xres.place(relx=0.3655, rely=0.139, relwidth=0.15, relheight=0.033)

img_xres = StringVar()
e5 = Entry(frame, textvariable=img_xres)
e5.place(relx=0.5155, rely=0.139, relwidth=0.2135, relheight=0.033)

image_yres_exif = StringVar()
image_yres_exif.set("Vertical Resolution:")
image_yres = Label(frame, textvariable=image_yres_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_yres.place(relx=0.3655, rely=0.173, relwidth=0.15, relheight=0.033)

img_yres = StringVar()
e6 = Entry(frame, textvariable=img_yres)
e6.place(relx=0.5155, rely=0.173, relwidth=0.2135, relheight=0.033)

image_resu_exif = StringVar()
image_resu_exif.set("Resolution Unit:")
image_resu = Label(frame, textvariable=image_resu_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_resu.place(relx=0.3655, rely=0.207, relwidth=0.15, relheight=0.033)

img_resunit = StringVar()
e7 = Entry(frame, textvariable=img_resunit)
e7.place(relx=0.5155, rely=0.207, relwidth=0.2135, relheight=0.033)

image_yposition = StringVar()
image_yposition.set("YCbCrPositioning:")
image_yposition = Label(frame, textvariable=image_yposition, bg='#4ad295', anchor="w", justify=LEFT)
image_yposition.place(relx=0.3655, rely=0.241, relwidth=0.15, relheight=0.033)

img_yposition = StringVar()
entry_yposition = Entry(frame, textvariable=img_yposition)
entry_yposition.place(relx=0.5155, rely=0.241, relwidth=0.2135, relheight=0.033)

camera_exifver = StringVar()
camera_exifver.set("EXIF Version:")
cam_exifver = Label(frame, textvariable=camera_exifver, bg='#4ad295', anchor="w", justify=LEFT)
cam_exifver.place(relx=0.3655, rely=0.275, relwidth=0.15, relheight=0.033)

img_exifver = StringVar()
entry_exifver = Entry(frame, textvariable=img_exifver)
entry_exifver.place(relx=0.5155, rely=0.275, relwidth=0.2135, relheight=0.033)

# ----------------------------------------------------------------------------------------------
camera_exif = StringVar()
camera_exif.set("Camera:")
cam_exif = Label(frame, textvariable=camera_exif, bg="#113255", fg="#ffffff", anchor="w", justify=LEFT)
cam_exif.place(relx=0, rely=0.309, relwidth=0.15, relheight=0.033)

camera_maker = StringVar()
camera_maker.set("Camera Maker:")
cam_maker = Label(frame, textvariable=camera_maker, bg='#4ad295', anchor="w", justify=LEFT)
cam_maker.place(relx=0, rely=0.343, relwidth=0.15, relheight=0.033)

img_maker = StringVar()
e15 = Entry(frame, textvariable=img_maker)
e15.place(relx=0.15, rely=0.343, relwidth=0.2135, relheight=0.033)

camera_model = StringVar()
camera_model.set("Camera Model:")
cam_model = Label(frame, textvariable=camera_model, bg='#4ad295', anchor="w", justify=LEFT)
cam_model.place(relx=0, rely=0.377, relwidth=0.15, relheight=0.033)

img_model = StringVar()
e16 = Entry(frame, textvariable=img_model)
e16.place(relx=0.15, rely=0.377, relwidth=0.2135, relheight=0.033)

camera_lensmaker = StringVar()
camera_lensmaker.set("Lens Maker:")
cam_lensmaker = Label(frame, textvariable=camera_lensmaker, bg='#4ad295', anchor="w", justify=LEFT)
cam_lensmaker.place(relx=0, rely=0.411, relwidth=0.15, relheight=0.033)

img_lensmaker = StringVar()
entry_lensmaker = Entry(frame, textvariable=img_lensmaker)
entry_lensmaker.place(relx=0.15, rely=0.411, relwidth=0.2135, relheight=0.033)

camera_lensmodel = StringVar()
camera_lensmodel.set("Lens Model:")
cam_lensmodel = Label(frame, textvariable=camera_lensmodel, bg='#4ad295', anchor="w", justify=LEFT)
cam_lensmodel.place(relx=0, rely=0.445, relwidth=0.15, relheight=0.033)

img_lensmodel = StringVar()
entry_lensmodel = Entry(frame, textvariable=img_lensmodel)
entry_lensmodel.place(relx=0.15, rely=0.445, relwidth=0.2135, relheight=0.033)

camera_lenspec = StringVar()
camera_lenspec.set("Lens Specification:")
cam_lenspec = Label(frame, textvariable=camera_lenspec, bg='#4ad295', anchor="w", justify=LEFT)
cam_lenspec.place(relx=0, rely=0.479, relwidth=0.15, relheight=0.033)

img_lenspec = StringVar()
entry_lenspec = Entry(frame, textvariable=img_lenspec)
entry_lenspec.place(relx=0.15, rely=0.479, relwidth=0.2135, relheight=0.033)

camera_focal = StringVar()
camera_focal.set("Focal Length:")
cam_focal = Label(frame, textvariable=camera_focal, bg='#4ad295', anchor="w", justify=LEFT)
cam_focal.place(relx=0, rely=0.513, relwidth=0.15, relheight=0.033)

img_focal = StringVar()
entry_focal = Entry(frame, textvariable=img_focal)
entry_focal.place(relx=0.15, rely=0.513, relwidth=0.2135, relheight=0.033)

camera_flash = StringVar()
camera_flash.set("Flash:")
cam_flash = Label(frame, textvariable=camera_flash, bg='#4ad295', anchor="w", justify=LEFT)
cam_flash.place(relx=0, rely=0.547, relwidth=0.15, relheight=0.033)

img_flash = StringVar()
e25 = Entry(frame, textvariable=img_flash)
e25.place(relx=0.15, rely=0.547, relwidth=0.2135, relheight=0.033)

camera_lightsource = StringVar()
camera_lightsource.set("Light Source:")
cam_lightsource = Label(frame, textvariable=camera_lightsource, bg='#4ad295', anchor="w", justify=LEFT)
cam_lightsource.place(relx=0, rely=0.581, relwidth=0.15, relheight=0.033)

img_lightsource = StringVar()
entry_lightsource = Entry(frame, textvariable=img_lightsource)
entry_lightsource.place(relx=0.15, rely=0.581, relwidth=0.2135, relheight=0.033)

camera_brightness = StringVar()
camera_brightness.set("Brightness:")
cam_brightness = Label(frame, textvariable=camera_brightness, bg='#4ad295', anchor="w", justify=LEFT)
cam_brightness.place(relx=0, rely=0.615, relwidth=0.15, relheight=0.033)

img_whitebalance = StringVar()
entry_brightness = Entry(frame, textvariable=img_whitebalance)
entry_brightness.place(relx=0.15, rely=0.615, relwidth=0.2135, relheight=0.033)

camera_whitebalance = StringVar()
camera_whitebalance.set("White Balance:")
cam_whitebalance = Label(frame, textvariable=camera_whitebalance, bg='#4ad295', anchor="w", justify=LEFT)
cam_whitebalance.place(relx=0, rely=0.649, relwidth=0.15, relheight=0.033)

img_whitebalance = StringVar()
entry_whitebalance = Entry(frame, textvariable=img_whitebalance)
entry_whitebalance.place(relx=0.15, rely=0.649, relwidth=0.2135, relheight=0.033)

camera_colorspace = StringVar()
camera_colorspace.set("Color Space:")
cam_colorspace = Label(frame, textvariable=camera_colorspace, bg='#4ad295', anchor="w", justify=LEFT)
cam_colorspace.place(relx=0, rely=0.683, relwidth=0.15, relheight=0.033)

img_colorspace = StringVar()
entry_colorspace = Entry(frame, textvariable=img_colorspace)
entry_colorspace.place(relx=0.15, rely=0.683, relwidth=0.2135, relheight=0.033)
# ----------------------------------------------------------------------------------------------
camera_fstop = StringVar()
camera_fstop.set("F-Stop (F-Number):")
cam_fstop = Label(frame, textvariable=camera_fstop, bg='#4ad295', anchor="w", justify=LEFT)
cam_fstop.place(relx=0.3655, rely=0.343, relwidth=0.15, relheight=0.033)

img_fstop = StringVar()
e17 = Entry(frame, textvariable=img_fstop)
e17.place(relx=0.5155, rely=0.343, relwidth=0.2135, relheight=0.033)

camera_iso = StringVar()
camera_iso.set("ISO Speed:")
cam_iso_speed = Label(frame, textvariable=camera_iso, bg='#4ad295', anchor="w", justify=LEFT)
cam_iso_speed.place(relx=0.3655, rely=0.377, relwidth=0.15, relheight=0.033)

img_iso_speed = StringVar()
e19 = Entry(frame, textvariable=img_iso_speed)
e19.place(relx=0.5155, rely=0.377, relwidth=0.2135, relheight=0.033)

camera_exptime = StringVar()
camera_exptime.set("Exposure Time:")
cam_exptime = Label(frame, textvariable=camera_exptime, bg='#4ad295', anchor="w", justify=LEFT)
cam_exptime.place(relx=0.3655, rely=0.411, relwidth=0.15, relheight=0.033)

img_exptime = StringVar()
e18 = Entry(frame, textvariable=img_exptime)
e18.place(relx=0.5155, rely=0.411, relwidth=0.2135, relheight=0.033)

camera_expbias = StringVar()
camera_expbias.set("Exposure Bias:")
cam_expbias = Label(frame, textvariable=camera_expbias, bg='#4ad295', anchor="w", justify=LEFT)
cam_expbias.place(relx=0.3655, rely=0.445, relwidth=0.15, relheight=0.033)

img_expbias = StringVar()
e20 = Entry(frame, textvariable=img_expbias)
e20.place(relx=0.5155, rely=0.445, relwidth=0.2135, relheight=0.033)

camera_expro = StringVar()
camera_expro.set("Exposure Program:")
cam_expro = Label(frame, textvariable=camera_expro, bg='#4ad295', anchor="w", justify=LEFT)
cam_expro.place(relx=0.3655, rely=0.479, relwidth=0.15, relheight=0.033)

img_expro = StringVar()
e24 = Entry(frame, textvariable=img_expro)
e24.place(relx=0.5155, rely=0.479, relwidth=0.2135, relheight=0.033)

camera_shsvalue = StringVar()
camera_shsvalue.set("Shutter Speed Value:")
cam_shsvalue = Label(frame, textvariable=camera_shsvalue, bg='#4ad295', anchor="w", justify=LEFT)
cam_shsvalue.place(relx=0.3655, rely=0.513, relwidth=0.15, relheight=0.033)

img_shsvalue = StringVar()
entry_shsvalue = Entry(frame, textvariable=img_shsvalue)
entry_shsvalue.place(relx=0.5155, rely=0.513, relwidth=0.2135, relheight=0.033)

camera_aperture = StringVar()
camera_aperture.set("Aperture:")
cam_aperture = Label(frame, textvariable=camera_aperture, bg='#4ad295', anchor="w", justify=LEFT)
cam_aperture.place(relx=0.3655, rely=0.547, relwidth=0.15, relheight=0.033)

img_aperture = StringVar()
entry_aperture = Entry(frame, textvariable=img_aperture)
entry_aperture.place(relx=0.5155, rely=0.547, relwidth=0.2135, relheight=0.033)

camera_metering = StringVar()
camera_metering.set("Metering Mode:")
cam_metering = Label(frame, textvariable=camera_metering, bg='#4ad295', anchor="w", justify=LEFT)
cam_metering.place(relx=0.3655, rely=0.581, relwidth=0.15, relheight=0.033)

img_metering = StringVar()
e23 = Entry(frame, textvariable=img_metering)
e23.place(relx=0.5155, rely=0.581, relwidth=0.2135, relheight=0.033)

camera_scenetype = StringVar()
camera_scenetype.set("Scene Type:")
cam_scenetype = Label(frame, textvariable=camera_scenetype, bg='#4ad295', anchor="w", justify=LEFT)
cam_scenetype.place(relx=0.3655, rely=0.615, relwidth=0.15, relheight=0.033)

img_scenetype = StringVar()
entry_scenetype = Entry(frame, textvariable=img_scenetype)
entry_scenetype.place(relx=0.5155, rely=0.615, relwidth=0.2135, relheight=0.033)

camera_scenecaptype = StringVar()
camera_scenecaptype.set("Scene Capture Type:")
cam_scenecaptype = Label(frame, textvariable=camera_scenecaptype, bg='#4ad295', anchor="w", justify=LEFT)
cam_scenecaptype.place(relx=0.3655, rely=0.649, relwidth=0.15, relheight=0.033)

img_scenecaptype = StringVar()
entry_scenecaptype = Entry(frame, textvariable=img_scenecaptype)
entry_scenecaptype.place(relx=0.5155, rely=0.649, relwidth=0.2135, relheight=0.033)

camera_sensingmethod = StringVar()
camera_sensingmethod.set("Sensing Method:")
cam_sensingmethod = Label(frame, textvariable=camera_sensingmethod, bg='#4ad295', anchor="w", justify=LEFT)
cam_sensingmethod.place(relx=0.3655, rely=0.683, relwidth=0.15, relheight=0.033)

img_sensingmethod = StringVar()
entry_sensingmethod = Entry(frame, textvariable=img_sensingmethod)
entry_sensingmethod.place(relx=0.5155, rely=0.683, relwidth=0.2135, relheight=0.033)

# ---------------------------------------------------------------------------------------
image_gps_exif = StringVar()
image_gps_exif.set("GPS Info:")
image_gps = Label(frame, textvariable=image_gps_exif, bg="#113255", fg="#ffffff", anchor="w", justify=LEFT)
image_gps.place(relx=0, rely=0.717, relwidth=0.15, relheight=0.033)

image_lat_exif = StringVar()
image_lat_exif.set("Latitute:")
image_lat = Label(frame, textvariable=image_lat_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_lat.place(relx=0, rely=0.751, relwidth=0.15, relheight=0.033)

img_lat = StringVar()
e13 = Entry(frame, textvariable=img_lat)
e13.place(relx=0.15, rely=0.751, relwidth=0.2135, relheight=0.033)

b1 = Button(frame, text="Show on Map", bg="#1273eb", fg="#FFFFFF", command=open_in_browser)
b1.place(relx=0.001, rely=0.785, relwidth=0.3625, relheight=0.037)

image_long_exif = StringVar()
image_long_exif.set("Longitude:")
image_long = Label(frame, textvariable=image_long_exif, bg='#4ad295', anchor="w", justify=LEFT)
image_long.place(relx=0.3655, rely=0.751, relwidth=0.15, relheight=0.033)

img_long = StringVar()
e14 = Entry(frame, textvariable=img_long)
e14.place(relx=0.5155, rely=0.751, relwidth=0.2135, relheight=0.033)

b2 = Button(frame, text="Readable Address", bg="#ffb229", fg="#113255", command=gps2loc)
b2.place(relx=0.3655, rely=0.785, relwidth=0.3635, relheight=0.037)

t1 = Text(frame, wrap=WORD, bg="#113255", fg="#ffffff", bd=0)
t1.place(relx=0, rely=0.822, relwidth=0.729, relheight=0.141)

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add Photo(s)", command=list_images)
filemenu.add_command(label="Add a Folder", command=add_one_folder)
filemenu.add_command(label="Add Folder (+Sub Folders)", command=add_folder)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=aboutmsg)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)
window.mainloop()
# Ends here
