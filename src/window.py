from tkinter import Tk, BOTH, Canvas
from cell import *

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Laberynth solver")
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
         
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
            
    def close(self):
        self.running = False
        
    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

