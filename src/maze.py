from cell import Cell
import time
import random

class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
            seed = None,
        ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.visited = False
        
        if seed is not None:
            random.seed(seed)
                
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        for j in range(self.num_rows):
            col_cells = []
            for i in range(self.num_cols):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for j in range(self.num_rows):
            for i in range(self.num_cols):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        cell = self.cells[j][i]
        x1 = (self.x1 * i) + self.cell_size_x
        x2 = x1 + self.cell_size_x
        y1 = (self.y1 * j) + self.cell_size_y
        y2 = y1 + self.cell_size_y
        cell.draw(x1, y1, x2, y2)
        self._animate()
        
    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self.cells[self.num_rows- 1][self.num_cols - 1].has_bottom_wall = False
        self.cells[self.num_rows- 1][self.num_cols - 1].has_top_wall = True
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)
    
    def _break_walls_r(self, i, j):
        self.cells[j][i].visited = True
        while True:
            next_index = []
            # left
            if i > 0 and not self.cells[j][i - 1].visited:
                next_index.append((i - 1, j))
            # right
            if i < self.num_cols - 1 and not self.cells[j][i + 1].visited:
                next_index.append((i + 1, j))
            # up
            if j > 0 and not self.cells[j - 1][i].visited:
                next_index.append((i, j - 1))
            # down
            if j < self.num_rows - 1 and not self.cells[j + 1][i].visited:
                next_index.append((i, j + 1))
            
            # if there is nowhere to go from here break out
            if len(next_index) == 0:
                self._draw_cell(i, j)
                return

            #randomly choose the next directioin to go
            direction = random.randrange(len(next_index))
            next = next_index[direction]
            
            # knock down walls
            #right
            if next[0] == i + 1:
                self.cells[j][i].has_right_wall = False
                self.cells[j][i + 1].has_left_wall = False
            # left
            if next[0] == i - 1:
                self.cells[j][i].has_left_wall = False
                self.cells[j][i - 1].has_right_wall = False
            # up
            if next[1] == j - 1:
                self.cells[j][i].has_top_wall = False
                self.cells[j - 1][i].has_bottom_wall = False
            # down
            if next[1] == j + 1:
                self.cells[j][i].has_bottom_wall = False
                self.cells[j + 1][i].has_top_wall = False
                
            # recursively visit the next cell
            self._break_walls_r(next[0], next[1])
                
    def _reset_cells_visited(self):
        for j in range(len(self.cells)):
            for i in range(len(self.cells[0])):
                self.cells[j][i].visited = False
    
    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()

        # visit current cell
        self.cells[j][i].visited = True
        # if end cell we are out of the maze
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # move left if possible and it hasnt been visited
        if (
            i > 0
            and self.cells[j][i].has_left_wall == False
            and self.cells[j][i - 1].visited == False
        ):
            self.cells[j][i].draw_move(self.cells[j][i - 1])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.cells[j][i].draw_move(self.cells[j][i - 1], True)

        # move right if possible and it hasnt been visited
        if (
            i < self.num_cols - 1
            and self.cells[j][i].has_right_wall == False
            and self.cells[j][i + 1].visited == False
        ):
            self.cells[j][i].draw_move(self.cells[j][i + 1])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.cells[j][i].draw_move(self.cells[j][i + 1], True)

        # move up if possible and it hasnt been visited
        if (
            j > 0
            and self.cells[j][i].has_top_wall == False
            and self.cells[j - 1][i].visited == False
        ):
            self.cells[j][i].draw_move(self.cells[j - 1][i])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.cells[j][i].draw_move(self.cells[j - 1][i], True)

        # move down if possible and it hasnt been visited
        if (
            j < self.num_rows - 1
            and self.cells[j][i].has_bottom_wall == False
            and self.cells[j + 1][i].visited == False
        ):
            self.cells[j][i].draw_move(self.cells[j + 1][i])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.cells[j][i].draw_move(self.cells[j + 1][i], True)

        # We did not reach the end and no more moves are possible
        return False

    def _animate(self):
        self.win.redraw()
        time.sleep(0.025)
    