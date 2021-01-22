import math
import random
from collections import deque


def astar_solver(maze_graphics, maze, start_x, start_y, end_x, end_y):

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

        neighbours = maze.get_cell_open_neighbours(x, y)

        for neighbour in neighbours:
            g_score_tmp = g_score[(x, y)] + 1

            if ((neighbour[0], neighbour[1]) not in g_score) or g_score_tmp < g_score[neighbour[0], neighbour[1]]:
                came_from[(neighbour[0], neighbour[1])] = (x, y)
                g_score[(neighbour[0], neighbour[1])] = g_score_tmp
                f_score[(neighbour[0], neighbour[1])] = g_score_tmp + heur(neighbour[0], neighbour[1], end_x, end_y)

                if (neighbour[0], neighbour[1]) not in open_set:
                    open_set.append((neighbour[0], neighbour[1]))

    return None



def bfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y):

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

        neighbours = maze.get_cell_open_neighbours(current[0], current[1])

        for neighbour in neighbours:

            if (neighbour[0], neighbour[1]) not in visited:
                q.append((neighbour[0], neighbour[1]))
                came_from[(neighbour[0], neighbour[1])] = current

    return None



def dfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y):

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
        neighbours = maze.get_cell_open_neighbours(current[0], current[1])

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



def dfs_iterative_base_solver(maze_graphics, maze, start_x, start_y, end_x, end_y, max_depth):

    if max_depth < 1:
        return None

    q = deque()
    current = (start_x, start_y)
    q.append(current)
    visited = set()
    visited.add(current)

    while q:
        current = q[-1]

        if current[0] == end_x and current[1] == end_y:
            return list(q)

        if len(q) == max_depth:
            q.pop()
            continue

        not_visited_neighbours = []
        neighbours = maze.get_cell_open_neighbours(current[0], current[1])

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



def dfs_iterative_solver(maze_graphics, maze, start_x, start_y, end_x, end_y):

    max_length = 1
    maze_shape = maze.cells.shape

    for item in maze_shape:
        max_length *= (item + 1) // 2

    min_length = (end_x - start_x) + (end_y - start_y) + 1

    for i in range(min_length, max_length + 1):
        solution = dfs_iterative_base_solver(maze_graphics, maze, start_x, start_y, end_x, end_y, i)

        if solution is not None:
            return solution

    return None



def general_solver(algorithm, maze_graphics, maze, start_x, start_y, end_x, end_y):

    if algorithm == "A*":
        return astar_solver(maze_graphics, maze, start_x, start_y, end_x, end_y)
    elif algorithm == "bfs":
        return bfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y)
    elif algorithm == "dfs":
        return dfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y)
    elif algorithm == "dfs iterative":
        return dfs_iterative_solver(maze_graphics, maze, start_x, start_y, end_x, end_y)

    return None