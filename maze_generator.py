import random


def recursive_backtracker(maze_graphics, maze):

    visited_stack = []

    init_x = random.randint(1, maze.x_size)
    init_y = random.randint(1, maze.y_size)

    visited_stack.append([init_x, init_y])
    maze.set_cell(init_x, init_y, 'V')

    while visited_stack:
        current_cell = visited_stack.pop()
        maze.set_cell(current_cell[0], current_cell[1], 'C')
        neighbours = maze.get_cell_not_visited_neighbours(current_cell[0], current_cell[1])

        if not neighbours:
            maze_graphics.redraw(maze)
            maze.set_cell(current_cell[0], current_cell[1], 'V')
            continue

        visited_stack.append(current_cell)
        chosen_neighbour = random.choice(neighbours)
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], 'C')
        maze.set_cell(chosen_neighbour[0], chosen_neighbour[1], 'V')
        visited_stack.append(chosen_neighbour)

        maze_graphics.redraw(maze)
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], ' ')
        maze.set_cell(current_cell[0], current_cell[1], 'V')



def hunt_and_kill(maze_graphics, maze):

    def hunt_and_kill_scan(maze_graphics, maze):

        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):
                tmp_cell = maze.get_cell(x, y)

                if tmp_cell == 'V':
                    neighbours = maze.get_cell_not_visited_neighbours(x, y)

                    if not neighbours:
                        continue

                    return [x, y], random.choice(neighbours)

        return None, None

    curr_x = random.randint(1, maze.x_size)
    curr_y = random.randint(1, maze.y_size)
    curr_cell = [curr_x, curr_y]

    while True:
        maze.set_cell(curr_cell[0], curr_cell[1], 'V')
        neighbours = maze.get_cell_not_visited_neighbours(curr_cell[0], curr_cell[1])

        if not neighbours:
            curr_cell, next_cell = hunt_and_kill_scan(maze_graphics, maze)
            if not curr_cell:
                return
        else:
            next_cell = random.choice(neighbours)

        maze.set_wall(curr_cell[0], curr_cell[1], next_cell[0], next_cell[1], ' ')
        curr_cell = next_cell



def hunt_and_kill_mod(maze_graphics, maze, reuse = False):

    def hunt_and_kill_scan(maze_graphics, maze):

        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):

                if maze.get_cell(x, y) == 'F':
                    neighbours = maze.get_cell_neighbours(x, y, 'I')

                    if not neighbours:
                        continue

                    return random.choice(neighbours)

        return None, None

    if reuse:
        stop = True

        # step required for maze reuse
        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):

                if maze.get_cell(x, y) == 'F':
                    neighbours = maze.get_cell_neighbours(x, y, 'I')

                    if not neighbours:
                        continue

                    neigh_x, neigh_y = random.choice(neighbours)
                    maze.set_wall(neigh_x, neigh_y, x, y, ' ')
                    curr_x, curr_y = x, y
                    stop = False
                    break

            if not stop:
                break

        if stop:
            return

    else:
        curr_x = random.randint(1, maze.x_size)
        curr_y = random.randint(1, maze.y_size)

    while True:
        #maze_graphics.redraw(maze)
        maze.set_cell(curr_x, curr_y, 'I')
        neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'O')

        for x, y in neighbours:
            maze.set_cell(x, y, 'F')

        neighbours =  maze.get_cell_neighbours(curr_x, curr_y, 'F')

        if not neighbours:
            curr_x, curr_y = hunt_and_kill_scan(maze_graphics, maze)

            if not curr_x:
                return

            neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'F')

        neigh_x, neigh_y = random.choice(neighbours)
        maze.set_wall(curr_x, curr_y, neigh_x, neigh_y, ' ')
        curr_x, curr_y = neigh_x, neigh_y



def eller(maze_graphics, maze):

    def get_set(set_list, x_it, y_it):
        for set_it in set_list:
            if (x_it, y_it) in set_it:
                return set_it

    set_counter = 0
    sets = []

    for x in range(1, maze.x_size + 1):
        new_set = set()
        sets.append(new_set)
        sets[-1].add((x, 1))
        set_counter = set_counter + 1
        maze.set_cell(x, 1, set_counter)

    for y in range(1, maze.y_size+1):
        maze_graphics.redraw(maze)
        for x in range(1, maze.x_size):

            if random.random() < 0.5 or y == maze.y_size:
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
                        maze.set_cell(val[0], val[1], maze.get_cell(x, y))

                    maze.set_wall(x, y, x + 1, y, ' ')

        if y == maze.y_size:
            return

        processed_sets = set()
        x_range = list(range(1, maze.x_size+1))
        random.shuffle(x_range)

        for x in x_range:

            if (maze.get_cell(x, y) not in processed_sets) or random.random() < 0.5:
                processed_sets.add(maze.get_cell(x, y))
                maze.set_wall(x, y, x, y+1, ' ')
                maze.set_cell(x, y + 1, maze.get_cell(x, y))
                set_a = get_set(sets, x, y)
                sets.remove(set_a)
                set_a.add((x, y+1))
                sets.append(set_a)
            else:
                new_set = set()
                sets.append(new_set)
                sets[-1].add((x, y+1))
                set_counter = set_counter + 1
                maze.set_cell(x, y+1, set_counter)