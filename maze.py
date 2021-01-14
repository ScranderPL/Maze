from graphics import *
import numpy as np
import random


CELL_SIZE = 40
FRAME_RATE = 1
STEP = 2


class Maze:

    def __init__(self, x_size, y_size):

        self.x_size = x_size
        self.y_size = y_size
        self.cells = np.zeros(shape=(x_size*2-1, y_size*2-1)).astype(str)


    def clear(self):

        for y in range(0, self.cells.shape[1]):
            for x in range(0, self.cells.shape[0]):
                self.cells[x, y] = ' '


    def fill(self):

        for y in range(0, self.cells.shape[1]):
            for x in range(0, self.cells.shape[0]):
                if x % 2 != 0 and y % 2 == 0:
                    self.cells[x, y] = 'W'
                elif x % 2 == 0 and y % 2 != 0:
                    self.cells[x, y] = 'W'
                else:
                    self.cells[x, y] = ' '

    def hunt_and_kill_fill(self):

        for y in range(0, self.cells.shape[1]):
            for x in range(0, self.cells.shape[0]):
                if x % 2 != 0 and y % 2 == 0:
                    self.cells[x, y] = 'W'
                elif x % 2 == 0 and y % 2 != 0:
                    self.cells[x, y] = 'W'
                else:
                    self.cells[x, y] = 'O'


    def get_cell(self, x, y):

        return self.cells[x*STEP-2, y*STEP-2]


    def random_start(self, W = 0):

        if W == 0:
            wall_chosen = random.randint(1, 4)
        else:
            wall_chosen = W

        if wall_chosen == 1:
            rand_x = 1
            rand_y = random.randint(1, self.y_size)
        elif wall_chosen == 2:
            rand_x = self.x_size
            rand_y = random.randint(1, self.y_size)
        elif wall_chosen == 3:
            rand_x = random.randint(1, self.x_size)
            rand_y = 1
        else:
            rand_x = random.randint(1, self.x_size)
            rand_y = self.y_size

        return rand_x, rand_y


    def get_cell_not_visited_neighbours(self, x, y):

        neighbours = []

        if x > 1:
            neighbour = self.get_cell(x-1, y)
            if neighbour != 'V':
                neighbours.append([x-1, y])

        if x < self.x_size:
            neighbour = self.get_cell(x+1, y)
            if neighbour != 'V':
                neighbours.append([x+1, y])

        if y > 1:
            neighbour = self.get_cell(x, y-1)
            if neighbour != 'V':
                neighbours.append([x, y-1])

        if y < self.y_size:
            neighbour = self.get_cell(x, y+1)
            if neighbour != 'V':
                neighbours.append([x, y+1])

        return neighbours


    def get_cell_open_neighbours(self, x, y):

        neighbours = []

        if x > 1:
            if self.get_wall(x, y, x-1, y) == ' ':
                neighbours.append([x-1, y])

        if x < self.x_size:
            if self.get_wall(x, y, x+1, y) == ' ':
                neighbours.append([x+1, y])

        if y > 1:
            if self.get_wall(x, y, x, y-1) == ' ':
                neighbours.append([x, y-1])

        if y < self.y_size:
            if self.get_wall(x, y, x, y+1) == ' ':
                neighbours.append([x, y+1])

        return neighbours


    def set_cell(self, x, y, value):

        self.cells[x*STEP-2, y*STEP-2] = value


    def set_wall(self, x1, y1, x2, y2, value):

        if x1 != x2 and y1 != y2:
            print("ERROR: Column xor row must be the same")
            return

        if abs(x1-x2) > 1 or abs(y1-y2) > 1:
            print("ERROR: Cells must be neighbours")
            return

        if x1 - x2 < 0:
            self.cells[x1*STEP-1, y1*STEP-2] = value
        elif x1 - x2 > 0:
            self.cells[x2*STEP-1, y2*STEP-2] = value
        elif y1 - y2 < 0:
            self.cells[x1*STEP-2, y1*STEP-1] = value
        else:
            self.cells[x2*STEP-2, y2*STEP-1] = value


    def get_wall(self, x1, y1, x2, y2):

        if x1 != x2 and y1 != y2:
            print("ERROR: Column xor row must be the same")
            return

        if abs(x1-x2) > 1 or abs(y1-y2) > 1:
            print("ERROR: Cells must be neighbours")
            return

        if x1 - x2 < 0:
            return self.cells[x1*STEP-1, y1*STEP-2]
        elif x1 - x2 > 0:
            return self.cells[x2*STEP-1, y2*STEP-2]
        elif y1 - y2 < 0:
            return self.cells[x1*STEP-2, y1*STEP-1]
        else:
            return self.cells[x2*STEP-2, y2*STEP-1]


    def get_cell_neighbours_outside_set(self, x, y, values_set):

        neighbours = []

        if x > 1:
            if (x-1, y) not in values_set:
                neighbours.append((x-1, y))

        if x < self.x_size:
            if (x+1, y) not in values_set:
                neighbours.append((x+1, y))

        if y > 1:
            if (x, y-1) not in values_set:
                neighbours.append((x, y-1))

        if y < self.y_size:
            if (x, y+1) not in values_set:
                neighbours.append((x, y+1))

        return neighbours

    def get_cell_neighbours(self, x, y, value):

        neighbours = []

        if x > 1:
            neighbour = self.get_cell(x-1, y)
            if neighbour == value:
                neighbours.append([x-1, y])

        if x < self.x_size:
            neighbour = self.get_cell(x+1, y)
            if neighbour == value:
                neighbours.append([x+1, y])

        if y > 1:
            neighbour = self.get_cell(x, y-1)
            if neighbour == value:
                neighbours.append([x, y-1])

        if y < self.y_size:
            neighbour = self.get_cell(x, y+1)
            if neighbour == value:
                neighbours.append([x, y+1])

        return neighbours



class MazeGraphics:

    def __init__(self, x_size, y_size):

        self.win = GraphWin("ss", x_size*CELL_SIZE+1, y_size*CELL_SIZE+1, autoflush=False)
        self.win.setBackground(color_rgb(0, 0, 0))

    def clear(self):

        for item in self.win.items[:]:
            item.undraw()

    def redraw(self, maze, framerate = FRAME_RATE):

        self.clear()
        self.print_maze_graph(maze)
        update(framerate)

    def destroy(self):

        self.win.getMouse()
        self.win.close()

    def print_maze_graph(self, maze):

        pt_up_left = Point(0, 0)
        pt_up_right = Point(maze.x_size*CELL_SIZE, 0)
        pt_down_left = Point(0, maze.y_size*CELL_SIZE)
        pt_down_right = Point(maze.x_size*CELL_SIZE, maze.y_size * CELL_SIZE)
        ln = Line(pt_up_left, pt_up_right)
        ln.setOutline(color_rgb(0, 255, 255))
        ln.draw(self.win)

        ln = Line(pt_up_right, pt_down_right)
        ln.setOutline(color_rgb(0, 255, 255))
        ln.draw(self.win)

        ln = Line(pt_down_right, pt_down_left)
        ln.setOutline(color_rgb(0, 255, 255))
        ln.draw(self.win)

        ln = Line(pt_down_left, pt_up_left)
        ln.setOutline(color_rgb(0, 255, 255))
        ln.draw(self.win)

        for y in range(0, maze.cells.shape[1]):
            for x in range(0, maze.cells.shape[0]):

                if maze.cells[x, y] == ' ':
                    continue

                if x % 2 != 0 and y % 2 == 0:
                    pt1 = Point((x//2+1)*CELL_SIZE, (y//2)*CELL_SIZE)
                    pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                    ln = Line(pt1, pt2)

                    if maze.cells[x, y] == 'C':
                        ln.setOutline('red')
                    else:
                        ln.setOutline(color_rgb(0, 255, 255))

                    ln.draw(self.win)
                elif x % 2 == 0 and y % 2 != 0:
                    pt1 = Point((x//2)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                    pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                    ln = Line(pt1, pt2)

                    if maze.cells[x, y] == 'C':
                        ln.setOutline('red')
                    else:
                        ln.setOutline(color_rgb(0, 255, 255))

                    ln.draw(self.win)
                elif x % 2 == 0 and y % 2 == 0:
                    pt1 = Point((x // 2) * CELL_SIZE+1, (y // 2) * CELL_SIZE+1)
                    pt2 = Point((x // 2 + 1) * CELL_SIZE-1, (y // 2 + 1) * CELL_SIZE-1)
                    rt = Rectangle(pt1, pt2)

                    if maze.cells[x, y] == 'C':
                        #rt.setOutline(color_rgb(0, 255, 0))
                        rt.setFill(color_rgb(0, 56, 0))
                        rt.draw(self.win)
                    else:

                        try:
                            str(maze.cells[x, y])
                        except ValueError:
                            continue

                        pt1.move(CELL_SIZE/2, CELL_SIZE/2)
                        label = Text(pt1, maze.cells[x, y])
                        color = color_rgb(hash(maze.cells[x, y]) % 256, hash(maze.cells[x, y] + "1") % 256, hash(maze.cells[x, y] + "2") % 256)
                        label.setOutline(color)
                        label.setFill(color)
                        label.setSize(CELL_SIZE//3)
                        label.draw(self.win)