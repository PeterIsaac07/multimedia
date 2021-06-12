from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import colorchooser
import webcolors as col
import math as m
import numpy as np
import matplotlib.pyplot as plt
from video_player import Player
from PIL import ImageTk, Image
import main as algo

UNFILLED = "white"


def Alert_Message(M, parent_root):
    error = Tk()
    error.title("ALERT")
    message = Label(error, text=M)
    message.grid(row=0, columnspan=3, pady=30, padx=40)
    if parent_root:
        error.protocol("WM_DELETE_WINDOW", lambda: [error.destroy(), parent_root.deiconify()])
    else:
        error.protocol("WM_DELETE_WINDOW", lambda: [error.destroy()])


def closest_colour_name(requested_colour):
    min_colours = {}
    for key, name in col.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = col.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


class GridApp:
    """The main class representing a grid of coloured cells."""

    def __init__(self, master, n, width=200, height=200, pad=2):
        """Initialize a grid and the Tk Frame on which it is rendered."""
        # Number of cells in each dimension.
        self.n = n

        self.ColorLayout_list = [[255, 255, 255]] * (self.n * self.n)

        # Some dimensions for the App in pixels.
        self.width, self.height = width, height
        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        npad = n + 1

        self.pad = pad

        xsize = (width - npad * pad) / n
        ysize = (height - npad * pad) / n
        # Canvas dimensions for the cell grid and the palette.
        c_width, c_height = width, height

        # The main frame onto which we draw the App's elements.
        frame = Frame(master)
        frame.pack()

        # The canvas onto which the grid is drawn.
        self.w = Canvas(master, width=c_width, height=c_height)
        self.w.pack()

        # Add the cell rectangles to the grid canvas.
        self.cells = []
        for iy in range(n):
            for ix in range(n):
                xpad, ypad = pad * (ix + 1), pad * (iy + 1)
                x, y = xpad + ix * xsize, ypad + iy * ysize
                rect = self.w.create_rectangle(x, y, x + xsize,
                                               y + ysize, fill=UNFILLED)
                self.cells.append(rect)

        def w_click_callback(event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (xsize + pad))
            iy = int(y // (ysize + pad))
            if ix < n and iy < n:
                i = iy * n + ix
                color_code = colorchooser.askcolor(title="Choose color")
                if color_code == (None, None):
                    return
                color_code = list(color_code[0])
                for j in range(3):
                    color_code[j] = m.floor(color_code[j])
                self.ColorLayout_list[i] = color_code
                self.w.itemconfig(self.cells[i], fill=closest_colour_name(color_code))

        # Bind the grid click callback function to the left mouse button
        # press event on the grid canvas.
        self.w.bind('<ButtonPress-1>', w_click_callback)

    def return_ColorList(self):
        """Output a list of cell coordinates, sorted by cell colour."""
        return self.ColorLayout_list

    def clear_grid(self):
        """Reset the grid to the background "UNFILLED" colour."""
        self.ColorLayout_list = [[255, 255, 255]] * (self.n * self.n)
        for cell in self.cells:
            self.w.itemconfig(cell, fill=UNFILLED)


def Video_InputWindow(mode, s_flag):
    input_file = filedialog.askopenfile(title='Please Select Video',
                                        filetypes=[("Videos", ".mp4")])
    print(s_flag)

    if input_file is None:
        root.deiconify()
        return

    if "Add" in mode:
        algo.saving_video(input_file.name)
        Alert_Message("___Video Added SUCCESSFULLY in DB___\n", root)
        return

    # Call l function beta3et l video retrieval
    output_list = algo.compare_video(input_file.name)

    if s_flag:
        algo.saving_video(input_file.name)
        Alert_Message("___Query Video SAVED in DB___\n", None)

    # call ll output
    Output(output_list)


def Image_InputWindow(mode, s_flag):
    input_file = filedialog.askopenfile(title='Please Select Image',
                                        filetypes=[("Image", ".jpg"), ("Image", ".png"), ("Image", ".jpeg")])



    if input_file is None:
        root.deiconify()
        return
    if "Add" in mode:
        algo.saving_image(input_file.name)
        Alert_Message("___Image Added SUCCESSFULLY in DB___\n", root)
        return
    elif "Histogram" in mode:
        '''
        call the image retrieval function based on histogram
        '''
        out_list = algo.compare_img_hist(input_file.name)
    else:
        '''
        call the image retrieval function based on Mean color
        '''
        out_list = algo.compare_img_mean(input_file.name)

    if s_flag:
        algo.saving_image(input_file.name)
        Alert_Message("___Query Image SAVED in DB___\n", None)

    Output(out_list)


def Output(out_list):
    output_root = Tk()
    output_root.title("OUTPUT WINDOW")
    output_root.protocol("WM_DELETE_WINDOW", lambda: [output_root.destroy(), root.deiconify()])

    wl = Label(output_root, text="__Select Output to View__\n . . . . .")
    entry_mod = Label(output_root, text="Content Base Retrieval OutPut :")
    mode = Combobox(output_root, justify='center', value=out_list, state='readonly')
    # mode.current(0)

    Nex = Button(output_root, text="VIEW",
                 command=lambda: [output_root.withdraw(),
                                  play_video(mode.get(), output_root) if 'mp4' in mode.get() else view_image(mode.get(),
                                                                                                             output_root)])
    wl.grid(row=0, columnspan=3, pady=15)

    entry_mod.grid(row=1, padx=10, sticky=W, pady=10)
    mode.grid(row=1, column=1, columnspan=2, padx=10, sticky=W, pady=10)

    Nex.grid(row=4, columnspan=3, pady=15)


def play_video(url, parent):
    rt = Tk()
    rt.title("VIEW WINDOW")
    p = Player(rt, url)
    rt.protocol("WM_DELETE_WINDOW", lambda: [rt.destroy(), p.Exit(), parent.deiconify()])
    p.Play()


def view_image(url, parent):
    rt = Tk()
    rt.protocol("WM_DELETE_WINDOW", lambda: [rt.destroy(), parent.deiconify()])

    image = Image.open(url)
    photo = ImageTk.PhotoImage(image, master=rt)

    label = Label(rt, image=photo)
    # label.image = photo
    label.grid(row=1)

    img = ImageTk.PhotoImage(Image.open(url))
    imag = Label(url, image=img)


def Layout_InputWindow():
    input_root = Tk()
    input_root.title("INPUT WINDOW")
    input_root.protocol("WM_DELETE_WINDOW", lambda: [input_root.destroy(), root.deiconify()])

    grid = GridApp(input_root, 6, 200, 200, 2)
    # Load and save image buttons
    b_next = Button(input_root, text='Next',
                    command=lambda: [input_root.withdraw(), ColorLayout_retrieve(grid.return_ColorList())])
    b_next.pack(side=RIGHT, padx=2, pady=2)
    # Add a button to clear the grid
    b_clear = Button(input_root, text='Clear', command=grid.clear_grid)
    b_clear.pack(side=LEFT, padx=2, pady=2)

    def ColorLayout_retrieve(color_list):
        # call the retrieve function
        im = np.array(color_list)
        # im = im.reshape((6, 6, 3))
        im = im.astype(np.uint8)
        im = Image.fromarray(im.reshape((6, 6, 3)))
        im = im.resize((600, 600))
        im = np.array(im)
        # im = im.resize(512,512)
        # plt.imshow(im)
        # plt.show()

        out_list = algo.compare_grid_hist(im)
        # call the output
        Output(out_list)


root = Tk()
root.title('MAIN MENU')
types = ["CBVR", "CBIR using Mean Color", "CBIR using Histogram", "CBIR using Color Layout", "Add Image to DB",
         "Add Video to DB"]

wlc = Label(root, text="______WELCOME______\n . . . . .")
entry_mode = Label(root, text="Content Base Retrieval Mode :")
modes = Combobox(root, justify='center', value=types, state='readonly')
modes.current(0)
check_input = IntVar()
c = Checkbutton(root, text = "Allow SAVING Query Image/Video in DB", variable=check_input)


Next = Button(root, text="NEXT",
              command=lambda: [root.withdraw(), Next_Window(modes.get(), check_input.get())])
wlc.grid(row=0, columnspan=3, pady=15)

entry_mode.grid(row=1, padx=10, sticky=W, pady=10)
modes.grid(row=1, column=1, columnspan=2, padx=10, sticky=W, pady=10)
c.grid(row=3, column=0, columnspan=2, padx=10, sticky=W, pady=10)
Next.grid(row=4, columnspan=3, pady=15)


def Next_Window(mode, save_flage):
    if "CBVR" in mode or "Video" in mode:
        Video_InputWindow(mode, save_flage)
    elif "Layout" in mode:
        Layout_InputWindow()
    else:
        Image_InputWindow(mode, save_flage)


root.mainloop()
