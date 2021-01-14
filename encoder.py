import random
import maze_generator
import maze_solver
import itertools


def encode(maze_graphics, maze, message, seed):
    # choose n start points
    # order is important (set with seed)

    # required for step 8
    random.seed(seed)
    embeddable_cells = []

    maze_graphics.redraw(maze)
    input("Press enter to continue")

    # step 2
    start_points = []
    paths = []
    start_points.append(maze.random_start(W=2))
    start_points.append(maze.random_start(W=4))

    end_x, end_y = maze.random_start(W=1)

    for start_x, start_y in start_points:
        paths.append(maze_solver.bfs_solver(maze_graphics, maze, start_x, start_y, end_x, end_y))

    maze_graphics.redraw(maze)
    input("Press enter to continue")

    # step 3
    maze.hunt_and_kill_fill()

    for path in paths:
        prev_x, prev_y = None, None

        for (x, y) in path:

            if prev_x:
                maze.set_wall(x, y, prev_x, prev_y, ' ')

            maze.set_cell(x, y, 'I')
            prev_x, prev_y = x, y

    maze_graphics.redraw(maze)
    input("Press enter to continue")

    # step 4
    embeddable_o_neighbours = set()
    for path in paths:
        for (curr_x, curr_y) in path:

            if curr_x == 1 or curr_x == maze.x_size or curr_y == 1 or curr_y == maze.y_size:
                continue

            neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'O')

            if len(neighbours) != 2:
                continue

            if ((neighbours[0][0],neighbours[0][1]) in embeddable_o_neighbours) \
                or ((neighbours[1][0],neighbours[1][1]) in embeddable_o_neighbours):
                continue

            maze.set_cell(neighbours[0][0], neighbours[0][1], 'O0')
            maze.set_cell(neighbours[1][0], neighbours[1][1], 'O1')
            embeddable_cells.append((curr_x, curr_y))
            embeddable_o_neighbours.add((neighbours[0][0],neighbours[0][1]))
            embeddable_o_neighbours.add((neighbours[1][0],neighbours[1][1]))

    maze_graphics.redraw(maze)
    input("Press enter to continue")

    # step 5
    message_counter = 0

    for embeddable_cell in embeddable_cells:
        curr_x = embeddable_cell[0]
        curr_y = embeddable_cell[1]

        neighbours_o0 = maze.get_cell_neighbours(curr_x, curr_y, 'O0')
        neighbours_o1 = maze.get_cell_neighbours(curr_x, curr_y, 'O1')
        neighbour_o0 = neighbours_o0[0]
        neighbour_o1 = neighbours_o1[0]


        if message_counter < len(message):
            curr_bit = message[message_counter]

            if curr_bit == '1':
                maze.set_cell(neighbour_o0[0], neighbour_o0[1], 'D')
                maze.set_cell(neighbour_o1[0], neighbour_o1[1], 'I')
                maze.set_wall(curr_x, curr_y, neighbour_o1[0], neighbour_o1[1], ' ')
            else:
                maze.set_cell(neighbour_o1[0], neighbour_o1[1], 'D')
                maze.set_cell(neighbour_o0[0], neighbour_o0[1], 'I')
                maze.set_wall(curr_x, curr_y, neighbour_o0[0], neighbour_o0[1], ' ')
            message_counter = message_counter + 1

        else:

            maze.set_wall(curr_x, curr_y, neighbour_o0[0], neighbour_o0[1], ' ')
            maze.set_wall(curr_x, curr_y, neighbour_o1[0], neighbour_o1[1], ' ')
            maze.set_cell(neighbour_o0[0], neighbour_o0[1], 'I')
            maze.set_cell(neighbour_o1[0], neighbour_o1[1], 'I')

    maze_graphics.redraw(maze)
    input("Press enter to continue")

    # step 6
    for (curr_x, curr_y) in itertools.product(range(1, maze.x_size+1),range(1, maze.y_size+1)):

        if maze.get_cell(curr_x, curr_y) != 'I':
            continue

        neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'O')

        for neigh_x, neigh_y in neighbours:
            maze.set_cell(neigh_x, neigh_y, 'F')

    maze_graphics.redraw(maze)
    input()

    while True:
        # step 7
        maze_generator.hunt_and_kill_mod(maze_graphics, maze, reuse=True)

        # step 8
        d_exist = False

        for (curr_x, curr_y) in itertools.product(range(1, maze.x_size + 1), range(1, maze.y_size + 1)):

            if maze.get_cell(curr_x, curr_y) != 'D':
                continue

            neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'I')

            unemb_i_exist = False

            for x, y in neighbours:

                if (x, y) in embeddable_cells:
                    continue

                unemb_i_exist = True
                found_x, found_y = curr_x, curr_y
                unemb_x, unemb_y = x, y
                break

            if not unemb_i_exist:
                continue

            d_exist = True
            break

        if d_exist:
            maze.set_wall(found_x, found_y, unemb_x, unemb_y, ' ')
            maze.set_cell(found_x, found_y, 'I')
            neighbours = maze.get_cell_neighbours(found_x, found_y, 'O')

            for x, y in neighbours:
                maze.set_cell(x, y, 'F')

        else:
            break

    # end (step 9)
    start_iter = 0

    for start_x, start_y in start_points:
        maze.set_cell(start_x, start_y, 'S' + str(start_iter))
        start_iter = start_iter + 1

    maze.set_cell(end_x, end_y, 'E')