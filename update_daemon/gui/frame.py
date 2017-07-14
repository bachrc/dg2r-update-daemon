import os
import tkinter as tk
from PIL import Image, ImageTk


def vertical_gradient_rectangle(canvas, x0, y0, x1, y1, start_red, start_green, start_blue, end_red, end_green, end_blue):
    y = y0
    while y <= y1:
        # fade the three color components depending on the y coordinate
        # note that integer division works fine here: why?
        red = int((start_red*(y1 - y) + end_red*(y - y0)) / (y1 - y0))
        green = int((start_green*(y1 - y) + end_green*(y - y0)) / (y1 - y0))
        blue = int((start_blue*(y1 - y) + end_blue*(y - y0)) / (y1 - y0))
        # create a hexadecimal color representation
        color = "#%02x%02x%02x" % (red, green, blue)

        # create a colored horizontal line at position y
        canvas.create_line(x0, y, x1, y, fill=color)
        y += 1


class Logo(tk.Frame):
    def __init__(self, width, height, master=None):
        super().__init__(master=master)
        self.parent = master

        canvas = tk.Canvas(master, width=width, height=(height/2))
        image = Image.open("%s/dg2r.png" % os.path.dirname(__file__))

        image.thumbnail((int(width/2), int(height/4)))
        image_tk = ImageTk.PhotoImage(image)

        canvas.create_image(width / 2, height / 4, anchor=tk.CENTER, image=image_tk)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)

        # self.attributes('-fullscreen', True)

        # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 800, 500

        self.canvas = tk.Canvas(self, width=w, height=h, highlightthickness=0)
        vertical_gradient_rectangle(self.canvas, 0, 0, w, h, 242, 242, 255, 178, 212, 242)
        self.canvas.pack(fill='both')

        self.image = Image.open("%s/dg2r.png" % os.path.dirname(__file__))
        self.image.thumbnail((int(w / 2), int(h / 4)))
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.canvas.create_image(w / 2, h / 4, anchor=tk.CENTER, image=self.image_tk)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
