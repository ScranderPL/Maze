import random
import time
import maze
import maze_generator
import sys


def test_gens(n, number_of_runs, seed = 1):

    random.seed(seed)
    print("test average runtime, number of runs =", number_of_runs, ", maze size is equal", "{}*{}".format(n, n))

    #test recursive_backtracker
    recursive_backtracker_time = 0

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)

        start = time.time()
        maze_generator.recursive_backtracker(None, maze_object)
        end = time.time()

        recursive_backtracker_time += (end - start) / number_of_runs

    print("Recursive backtracker average time is", recursive_backtracker_time, "sec.")


    #test hunt_and_kill
    hunt_and_kill_time = 0

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)

        start = time.time()
        maze_generator.hunt_and_kill(None, maze_object)
        end = time.time()

        hunt_and_kill_time += (end - start) / number_of_runs

    print("Hunt and Kill average time is", hunt_and_kill_time, "sec.")


    #test eller
    eller_time = 0

    for i in range(number_of_runs):
        maze_object = maze.Maze(n, n)

        start = time.time()
        maze_generator.eller(None, maze_object)
        end = time.time()

        eller_time += (end - start) / number_of_runs

    print("Eller average time is", eller_time, "sec.")

    return None


if __name__ == '__main__':
    #to run it print in command line "py test_generators.py labirint_size number_of_runs"
    test_gens(int(sys.argv[1]), int(sys.argv[2]))
