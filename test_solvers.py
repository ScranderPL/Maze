import random
import time
import maze
import maze_generator
import maze_solver
import sys


def test_solvs(n, number_of_runs, seed = 1):

    random.seed(seed)
    print("test average runtime, number of runs =", number_of_runs, ", maze size is equal", "{}*{}".format(n, n), '\n')

    available_algorithms = ["A*", "bfs", "dfs", "dfs iterative"]

    #test recursive_backtracker
    recursive_backtracker_time = {item : 0 for item in available_algorithms}

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)
        maze_generator.recursive_backtracker(None, maze_object)

        for item in available_algorithms:
            start = time.time()
            maze_solver.general_solver(item, None, maze_object, 1, 1, n, n)
            end = time.time()

            recursive_backtracker_time[item] += (end - start) / number_of_runs

    print("Recursive backtracker average time is:")

    for item in available_algorithms:
        print(item + ':', recursive_backtracker_time[item], "sec.")
    print("\n")


    #test hunt_and_kill
    hunt_and_kill_time = {item : 0 for item in available_algorithms}

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)
        maze_generator.hunt_and_kill_optimized(None, maze_object)

        for item in available_algorithms:
            start = time.time()
            maze_solver.general_solver(item, None, maze_object, 1, 1, n, n)
            end = time.time()

            hunt_and_kill_time[item] += (end - start) / number_of_runs

    print("Hunt and Kill average time is:")

    for item in available_algorithms:
        print(item + ':', hunt_and_kill_time[item], "sec.")
    print("\n")


    #test eller
    eller_time = {item : 0 for item in available_algorithms}

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)
        maze_generator.eller_optimized(None, maze_object)

        for item in available_algorithms:
            start = time.time()
            maze_solver.general_solver(item, None, maze_object, 1, 1, n, n)
            end = time.time()

            eller_time[item] += (end - start) / number_of_runs

    print("Eller average time is:")

    for item in available_algorithms:
        print(item + ':', eller_time[item], "sec.")
    print("\n")

    return None


if __name__ == '__main__':
    #to run it print in command line "py test_generators.py labirint_size number_of_runs"
    test_solvs(int(sys.argv[1]), int(sys.argv[2]))
