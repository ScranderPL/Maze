import random
import maze_solver

def decode(maze_graphics, maze, seed):

    random.seed(seed)
    answer = ""

    start_points = []
    paths = []
    path_cells = set()
    start_points.append(maze.random_start(W=2))
    start_points.append(maze.random_start(W=4))

    end_x, end_y = maze.random_start(W=1)

    for start_x, start_y in start_points:
        path = maze_solver.bfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y)
        paths.append(path)
        path_cells.update(path)

    embeddable_neighbours = set()

    for path in paths:
        for (curr_x, curr_y) in path:

            if curr_x == 1 or curr_x == maze.x_size or curr_y == 1 or curr_y == maze.y_size:
                continue

            neighbours = maze.get_cell_neighbours_outside_set(curr_x, curr_y, path_cells)

            if len(neighbours) != 2:
                continue

            if neighbours[0] in embeddable_neighbours \
                or neighbours[1] in embeddable_neighbours:
                continue

            current = ""

            if maze.get_wall(curr_x, curr_y, neighbours[0][0], neighbours[0][1]) == " ":
                current += "0"

            if maze.get_wall(curr_x, curr_y, neighbours[1][0], neighbours[1][1]) == " ":
                current += "1"

            if len(current) == 1:
                answer += current

            embeddable_neighbours.add(neighbours[0])
            embeddable_neighbours.add(neighbours[1])

    return answer