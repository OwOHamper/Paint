import tkinter
from src.constants import *
from PIL import Image, ImageTk

x, y = 800, 500

okno = tkinter.Tk()
okno.title("Skicár")
okno.geometry(f"{x}x{y}")




navbar = tkinter.Canvas(width=x, height=y/5, bg="gray")
navbar.place(x=0, y=0)

canvas = tkinter.Canvas(width=x, height=y, cursor="pencil", bg="white")
canvas.place(x=0, y=y/5)

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
    if index > 23:
        index -= 24
        add_button(5+index*20, 45, COLORS[color])
    elif index > 11:
        index -= 12
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

tool = "pencil"

def change_tool(new_tool):
    global tool
    tool = new_tool



tkinter.Button(navbar, image=brushImage, width=15, height=15, cursor="target", command=lambda: change_tool("pencil")).place(x=480, y=5)
tkinter.Button(navbar, image=rectImage, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle")).place(x=500, y=5)
tkinter.Button(navbar, image=rectImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("rectangle_filled")).place(x=520, y=5)
tkinter.Button(navbar, image=circleImage, width=15, height=15, cursor="target", command=lambda: change_tool("circle")).place(x=540, y=5)
tkinter.Button(navbar, image=circleImageFilled, width=15, height=15, cursor="target", command=lambda: change_tool("circle_filled")).place(x=560, y=5)
tkinter.Button(navbar, image=clearImage, width=15, height=15, cursor="target", command=lambda: canvas.delete("all")).place(x=580, y=5)

def handle_key_event(event):
    key = event.keysym
    print(key)

bodky = []
shapes = []

def handle_left_click(event):
    global bodky, shapes
    if tool == "pencil":
        bodky.append([event.x, event.y])
        if len(bodky) >= 2:
            canvas.create_line(bodky[0], bodky[1], width=widthSlider.get(), fill=current_color)
            bodky.pop(0)
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
        shapes.append(s)

def handle_left_up(event):
    global bodky, shapes
    
    shapes = []
    bodky = []


canvas.bind_all("<Key>", handle_key_event)
# canvas.bind_all("<Button-1>", handle_left_click)
canvas.bind("<B1-Motion>", handle_left_click)
canvas.bind("<ButtonRelease>", handle_left_up)
# okno.bind("<Configure>", resize)

okno.mainloop()