import tkinter
from tkinter import Menu
from src.constants import *
from PIL import Image, ImageTk, ImageGrab
import win32clipboard as clipboard
from io import BytesIO
from tkinter import filedialog
import os

x, y = 800, 500

okno = tkinter.Tk()
okno.title("Skicár")
okno.iconbitmap("assets/icon.ico")


# okno.geometry(f"{x+10}x{y+10}")

# create a menubar
menubar = Menu(okno, tearoff=0)
okno.config(menu=menubar)

navbar_y_size = 100
navbar = tkinter.Canvas(width=x, height=navbar_y_size, bg="gray")
navbar.place(x=0, y=0)

canvas = tkinter.Canvas(width=x, height=y-navbar_y_size, cursor="pencil", bg="white")
canvas.place(x=0, y=navbar_y_size)

def set_size(x, y):
    navbar.config(width=x, height=navbar_y_size)
    canvas.config(width=x, height=y-navbar_y_size)
    okno.geometry(f"{x+10}x{y+10}") 

okno.geometry(f"810x530") 


def rgb_color(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

current_color = "black"
def handle_color_button_click(color):
    global current_color
    current_color = color


pixel = tkinter.PhotoImage(width=1, height=1)
def add_button(x, y, rgb):
    return tkinter.Button(navbar, bg=rgb_color(rgb), activebackground=rgb_color(rgb), image=pixel, width=15, height=15, cursor="target",
    command=lambda: handle_color_button_click(rgb_color(rgb))).place(x=x, y=y)



for index, color in enumerate(COLORS):
    if index > 21:
        index -= 22
        add_button(5+index*20, 45, COLORS[color])
    elif index > 9:
        index -= 10
        add_button(5+index*20, 25, COLORS[color])
    else:
        add_button(5+index*20, 5, COLORS[color])

widthSlider = tkinter.Scale(navbar, from_=1, to=50, orient=tkinter.HORIZONTAL)
widthSlider.set(1)
widthSlider.place(x=5, y=55)

# for i in range(5, 100, 21):
    # add_button(i, 5, "red")

def load_image(image_path):
    return ImageTk.PhotoImage(Image.open(image_path).resize((15, 15)))

brushImage = load_image(BRUSH_PATH)
rectImage = load_image(RECTANGLE_PATH)
rectImageFilled = load_image(RECTANGLE_FILLED_PATH)
circleImage = load_image(CIRCLE_PATH)
circleImageFilled = load_image(CIRCLE_FILLED_PATH)
clearImage = load_image(CLEAR_PATH)
selectImage = load_image(SELECT_PATH)

tool = "pencil"
selectTool = None
def change_tool(new_tool):
    global tool, selectTool
    if selectTool != None and new_tool != "select":
        canvas.delete(selectTool)
        selectTool = None
    tool = new_tool


tkinter.Button(navbar, image=selectImage, width=15, height=15, cursor="target", command=lambda: change_tool("select")).place(x=460, y=5)
tkinter.Button(navbar, image=brushImage, width=15, height=15, cursor="target", command=lambda: change_tool("pencil")).place(x=480, y=5)
tkinter.Button(navbar, image=rectImage, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle")).place(x=500, y=5)
tkinter.Button(navbar, image=rectImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle_filled")).place(x=520, y=5)
tkinter.Button(navbar, image=circleImage, width=15, height=15, cursor="target", command=lambda: change_tool("circle")).place(x=540, y=5)
tkinter.Button(navbar, image=circleImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("circle_filled")).place(x=560, y=5)
tkinter.Button(navbar, image=clearImage, width=15, height=15, cursor="target", command=lambda: canvas.delete("all")).place(x=580, y=5)


def save_to_clipboard(image):
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(clipboard.CF_DIB, image)
    clipboard.CloseClipboard()


def destroy(window, e1, e2):
    global x, y
    x, y = int(e1), int(e2)
    set_size(x, y)
    window.destroy()


def popupmsg():
    global popup
    popup = tkinter.Tk()
    popup.geometry(f"320x80")
    popup.wm_title("Skicár - Change window size")
    popup.iconbitmap("assets/icon.ico")
    tkinter.Label(popup, text="New x: ").place(x=60, y=0)
    tkinter.Label(popup, text="New y: ").place(x=60, y=20)
    e1_text = tkinter.StringVar()
    e2_text = tkinter.StringVar()
    e1 = tkinter.Entry(popup, textvariable=e1_text)
    e2 = tkinter.Entry(popup, textvariable=e2_text)
    e1.place(x=110, y=0)
    e2.place(x=110, y=20)
    tkinter.Button(popup, text="Okay", command=lambda: destroy(popup, e1.get(), e2.get())).place(x=140, y=40)
    popup.mainloop()

def save_canvas():
    x = okno.winfo_rootx() + canvas.winfo_x()
    y = okno.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()
    ImageGrab.grab(bbox=(x, y, xx, yy)).save("canvas.png")

def save_canvas_as():
    x = okno.winfo_rootx() + canvas.winfo_x()
    y = okno.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()
    save_image_as(ImageGrab.grab(bbox=(x, y, xx, yy)))

def save_image_as(image):
    result = filedialog.asksaveasfilename(initialdir="/", title="Save file as", defaultextension=".png", filetypes=(
        ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('BMP', ('*.bmp', '*.jdib'))))
    if result != "":
        image.save(result)

def copy_canvas(coords):
    x = okno.winfo_rootx() + canvas.winfo_x() + coords[0] + 1
    y = okno.winfo_rooty() + canvas.winfo_y() + coords[1] + 1
    xx = x + coords[2] - coords[0] - 1
    yy = y + coords[3] - coords[1] - 1
    
    image = ImageGrab.grab(bbox=(x, y, xx, yy))

    output = BytesIO()
    image.save(output, format="BMP")
    data = output.getvalue()[14:]
    output.close()
    save_to_clipboard(data)

def open_image():
    global image
    image = Image.open(filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
        ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('BMP', ('*.bmp', '*.jdib')))))
    # image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
    if image != "":
        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)

def paste_image():
    image = ImageGrab.grabclipboard()
    if image is not None:
        image.save("clipboard.png")
        image = Image.open("clipboard.png")
        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)
        os.remove("clipboard.png")


control = False
shift = False
def handle_key_event(event):
    global control, shift, selectTool
    key = event.keysym

    if key == "Control_L":
        control = True
    if key == "Shift_L":
        shift = True

    if key == "Delete":
        if selectTool is not None:
            canvas.create_rectangle(canvas.coords(selectTool), fill="white", outline="white")
            canvas.delete(selectTool)
            selectTool = None
    elif key == "a" and control:
        if selectTool is not None:
            canvas.delete(selectTool)
            selectTool = None
        selectTool = canvas.create_rectangle(5, 5, canvas.winfo_width()-10, canvas.winfo_height()-10, width=1, outline="black", dash=(4, 1))
    elif key == "c" and control and selectTool is not None:
        copy_canvas(canvas.coords(selectTool))
        canvas.delete(selectTool)
    elif key == "n" and control:
        popupmsg()
    elif key == "o" and control:
        open_image()
    elif key == "s" and control:
        save_canvas()
    elif key == "s" and control and shift:
        save_canvas_as()
    elif key == "v" and control:
        paste_image()
    elif key == "z" and control:
        undo()
        
def handle_key_release(event):
    global control, shift
    key = event.keysym
    if key == "Control_L":
        control = False
    if key == "Shift_L":
        shift = False

bodky = []
shapes = []
history = []
draw_history = []

def handle_left_click(event):
    global bodky, shapes, selectTool, draw_history
    if tool == "pencil":
        if widthSlider.get() < 3:
            bodky.append([event.x, event.y])
            if len(bodky) >= 2:
                line = canvas.create_line(bodky[0], bodky[1], width=widthSlider.get(), fill=current_color)
                draw_history.append(line)
                bodky.pop(0)
        else:
            oval = canvas.create_oval(event.x-widthSlider.get()/2, event.y-widthSlider.get()/2, event.x+widthSlider.get()/2, event.y+widthSlider.get()/2, fill=current_color, outline=current_color)
            draw_history.append(oval)
    # elif tool == "rectangle":
    else:
        if len(bodky) < 1:
            bodky.append([event.x, event.y])
        for shape in shapes:
            canvas.delete(shape)
        shapes = []
        if tool == "rectangle":
            s = canvas.create_rectangle(bodky[0][0], bodky[0][1], event.x, event.y, width=widthSlider.get(), outline=current_color)
        elif tool == "rectangle_filled":
            s = canvas.create_rectangle(bodky[0][0], bodky[0][1], event.x, event.y, width=widthSlider.get(), outline=current_color, fill=current_color)
        elif tool == "circle":
            s = canvas.create_oval(bodky[0][0], bodky[0][1], event.x, event.y, width=widthSlider.get(), outline=current_color)
        elif tool == "circle_filled":
            s = canvas.create_oval(bodky[0][0], bodky[0][1], event.x, event.y, width=widthSlider.get(), outline=current_color, fill=current_color)
        elif tool == "select":
            if selectTool is not None:
                canvas.delete(selectTool)
                selectTool = None
            s = canvas.create_rectangle(bodky[0][0], bodky[0][1], event.x, event.y, width=1, outline="black", dash=(4, 1))
        shapes.append(s)

def handle_left_up(event):
    global bodky, shapes, selectTool, draw_history
    if tool == "select":
        selectTool = shapes[0]
        # canvas.delete(shapes[0])
        # bodky.append([event.x, event.y])
        # if len(bodky) >= 2:
        #     canvas.create_line(bodky[0], bodky[1], width=widthSlider.get(), fill=current_color)
        #     bodky.pop(0)
    if shapes != []:
        history.append(shapes)
    if draw_history != []:
        history.append(draw_history)
    shapes = []
    bodky = []
    draw_history = []

def undo():
    global history
    if len(history) == 0:
        return
    if type(history[-1]) == list:
        for line in history[-1]:
            canvas.delete(line)
    else:
        canvas.delete(history[-1])

    history.pop(-1)

# create a menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=popupmsg, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_image, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_canvas, accelerator="Ctrl+S")
file_menu.add_command(label="Save as...", command=save_canvas_as, accelerator="Ctrl+Shift+S")
file_menu.add_command(label='Exit', command=okno.destroy)


edit_menu = Menu(menubar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
edit_menu.add_separator()
edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
edit_menu.add_command(label="Delete", command=lambda: canvas.delete("all"), accelerator="Del")




menubar.add_cascade(
    label="File",
    menu=file_menu
)

menubar.add_cascade(
    label="Edit",
    menu=edit_menu
)



canvas.bind_all("<Key>", handle_key_event)
canvas.bind_all("<KeyRelease>", handle_key_release)
canvas.bind("<Button-1>", handle_left_click)
canvas.bind("<B1-Motion>", handle_left_click)
canvas.bind("<ButtonRelease>", handle_left_up)
okno.mainloop()