class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
class Line():
    def __init__(self, point_a, point_b):
        self.a = point_a
        self.b = point_b
        
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2
        )
        
class Cell():
    def __init__(self, win):
        self.has_left_wall = True 
        self.has_right_wall = True 
        self.has_top_wall = True 
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1  = None
        self._y2 = None
        self._win = win
        self.visited = False
        
    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
            
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")
            
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
            
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")
            
    def draw_move(self, to_cell, undo=False):
        start_point = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        end_point = Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)
        color = "red" if not undo else "gray"
        line = Line(start_point, end_point)
        self._win.draw_line(line, color)
    
    def __str__(self):
        return f"""
                Left wall: {self.has_left_wall}
                Top wall: {self.has_top_wall}
                Right wall: {self.has_right_wall}
                Bottom wall: {self.has_bottom_wall}
            """
            