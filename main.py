import numpy as np
import random
from graphics import *

x_size = int(input("Podaj szerokość labiryntu (X): "))
y_size = int(input("Podaj wysokość labiryntu (Y): "))

STEP = 2
CELL_SIZE = 40
FRAME_RATE = 4

def clear(win):
    for item in win.items[:]:
        item.undraw()

def redraw(win, maze, framerate):
    clear(win)
    print_maze_graph(win, maze)
    update(framerate)

def clear_maze(cells):
    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            cells[x, y] = ' '

def fill_maze(cells):
    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            if x % 2 != 0 and y % 2 == 0:
                cells[x, y] = 'W'
            elif x % 2 == 0 and y % 2 != 0:
                cells[x, y] = 'W'
            else:
                cells[x, y] = ' '

def print_maze_graph(win, cells):
    pt_up_left = Point(0, 0)
    pt_up_right = Point(x_size*CELL_SIZE, 0)
    pt_down_left = Point(0, y_size*CELL_SIZE)
    pt_down_right = Point(x_size*CELL_SIZE, y_size * CELL_SIZE)
    ln = Line(pt_up_left, pt_up_right)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_up_right, pt_down_right)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_down_right, pt_down_left)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    ln = Line(pt_down_left, pt_up_left)
    ln.setOutline(color_rgb(0, 255, 255))
    ln.draw(win)

    for y in range(0, cells.shape[1]):
        for x in range(0, cells.shape[0]):
            if cells[x, y] == ' ':
                continue
            if x % 2 != 0 and y % 2 == 0:
                pt1 = Point((x//2+1)*CELL_SIZE, (y//2)*CELL_SIZE)
                pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                ln = Line(pt1, pt2)
                if cells[x, y] == 'C':
                    ln.setOutline('red')
                else:
                    ln.setOutline(color_rgb(0, 255, 255))
                ln.draw(win)
            elif x % 2 == 0 and y % 2 != 0:
                pt1 = Point((x//2)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                pt2 = Point((x//2+1)*CELL_SIZE, (y//2+1)*CELL_SIZE)
                ln = Line(pt1, pt2)
                if cells[x, y] == 'C':
                    ln.setOutline('red')
                else:
                    ln.setOutline(color_rgb(0, 255, 255))
                ln.draw(win)
            elif x % 2 == 0 and y % 2 == 0:
                pt1 = Point((x // 2) * CELL_SIZE+1, (y // 2) * CELL_SIZE+1)
                pt2 = Point((x // 2 + 1) * CELL_SIZE-1, (y // 2 + 1) * CELL_SIZE-1)
                rt = Rectangle(pt1, pt2)
                if cells[x, y] == 'C':
                    #rt.setOutline(color_rgb(0, 255, 0))
                    rt.setFill(color_rgb(0, 56, 0))
                    rt.draw(win)
                else:
                    try:
                        str(cells[x, y])
                    except ValueError:
                        continue
                    pt1.move(CELL_SIZE/2, CELL_SIZE/2)
                    label = Text(pt1, cells[x, y])
                    color = color_rgb(hash(cells[x, y]) % 256, hash(cells[x, y] + "1") % 256, hash(cells[x, y] + "2") % 256)
                    label.setOutline(color)
                    label.setFill(color)
                    label.setSize(CELL_SIZE//3)
                    label.draw(win)

def get_cell(cells, x, y):
    return cells[x*STEP-2, y*STEP-2]

def set_cell(cells, x, y, value):
    cells[x*STEP-2, y*STEP-2] = value

def set_wall(cells, x1, y1, x2, y2, value):
    if x1 != x2 and y1 != y2:
        print("ERROR: Column xor row must be the same")
        return
    if abs(x1-x2) > 1 or abs(y1-y2) > 1:
        print("ERROR: Cells must be neighbours")
        return

    if x1 - x2 < 0:
        cells[x1*STEP-1, y1*STEP-2] = value
    elif x1 - x2 > 0:
        cells[x2*STEP-1, y2*STEP-2] = value
    elif y1 - y2 < 0:
        cells[x1*STEP-2, y1*STEP-1] = value
    else:
        cells[x2*STEP-2, y2*STEP-1] = value

def eller(win, maze):
    def get_set(set_list, x_it, y_it):
        for set_it in set_list:
            if (x_it, y_it) in set_it:
                return set_it

    set_counter = 0
    sets = []

    for x in range(1, x_size + 1):
        new_set = set()
        sets.append(new_set)
        sets[-1].add((x, 1))
        set_counter = set_counter + 1
        set_cell(maze, x, 1, set_counter)

    for y in range(1, y_size+1):
        redraw(win, maze, FRAME_RATE)

        for x in range(1, x_size):
            if random.random() < 0.5 or y == y_size:
                sets_ready = 0
                for set_t in sets:
                    if (x, y) in set_t:
                        if (x+1, y) in set_t:
                            break
                        set_a = set_t
                        sets_ready = sets_ready + 1
                    elif (x+1, y) in set_t:
                        set_b = set_t
                        sets_ready = sets_ready + 1
                    if sets_ready == 2:
                        break
                if sets_ready == 2:
                    sets.remove(set_a)
                    sets.remove(set_b)
                    set_a = set_a.union(set_b)
                    sets.append(set_a)
                    for val in set_a:
                        set_cell(maze, val[0], val[1], get_cell(maze, x, y))
                    set_wall(maze, x, y, x + 1, y, ' ')
        if y == y_size:
            return
        processed_sets = set()
        x_range = list(range(1, x_size+1))
        random.shuffle(x_range)
        for x in x_range:
            if (get_cell(maze, x, y) not in processed_sets) or random.random() < 0.5:
                processed_sets.add(get_cell(maze, x, y))
                set_wall(maze, x, y, x, y+1, ' ')
                set_cell(maze, x, y + 1, get_cell(maze, x, y))
                set_a = get_set(sets, x, y)
                sets.remove(set_a)
                set_a.add((x, y+1))
                sets.append(set_a)
            else:
                new_set = set()
                sets.append(new_set)
                sets[-1].add((x, y+1))
                set_counter = set_counter + 1
                set_cell(maze, x, y+1, set_counter)

# raw maze, filled with 0's
maze = np.zeros(shape=(x_size*2-1, y_size*2-1)).astype(str)

win = GraphWin("window", x_size*CELL_SIZE+1, y_size*CELL_SIZE+1, autoflush=False)
win.setBackground(color_rgb(0, 0, 0))

random.seed(a=3)

clear_maze(maze)
fill_maze(maze)
eller(win, maze)
redraw(win, maze, FRAME_RATE)

win.getMouse()
win.close()
