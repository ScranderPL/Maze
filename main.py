import math

import numpy as np
import random
from graphics import *
import time

x_size = int(input("Insert X size: "))
y_size = int(input("Insert Y size: "))
print("1. Recursive backtracker")
print("2. Hunt and kill")
print("3. Eller's algorithm")
algorithm = int(input("Choose algorithm: "))
STEP = 2
CELL_SIZE = 50
FRAME_RATE = 30



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
                    rt.setOutline(color_rgb(0, 255, 0))
                    rt.setFill(color_rgb(0, 255, 0))
                    rt.draw(win)
                else:
                    try:
                        int(cells[x, y])
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


def get_cell_not_visited_neighbours(cells, x, y):
    neighbours = []
    if x > 1:
        neighbour = get_cell(cells, x-1, y)
        if neighbour != 'V':
            neighbours.append([x-1, y])
    if x < x_size:
        neighbour = get_cell(cells, x+1, y)
        if neighbour != 'V':
            neighbours.append([x+1, y])
    if y > 1:
        neighbour = get_cell(cells, x, y-1)
        if neighbour != 'V':
            neighbours.append([x, y-1])
    if y < y_size:
        neighbour = get_cell(cells, x, y+1)
        if neighbour != 'V':
            neighbours.append([x, y+1])
    return neighbours

def get_cell_open_neighbours(cells, x, y):
    neighbours = []
    if x > 1:
        if get_wall(cells, x, y, x-1, y) == ' ':
            neighbours.append([x-1, y])
    if x < x_size:
        if get_wall(cells, x, y, x+1, y) == ' ':
            neighbours.append([x+1, y])
    if y > 1:
        if get_wall(cells, x, y, x, y-1) == ' ':
            neighbours.append([x, y-1])
    if y < y_size:
        if get_wall(cells, x, y, x, y+1) == ' ':
            neighbours.append([x, y+1])
    return neighbours


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

def get_wall(cells, x1, y1, x2, y2):
    if x1 != x2 and y1 != y2:
        print("ERROR: Column xor row must be the same")
        return
    if abs(x1-x2) > 1 or abs(y1-y2) > 1:
        print("ERROR: Cells must be neighbours")
        return

    if x1 - x2 < 0:
        return cells[x1*STEP-1, y1*STEP-2]
    elif x1 - x2 > 0:
        return cells[x2*STEP-1, y2*STEP-2]
    elif y1 - y2 < 0:
        return cells[x1*STEP-2, y1*STEP-1]
    else:
        return cells[x2*STEP-2, y2*STEP-1]


def recursive_backtracker(win, maze):
    visited_stack = []

    init_x = random.randint(1, x_size)
    init_y = random.randint(1, y_size)

    visited_stack.append([init_x, init_y])
    set_cell(maze, init_x, init_y, 'V')

    while visited_stack:
        current_cell = visited_stack.pop()
        set_cell(maze, current_cell[0], current_cell[1], 'C')
        neighbours = get_cell_not_visited_neighbours(maze, current_cell[0], current_cell[1])
        if not neighbours:
            redraw(win, maze, FRAME_RATE)
            set_cell(maze, current_cell[0], current_cell[1], 'V')
            continue
        visited_stack.append(current_cell)
        chosen_neighbour = random.choice(neighbours)
        set_wall(maze, current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], 'C')
        set_cell(maze, chosen_neighbour[0], chosen_neighbour[1], 'V')
        visited_stack.append(chosen_neighbour)

        redraw(win, maze, FRAME_RATE)
        set_wall(maze, current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], ' ')
        set_cell(maze, current_cell[0], current_cell[1], 'V')



def hunt_and_kill(win, maze):
    def hunt_and_kill_scan(win, maze):
        for y in range(1, y_size + 1):
            for x in range(1, x_size + 1):
                tmp_cell = get_cell(maze, x, y)
                if tmp_cell == 'V':
                    neighbours = get_cell_not_visited_neighbours(maze, x, y)
                    if not neighbours:
                        continue
                    return [x, y], random.choice(neighbours)
        return None, None
    curr_x = random.randint(1, x_size)
    curr_y = random.randint(1, y_size)
    curr_cell = [curr_x, curr_y]
    while True:
        set_cell(maze, curr_cell[0], curr_cell[1], 'V')
        neighbours = get_cell_not_visited_neighbours(maze, curr_cell[0], curr_cell[1])
        if not neighbours:
            curr_cell, next_cell = hunt_and_kill_scan(win, maze)
            if not curr_cell:
                return
        else:
            next_cell = random.choice(neighbours)
        set_wall(maze, curr_cell[0], curr_cell[1], next_cell[0], next_cell[1], ' ')
        curr_cell = next_cell



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

def astar_solver(win, maze, start_x, start_y, end_x, end_y):
    def reconstruct_path(cameFrom, x_curr, y_curr):
        total_path = [(x_curr, y_curr)]
        while (x_curr, y_curr) in cameFrom:
            (x_curr, y_curr) = cameFrom[(x_curr, y_curr)]
            total_path.insert(0, (x_curr, y_curr))
        return total_path

    def heur(x_from, y_from, x_to, y_to):
        return math.sqrt((x_from - x_to) ** 2 + (y_from - y_to) ** 2)

    open_set = []
    came_from = {}

    g_score = {}
    f_score = {}

    open_set.append((start_x, start_y))
    g_score[(start_x, start_y)] = 0
    f_score[(start_x, start_y)] = heur(start_x, start_y, end_x, end_y)

    while open_set:
        (x, y) = min(f_score.keys() & open_set, key=f_score.get)
        if x == end_x and y == end_y:
            return reconstruct_path(came_from, x, y)

        open_set.remove((x, y))

        neighbours = get_cell_open_neighbours(maze, x, y)
        for neighbour in neighbours:
            g_score_tmp = g_score[(x, y)] + 1
            if ((neighbour[0], neighbour[1]) not in g_score) or g_score_tmp < g_score[neighbour[0], neighbour[1]]:
                came_from[(neighbour[0], neighbour[1])] = (x, y)
                g_score[(neighbour[0], neighbour[1])] = g_score_tmp
                f_score[(neighbour[0], neighbour[1])] = g_score_tmp + heur(neighbour[0], neighbour[1], end_x, end_y)
                if (neighbour[0], neighbour[1]) not in open_set:
                    open_set.append((neighbour[0], neighbour[1]))

    return None

from collections import deque

def bfs_solver(win, maze, start_x, start_y, end_x, end_y):
    def reconstruct_path(cameFrom, x_curr, y_curr):
        total_path = [(x_curr, y_curr)]
        while (x_curr, y_curr) in cameFrom:
            (x_curr, y_curr) = cameFrom[(x_curr, y_curr)]
            total_path.insert(0, (x_curr, y_curr))
        return total_path
        
    q = deque()
    q.append((start_x, start_y))
    came_from = {}
    visited = set()
    
    while q:
        current = q.popleft()
        visited.add(current)
        if current[0] == end_x and current[1] == end_y:
            return reconstruct_path(came_from, current[0], current[1])
        
        neighbours = get_cell_open_neighbours(maze, current[0], current[1])
        for neighbour in neighbours:
            if (neighbour[0], neighbour[1]) not in visited:
                q.append((neighbour[0], neighbour[1]))
                came_from[(neighbour[0], neighbour[1])] = current
    
    return None
    
def dfs_solver(win, maze, start_x, start_y, end_x, end_y):
    q = deque()
    current = (start_x, start_y)
    q.append(current)
    visited = set()
    visited.add(current)
    
    
    while q:
        current = q[-1]
        if current[0] == end_x and current[1] == end_y:
            return list(q)
        
        not_visited_neighbours = []
        neighbours = get_cell_open_neighbours(maze, current[0], current[1])

        for neighbour in neighbours:
            if (neighbour[0], neighbour[1]) not in visited:
                not_visited_neighbours.append((neighbour[0], neighbour[1]))

        if not_visited_neighbours:
            new_item = random.choice(not_visited_neighbours)
            q.append(new_item)
            visited.add(new_item)
        else:
            q.pop()
    
    return None

maze = np.zeros(shape=(x_size*2-1, y_size*2-1)).astype(str)

win = GraphWin("ss", x_size*CELL_SIZE+1, y_size*CELL_SIZE+1, autoflush=False)
win.setBackground(color_rgb(0, 0, 0))

random.seed(a=3)

clear_maze(maze)
fill_maze(maze)

if algorithm == 1:
    recursive_backtracker(win, maze)
elif algorithm == 2:
    hunt_and_kill(win, maze)
elif algorithm == 3:
    eller(win, maze)

redraw(win, maze, FRAME_RATE)

print("A* start solution:")
start = time.time()
print(astar_solver(win, maze, 1, 1, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))
print("BFS solution:")
start = time.time()
print(bfs_solver(win, maze, 1, 1, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))
print("DFS solution:")
start = time.time()
print(dfs_solver(win, maze, 1, 1, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))



win.getMouse()
win.close()

