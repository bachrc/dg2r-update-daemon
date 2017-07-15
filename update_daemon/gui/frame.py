import os
import tkinter as tk
from copy import copy
from queue import Queue, LifoQueue
from tkinter.font import Font

from PIL import Image, ImageTk

from update_daemon import STATE
from update_daemon.threads import Update


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


class Application(tk.Tk):

    def __init__(self, app_state):
        super().__init__()
        self.overrideredirect(True)

        # self.attributes('-fullscreen', True)

        # w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.w, self.h = 800, 480

        self.canvas = tk.Canvas(self, width=self.w, height=self.h, highlightthickness=0)
        vertical_gradient_rectangle(self.canvas, 0, 0, self.w, self.h, 242, 242, 255, 178, 212, 242)
        self.canvas.pack(fill='both')

        self.image = Image.open("%s/dg2r.png" % os.path.dirname(__file__))
        self.image.thumbnail((int(self.w / 2), int(self.h / 3)))
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.canvas.create_image(self.w / 2, self.h / 4, anchor=tk.CENTER, image=self.image_tk)

        self.canvas.create_text(self.w / 2, self.h * 0.7,
                                anchor=tk.CENTER,
                                text="Bienvenue dans l'utilitaire de mise à jour DG2R.",
                                fill="#1370FF",
                                justify=tk.CENTER,
                                font=Font(weight="bold", size=20),
                                width=self.w*0.9)

        self.update_state = app_state

        self.status_text = self.canvas.create_text(self.w / 2, self.h,
                                                   anchor=tk.CENTER,
                                                   text="Salut je suis caché",
                                                   fill="#1370FF",
                                                   justify=tk.CENTER,
                                                   font=Font(size=18),
                                                   width=self.w * 0.9)

        _, y1, _, y2 = self.canvas.bbox(self.status_text)
        self.text_height = y2 - y1

        self.canvas.move(self.status_text, 0, int(self.text_height/2))
        self.canvas.after(2000, self.waiting_for_update)


    def waiting_for_update(self):


        self.canvas.itemconfig(self.status_text, text="La mise à jour va commencer.")
        self.move(self.status_text, self.h - self.text_height, 1, 5,
                  callback=lambda: self.after(2000, self.place_loading))

    def place_loading(self):
        def go_up():
            self.canvas.itemconfig(self.status_text, text="Veuillez patienter")
            self.move(self.status_text, self.h - self.text_height, 1, 5,
                      callback=self.animate_dot)

        self.update_state.put(STATE.UPDATING)
        self.after(1000, lambda: self.move(self.status_text, self.h + self.text_height, 1, 5,
                                           callback=go_up))

    def animate_dot(self, dot=0):
        if self.update_state.queue[-1] in (STATE.UPDATING, STATE.DISPLAYING):
            self.canvas.itemconfig(self.status_text, text="Veuillez patienter%s" % ("." * dot))
            self.after(500, lambda: self.animate_dot((dot + 1) % 4))
        else:
            print("NON YA PU")


    def move(self, text_id, destination_y, step, speed, callback=None):
        x, y = self.canvas.coords(text_id)
        distance = abs(y - destination_y)

        way = 1 if y < destination_y else -1

        if distance == 0:
            if callback is not None:
                callback()
        elif distance < step:
            self.canvas.move(text_id, 0, (step * way))

            if callback is not None:
                callback()
        else:
            self.canvas.move(text_id, 0, (step * way))
            self.canvas.after(speed, lambda: self.move(text_id, destination_y, step, speed, callback))


if __name__ == '__main__':
    q = LifoQueue()
    q.put(STATE.DISPLAYING)

    th_update = Update(q)
    th_update.start()

    app = Application(q)

    app.mainloop()