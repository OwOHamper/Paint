import tkinter
from tkinter import Menu
from src.constants import *
from PIL import Image, ImageTk, ImageGrab
import win32clipboard as clipboard
from io import BytesIO
from tkinter import filedialog
import os
import webbrowser

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

canvas = tkinter.Canvas(width=x, height=y-navbar_y_size, cursor="none", bg="white")
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
def add_button(x, y, rgb, width=15, height=15):
    return tkinter.Button(navbar, bg=rgb_color(rgb), activebackground=rgb_color(rgb), image=pixel, width=width, height=height, cursor="target",
    command=lambda: handle_color_button_click(rgb_color(rgb))).place(x=x, y=y)

def delete_canvas():
    global images
    confirmation.destroy()
    # images_garbage_collection = []
    images = []
    canvas.delete("all")


def delete_confirmation():
    global confirmation
    confirmation = tkinter.Tk()
    confirmation.geometry(f"360x80")
    confirmation.wm_title("Skicár - Delete canvas")
    confirmation.iconbitmap("assets/icon.ico")
    tkinter.Label(confirmation, text="Are you sure you want to delete the canvas?").place(x=60, y=0)
    tkinter.Button(confirmation, text="Yes", command=delete_canvas, width=5).place(x=130, y=40)
    tkinter.Button(confirmation, text="No", command=confirmation.destroy, width=5).place(x=180, y=40)
    confirmation.mainloop()



for index, color in enumerate(COLORS):
    if index > 21:
        index -= 22
        add_button(5+index*40, 85, COLORS[color], width=40, height=40)
    elif index > 9:
        index -= 10
        add_button(5+index*40, 45, COLORS[color], width=40, height=40)
    else:
        add_button(5+index*40, 5, COLORS[color], width=40, height=40)

widthSlider = tkinter.Scale(navbar, from_=1, to=200, orient=tkinter.HORIZONTAL, troughcolor="black", length=250, font=("Helvetica",13,"bold"), cursor="sb_h_double_arrow", highlightbackground=None)
widthSlider.set(1)
widthSlider.place(x=445, y=43)

# for i in range(5, 100, 21):
    # add_button(i, 5, "red")

def load_image(image_path):
    return ImageTk.PhotoImage(Image.open(image_path).resize((28, 28)))

brushImage = load_image(BRUSH_PATH)
rectImage = load_image(RECTANGLE_PATH)
rectImageFilled = load_image(RECTANGLE_FILLED_PATH)
circleImage = load_image(CIRCLE_PATH)
circleImageFilled = load_image(CIRCLE_FILLED_PATH)
clearImage = load_image(CLEAR_PATH)
selectImage = load_image(SELECT_PATH)
pointerImage = load_image(POINTER_PATH)
eraserImage = load_image(ERASER_PATH)
lineImage = load_image(LINE_PATH)

tool = "pencil"
selectTool = None
pointer_status = None
def change_tool(new_tool):
    global tool, selectTool, temp_pointer
    if temp_pointer != None and (new_tool != "pencil" or new_tool != "eraser"):
        canvas.delete(temp_pointer)
        temp_pointer = None
    if new_tool == "pencil" or new_tool == "eraser":
        canvas.config(cursor="none")
    elif new_tool == "pointer":
        pointer_status = "move"
        canvas.config(cursor="arrow")
    else:
        canvas.config(cursor="crosshair")
    if selectTool != None and new_tool != "select":
        canvas.delete(selectTool)
        selectTool = None
    tool = new_tool

from idlelib.tooltip import Hovertip

pointerButton = tkinter.Button(navbar, image=pointerImage, width=15, height=15, cursor="target", command=lambda: change_tool("pointer"))
selectButton = tkinter.Button(navbar, image=selectImage, width=15, height=15, cursor="target", command=lambda: change_tool("select"))
pencilButton = tkinter.Button(navbar, image=brushImage, width=15, height=15, cursor="target", command=lambda: change_tool("pencil"))
eraserButton = tkinter.Button(navbar, image=eraserImage, width=15, height=15, cursor="target", command=lambda: change_tool("eraser"))
lineButton = tkinter.Button(navbar, image=lineImage, width=15, height=15, cursor="target", command=lambda: change_tool("line"))
rectangleButton = tkinter.Button(navbar, image=rectImage, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle"))
rectangleFilledButton = tkinter.Button(navbar, image=rectImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle_filled"))
circleButton = tkinter.Button(navbar, image=circleImage, width=15, height=15, cursor="target", command=lambda: change_tool("circle"))
circleFilledButton = tkinter.Button(navbar, image=circleImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("circle_filled"))
clearButton = tkinter.Button(navbar, image=clearImage, width=15, height=15, cursor="target", command=delete_confirmation)

width = 30

toolList = [pointerButton, selectButton, pencilButton, eraserButton, lineButton, rectangleButton, rectangleFilledButton, circleButton, circleFilledButton, clearButton]
positions_x = range(440, 440+width*len(toolList), width)
for tool_ in toolList:
    tool_.place(x=positions_x[toolList.index(tool_)], y=5, width=30, height=30)


Hovertip(pointerButton, "Pointer Tool (v)")
Hovertip(selectButton, "Select Tool (m)")
Hovertip(pencilButton, "Brush Tool (b)")
Hovertip(eraserButton, "Eraser Tool (e)")
Hovertip(lineButton, "Line Tool (l)")
Hovertip(rectangleButton, "Rectangle Tool (r)")
Hovertip(rectangleFilledButton, "Filled Rectangle Tool (f)")
Hovertip(circleButton, "Circle Tool (c)")
Hovertip(circleFilledButton, "Filled Circle Tool (d)")
Hovertip(clearButton, "Clear Canvas")

# tkinter.Label(navbar, text="v").place(x=440, y=25, width=15, height=15)


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



def open_link(url):
    webbrowser.open_new_tab(url)

def about_window():
    global about
    about = tkinter.Tk()
    about.geometry(f"400x100")
    about.wm_title("Skicár - About")
    about.iconbitmap("assets/icon.ico")
    tkinter.Label(about, text=f"Skicár version: {VERSION}").place(x=70, y=10)
    tkinter.Label(about, text="GitHub repository: ").place(x=50, y=30)
    link = tkinter.Label(about, text="https://github.com/OwOHamper/Paint", fg="blue", cursor="hand2")
    link.place(x=150, y=30)
    link.bind("<Button-1>", lambda x: open_link("https://github.com/OwOHamper/Paint"))
    tkinter.Button(about, text="Okay", command=lambda: about.destroy()).place(x=180, y=60)
    about.mainloop()

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
images = []
# images_garbage_collection = []
def open_image():
    global image, images
    files = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=(
        ('PNG', '*.png'), ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('BMP', ('*.bmp', '*.jdib'))))
    for image_file in files:
        pil_image = Image.open(image_file)
        if pil_image != "":
            image = ImageTk.PhotoImage(pil_image)
            # images_garbage_collection.append(image)
            im = canvas.create_image(0, 0, anchor="nw", image=image)
            #append to start instead of end
            images.insert(0, {"image": im, "coords": [0, 0, image.width(), image.height()], "pil_image": pil_image, "photo_image": image})

def paste_image():
    global image, images
    image = ImageGrab.grabclipboard()
    if image is not None:
        image.save("clipboard.png")
        pil_image = Image.open("clipboard.png")
        image = ImageTk.PhotoImage(pil_image)
        # images_garbage_collection.append(image)
        im = canvas.create_image(0, 0, anchor="nw", image=image)
        #append to start instead of end
        images.insert(0, {"image": im, "coords": [0, 0, image.width(), image.height()], "pil_image": pil_image, "photo_image": image})
        os.remove("clipboard.png")

def resize_pil_image(pil_image, coords, corner, x_diff, y_diff):
    # try:
    if corner == "top_left":
        width = coords[2] - coords[0] - x_diff
        height = coords[3] - coords[1] - y_diff
        pos_x = coords[0] + x_diff
        pos_y = coords[1] + y_diff
        if width < 1:
            width = 1
            pos_x = coords[0]
        if height < 1:
            height = 1
            pos_y = coords[1]

        pil_image_reiszed = pil_image.resize((width, height), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(pil_image_reiszed)
        image = canvas.create_image(pos_x, pos_y, anchor="nw", image=photo_image)
        return {"image": image, "coords": [pos_x, pos_y, pos_x + width, pos_y + height], "pil_image": pil_image, "photo_image": photo_image}
    elif corner == "top_right":
        width = coords[2] - coords[0] + x_diff
        height = coords[3] - coords[1] - y_diff
        pos_x = coords[0]
        pos_y = coords[1] + y_diff
        if width < 1:
            width = 1
        if height < 1:
            height = 1
            pos_y = coords[1]

        pil_image_reiszed = pil_image.resize((width, height), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(pil_image_reiszed)
        image = canvas.create_image(pos_x, pos_y, anchor="nw", image=photo_image)
        return {"image": image, "coords": [pos_x, pos_y, pos_x + width, pos_y + height], "pil_image": pil_image, "photo_image": photo_image}
    elif corner == "bottom_left":
        width = coords[2] - coords[0] - x_diff
        height = coords[3] - coords[1] + y_diff
        pos_x = coords[0] + x_diff
        pos_y = coords[1]
        if width < 1:
            width = 1
            pos_x = coords[0]
        if height < 1:
            height = 1

        pil_image_reiszed = pil_image.resize((width, height), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(pil_image_reiszed)
        image = canvas.create_image(pos_x, pos_y, anchor="nw", image=photo_image)
        return {"image": image, "coords": [pos_x, pos_y, pos_x + width, pos_y + height], "pil_image": pil_image, "photo_image": photo_image}
    elif corner == "bottom_right":
        width = coords[2] - coords[0] + x_diff
        height = coords[3] - coords[1] + y_diff
        pos_x = coords[0]
        pos_y = coords[1]
        if width < 1:
            width = 1
        if height < 1:
            height = 1

        pil_image_reiszed = pil_image.resize((width, height), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(pil_image_reiszed)
        image = canvas.create_image(pos_x, pos_y, anchor="nw", image=photo_image)
        return {"image": image, "coords": [pos_x, pos_y, pos_x + width, pos_y + height], "pil_image": pil_image, "photo_image": photo_image}
    # except ValueError:
    #     print("Test")
    #     photo_image = ImageTk.PhotoImage(pil_image)
    #     image = canvas.create_image(coords[0], coords[1], anchor="nw", image=photo_image)
    #     return {"image": image, "coords": coords, "pil_image": pil_image, "photo_image": photo_image}

control = False
shift = False
def handle_key_event(event):
    global control, shift, selectTool
    key = event.keysym

    #modifiers
    if key == "Control_L":
        control = True
    if key == "Shift_L":
        shift = True

    #tools
    if key == "v":
        change_tool("pointer")
    elif key == "m":
        change_tool("select")
    elif key == "b":
        change_tool("pencil")
    elif key == "b":
        change_tool("pencil")
    elif key == "e":
        change_tool("eraser")
    elif key == "l":
        change_tool("line")
    elif key == "r":
        change_tool("rectangle")
    elif key == "f":
        change_tool("rectangle_filled")
    elif key == "c":
        change_tool("circle")
    elif key == "d":
        change_tool("circle_filled")



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
initial_mouse_pos = []
image_selected = None
temp_pointer = None
total_image_move = [0, 0]
def handle_left_click(event):
    global bodky, shapes, selectTool, draw_history, initial_mouse_pos, image_selected, temp_pointer, total_image_move
    global a

    if tool == "pencil" or tool == "eraser":
        if widthSlider.get() < 3:
            bodky.append([event.x, event.y])
            if len(bodky) >= 2:
                if tool == "pencil":
                    line = canvas.create_line(bodky[0], bodky[1], width=widthSlider.get(), fill=current_color)
                else:
                    line = canvas.create_line(bodky[0], bodky[1], width=widthSlider.get(), fill="white")
                draw_history.append(line)
                bodky.pop(0)
        else:
            if tool == "pencil":
                oval = canvas.create_oval(event.x-widthSlider.get()/2, event.y-widthSlider.get()/2, event.x+widthSlider.get()/2, event.y+widthSlider.get()/2, fill=current_color, outline=current_color)
            else:
                oval = canvas.create_oval(event.x-widthSlider.get()/2, event.y-widthSlider.get()/2, event.x+widthSlider.get()/2, event.y+widthSlider.get()/2, fill="white", outline="white")
            draw_history.append(oval)
        if tool == "eraser":
            if temp_pointer is not None:
                canvas.delete(temp_pointer)
            temp_pointer = canvas.create_oval(event.x-widthSlider.get()/2, event.y-widthSlider.get()/2, event.x+widthSlider.get()/2, event.y+widthSlider.get()/2, outline="black")

    # elif tool == "rectangle":
    elif tool == "pointer":
        if image_selected is None:
            #reverse list so images on top will be prioritized
            for image in range(len(images)):
                coords = images[image]["coords"]
                #get image height and width
                if coords[0] < event.x < coords[2] and coords[1] < event.y < coords[3]:
                    if initial_mouse_pos == []:
                        initial_mouse_pos = [event.x, event.y]
                        image_selected = image
                        if image >= 1:
                            #move image to top only visually need to change order in list too
                            canvas.tag_raise(images[image_selected]["image"])
                            images.insert(0, images.pop(image_selected))
                            image_selected = 0
        else:
            coords = images[image_selected]["coords"]
            x_diff = event.x-initial_mouse_pos[0]
            y_diff = event.y-initial_mouse_pos[1]
            if pointer_status == "move":
                canvas.move(images[image_selected]["image"], x_diff, y_diff)
                total_image_move[0] += x_diff
                total_image_move[1] += y_diff
                images[image_selected]["coords"] = [coords[0]+x_diff, coords[1]+y_diff, coords[2]+x_diff, coords[3]+y_diff]
                initial_mouse_pos = [event.x, event.y]
            elif pointer_status.startswith("resize"):
                canvas.delete(images[image_selected]["image"])
                if pointer_status == "resize-top-left":
                    images[image_selected] = resize_pil_image(images[image_selected]["pil_image"], images[image_selected]["coords"], "top_left", x_diff, y_diff)
                    initial_mouse_pos = [event.x, event.y]
                elif pointer_status == "resize-top-right":
                    images[image_selected] = resize_pil_image(images[image_selected]["pil_image"], images[image_selected]["coords"], "top_right", x_diff, y_diff)
                    initial_mouse_pos = [event.x, event.y]
                elif pointer_status == "resize-bottom-left":
                    images[image_selected] = resize_pil_image(images[image_selected]["pil_image"], images[image_selected]["coords"], "bottom_left", x_diff, y_diff)
                    initial_mouse_pos = [event.x, event.y]
                elif pointer_status == "resize-bottom-right":
                    images[image_selected] = resize_pil_image(images[image_selected]["pil_image"], images[image_selected]["coords"], "bottom_right", x_diff, y_diff)
                    initial_mouse_pos = [event.x, event.y]
    else:
        if len(bodky) < 1:
            bodky.append([event.x, event.y])
        for shape in shapes:
            canvas.delete(shape)
        shapes = []
        if tool == "line":
            s = canvas.create_line(bodky[0][0], bodky[0][1], event.x, event.y, width=widthSlider.get(), fill=current_color)
        elif tool == "rectangle":
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

def handle_left_drag(event):
    global temp_pointer, pointer_status
    if tool == "pencil" or tool == "eraser":
        if temp_pointer is not None:
            canvas.delete(temp_pointer)
        temp_pointer = canvas.create_oval(event.x-widthSlider.get()/2, event.y-widthSlider.get()/2, event.x+widthSlider.get()/2, event.y+widthSlider.get()/2, outline="black")
    elif tool == "pointer":
        if len(images) == 0:
            canvas.config(cursor="arrow")
        for image in range(len(images)):
            coords = images[image]["coords"]
            corner_tolerance = 20

            #cursor change
            #moving cursor
            if coords[0] < event.x < coords[2] and coords[1] < event.y < coords[3]:
                canvas.config(cursor="fleur")
                pointer_status = "move"
                break
            #resizing cursor
            elif coords[0]-corner_tolerance < event.x < coords[0]+corner_tolerance and coords[1]-corner_tolerance < event.y < coords[1]+corner_tolerance:
                canvas.config(cursor="top_left_corner")
                pointer_status = "resize-top-left"
                break
            elif coords[2]-corner_tolerance < event.x < coords[2]+corner_tolerance and coords[1]-corner_tolerance < event.y < coords[1]+corner_tolerance:
                canvas.config(cursor="top_right_corner")
                pointer_status = "resize-top-right"
                break
            elif coords[0]-corner_tolerance < event.x < coords[0]+corner_tolerance and coords[3]-corner_tolerance < event.y < coords[3]+corner_tolerance:
                canvas.config(cursor="bottom_left_corner")
                pointer_status = "resize-bottom-left"
                break
            elif coords[2]-corner_tolerance < event.x < coords[2]+corner_tolerance and coords[3]-corner_tolerance < event.y < coords[3]+corner_tolerance:
                canvas.config(cursor="bottom_right_corner")
                pointer_status = "resize-bottom-right"
                break
            #default cursor
            else:
                canvas.config(cursor="arrow")




def handle_left_up(event):
    global bodky, shapes, selectTool, draw_history, initial_mouse_pos, image_selected, total_image_move
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
    if total_image_move != [0, 0]:
        history.append({"type": "image_move", "image": image_selected, "move": total_image_move})
    total_image_move = [0, 0]
    initial_mouse_pos = []
    image_selected = None
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
    elif type(history[-1]) == dict:
        if history[-1].get("type") == "image_move":
            x_diff = history[-1]["move"][0]
            y_diff = history[-1]["move"][1]
            canvas.move(images[history[-1]["image"]]["image"], -x_diff, -y_diff)
            coords = images[history[-1]["image"]]["coords"]
            images[history[-1]["image"]]["coords"] = [coords[0]-x_diff, coords[1]-y_diff, coords[2]-x_diff, coords[3]-y_diff]
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
edit_menu.add_command(label="Delete", command=delete_confirmation, accelerator="Del")

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=about_window)


menubar.add_cascade(
    label="File",
    menu=file_menu
)

menubar.add_cascade(
    label="Edit",
    menu=edit_menu
)

menubar.add_cascade(
    label="Help",
    menu=help_menu
)



canvas.bind_all("<Key>", handle_key_event)
canvas.bind_all("<KeyRelease>", handle_key_release)
canvas.bind("<Button-1>", handle_left_click)
canvas.bind("<B1-Motion>", handle_left_click)
canvas.bind("<Motion>", handle_left_drag)
canvas.bind("<ButtonRelease>", handle_left_up)
okno.mainloop()
