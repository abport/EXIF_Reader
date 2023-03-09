import os
import ntpath
import webbrowser
from tkinter import Tk, mainloop, END, Label, Button, Canvas, filedialog, Frame, StringVar, Listbox, Scrollbar, Entry, Text, WORD, Menu, LEFT, Toplevel, messagebox
from PIL import Image, ImageTk

import pre_block_functions


def callback(url):
    webbrowser.open_new(url)


def alert_popup(title, message, link):
    """Generate a pop-up window for the about section."""
    popup = Toplevel()
    popup.title(title)
    w = 400  # popup window width
    h = 200  # popup window height
    sw = popup.winfo_screenwidth()
    sh = popup.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n\n'
    m += "Looking to reach out and connect?\nHead over to my website!"
    w = Label(popup, text=m, width=120, height=7)
    w.pack()
    link_label = Label(popup, text=link, fg="blue", cursor="hand2")
    link_label.pack()
    link_label.bind("<Button-1>", lambda event: webbrowser.open(link))
    b = Button(popup, text="OK", command=popup.destroy, width=10)
    b.pack()


def aboutmsg():
    alert_popup("About EXIF Reader",
                "Version: 1.0\n\nCoded by: Amin Beheshti",
                "https://www.aminbeheshti.com\n")


# Get file name from path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# Delete all textbox
def delete_all_texboxes():
    if not list1.curselection():
        return
    t1.delete('1.0', END)
    t2.delete('1.0', END)


def list_images():
    delete_all_texboxes()

    window.call('wm', 'attributes', '.', '-topmost', True)
    files = filedialog.askopenfilename(multiple=True, title="Select File(s)", filetypes=(
        ("Image Files", "*.jpg *.jpeg *.jpe *.jp2 *.tiff *.tif *.gif *.bmp *.png *.webp *.cr2 *.nef *.orf *.sr2 *.srw *.dng *.rw2 *.raf *.pef *.arw"), ("All Files", "*.*")))

    filePaths = list(files)

    valid_extensions = ['.jpg', '.jpeg', '.jpe', '.jp2', '.tiff', '.tif', '.gif', '.bmp', '.png',
                        '.webp', '.cr2', '.nef', '.orf', '.sr2', '.srw', '.dng', '.rw2', '.raf', '.pef', '.arw']

    list1.delete(0, END)
    for row in filePaths:
        _, ext = os.path.splitext(row)
        if ext.lower() in valid_extensions:
            list1.insert(END, row)


def add_one_folder():
    folder_selected = filedialog.askdirectory()
    delete_all_texboxes()
    files = pre_block_functions.walk_dir_onefolder(folder_selected)

    var = window.splitlist(files)
    filePaths = list(var)

    list1.delete(0, END)

    for row in filePaths:
        list1.insert(END, row)


def add_folder():
    folder_selected = filedialog.askdirectory()
    delete_all_texboxes()
    filePaths = []

    for dirpath, _, filenames in os.walk(folder_selected):
        for filename in filenames:
            filePaths.append(os.path.join(dirpath, filename))

    list1.delete(0, END)

    for row in filePaths:
        list1.insert(END, row)


def get_selected_row(event):
    global selected_tuple

    index = list1.curselection()

    if index:
        selected_tuple = list1.get(index)

        getting_imagefilesize = pre_block_functions.get_file_size(
            selected_tuple)
        imagefilesize = pre_block_functions.convert_bytes(
            str(getting_imagefilesize), "MB")

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
            t2.delete('1.0', END)
            t2.insert(END, "Unfortunately " + heic_format +
                      "(.HEIC) are not supported!")
        elif st_row.endswith('.cr2'):
            var.set("Preview Not Available!")
            heic_format = "Canon Raw Version 2"

        labelimg.config(image=render)
        labelimg.image = render

        # Display File Name Under the Image
        filen = path_leaf(selected_tuple)

        img_exif_tags = pre_block_functions.get_exifread(selected_tuple)
        # Create an empty string to store the tag information
        tag_info = ""

        if not img_exif_tags:

            delete_all_texboxes()
            t1.insert(END, "No EXIF Data Detected")
            t2.insert(END, "No EXIF Data Detected")

        else:

            if img_exif_tags:
                try:
                    # Loop through each tag and add its information to the tag_info string
                    for tag in img_exif_tags.keys():
                        # Skip the JPEGThumbnail tag (because it is too long!)
                        # If you want to display the JPEGThumbnail tag, remove the 2 lines below
                        if tag.lower() == "jpegthumbnail":
                            continue
                        tag_info += f"{tag}: {img_exif_tags[tag]}\n"

                    # Display the tag information in the text field
                    delete_all_texboxes()
                    t2.insert(END, "File Name: " + filen + "\n")
                    t2.insert(END, "File Size: " + imagefilesize + "\n")
                    t2.insert('end', tag_info)
                except KeyError:
                    pass

        # Get Geo details (lat and long) and display in textbox
        img_lat_long = pre_block_functions.gps_lat_long(selected_tuple)

        if img_lat_long:
            t1.insert(END, f"GPS: {img_lat_long[0]}, {img_lat_long[1]}\n")
            t1.insert(
                END, "To Convert the GPS Coordinates to a Human Readable Location, Click the Button")


def remove_exif():
    global selected_tuple
    try:
        if not selected_tuple:
            messagebox.showwarning("No Image Selected",
                                   "Please select an image.")
            return
    except NameError:
        messagebox.showwarning("No Image Selected", "Please select an image.")
        return

    # Check if image has EXIF data
    img_exif_tags = pre_block_functions.get_exifread(selected_tuple)
    if not img_exif_tags:
        messagebox.showwarning(
            "No EXIF Data", "The selected image does not contain any EXIF data.")
        return

    # Check if image format is supported
    img_ext = os.path.splitext(selected_tuple)[1].lower()
    if img_ext not in ['.tiff', '.jpeg', '.jpg', '.png', '.webp', '.heic']:
        messagebox.showwarning(
            "Unsupported Image Format", "The selected image format is not supported.")
        return

    # Ask for confirmation before removing EXIF data
    confirmed = messagebox.askyesno(
        "Remove EXIF Data", "Are you sure you want to remove all EXIF data?")
    if confirmed:
        # Remove all EXIF data using exifread
        img = Image.open(selected_tuple)
        data = list(img.getdata())
        img_without_exif = Image.new(img.mode, img.size)
        img_without_exif.putdata(data)

        # Save the modified image using PIL.Image.save() method
        img_without_exif.save(selected_tuple)

        messagebox.showinfo(
            "EXIF Data Removed", "All EXIF data has been removed from the selected image.")


# Convert Lat and Long to Readable Address (Reverse Geocoding)
def get_gps_location(selected_tuple):
    try:
        gps_lat_long = pre_block_functions.gps_lat_long(selected_tuple)
        if gps_lat_long:
            location = pre_block_functions.convert_gps_to_loc(gps_lat_long)
            if location:
                return gps_lat_long, location
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def gps2loc_button_click():
    result = get_gps_location(selected_tuple)
    if result:
        gps, location = result
        t1.delete('1.0', END)
        t1.insert(END, f"GPS: {gps[0]}, {gps[1]}\n")
        t1.insert(END, f"Location: {location}")


def open_in_browser():
    img_lat_long = pre_block_functions.gps_lat_long(selected_tuple)
    if img_lat_long:
        webbrowser.open('https://www.google.com/maps?q=' +
                        str(img_lat_long[0]) + "," + str(img_lat_long[1]))


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
list1.place(relx=0.73, rely=0.274, relwidth=0.258, relheight=0.488)

# Link a scrollbar to the canvas
vsb = Scrollbar(frame, orient="vertical", command=list1.yview)
vsb.place(relx=0.988, rely=0.274, relheight=0.509, relwidth=0.012)
list1.configure(yscrollcommand=vsb.set)

hsb = Scrollbar(frame, orient="horizontal", command=list1.xview)
hsb.place(relx=0.73, rely=0.762, relheight=0.021, relwidth=0.258)
list1.configure(xscrollcommand=hsb.set)

list1.bind('<<ListboxSelect>>', get_selected_row)

statusbartext = StringVar()
statusbartext.set("Support this project by making a donation.")
satusbar = Label(frame, textvariable=statusbartext, bg="#0099df",
                 anchor="w", justify=LEFT, fg="#ffffff", cursor="hand2")
satusbar.place(relx=0, rely=0.965, relwidth=1, relheight=0.035)


def callback(event):
    webbrowser.open_new("https://aminbeheshti.com/donate/")


satusbar.bind("<Button-1>", callback)


t2 = Text(frame, wrap=WORD, bg="#ffffff", fg="#000000", bd=0)
t2.place(relx=0, rely=0.003, relwidth=0.729, relheight=0.780)

# Link a scrollbar to the canvas
t2_vsb = Scrollbar(frame, orient="vertical", command=t2.yview)
t2_vsb.place(relx=0.714, rely=0.003, relheight=0.780, relwidth=0.015)
t2.configure(yscrollcommand=t2_vsb.set)

b1 = Button(frame, text="Show on Map", bg="#1273eb",
            fg="#FFFFFF", command=open_in_browser)
b1.place(relx=0.001, rely=0.785, relwidth=0.3625, relheight=0.037)

b2 = Button(frame, text="Readable Address",
            bg="#ffb229", fg="#113255", command=gps2loc_button_click)
b2.place(relx=0.3655, rely=0.785, relwidth=0.3635, relheight=0.037)

b3 = Button(frame, text="Remove All EXIF Data",
            bg="#FF0000", fg="#113255", command=remove_exif)
# b3.place(relx=0.3655, rely=0.785, relwidth=0.3635, relheight=0.037)
b3.place(relx=0.73, rely=0.785, relwidth=0.27, relheight=0.037)

t1 = Text(frame, wrap=WORD, bg="#113255", fg="#ffffff", bd=0)
t1.place(relx=0, rely=0.822, relwidth=1, relheight=0.141)


def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)
    context_menu.event = event  # store the event in the menu


def copy_selected_text(widget):
    text = widget.get("sel.first", "sel.last")
    widget.clipboard_clear()  # clear the clipboard
    widget.clipboard_append(text)  # copy the selected text


context_menu = Menu(tearoff=0)
context_menu.add_command(
    label="Copy", command=lambda: copy_selected_text(context_menu.event.widget))

t1.bind("<Button-3>", show_context_menu)
t2.bind("<Button-3>", show_context_menu)

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add Photo(s)", command=list_images)
filemenu.add_command(label="Add a Folder", command=add_one_folder)
filemenu.add_command(label="Add Folder (+Sub Folders)", command=add_folder)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

menubar.add_command(label="About", command=aboutmsg)

window.config(menu=menubar)
window.mainloop()
# Ends here
