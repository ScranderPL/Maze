import random
import time
import maze
import maze_generator
import maze_solver
import encoder
import decoder

x_size = int(input("Insert X size: "))
y_size = int(input("Insert Y size: "))
print("1. Recursive backtracker")
print("2. Hunt and kill")
print("3. Eller's algorithm")
print("4. Steganografy: encode and decode")
algorithm = int(input("Choose algorithm: "))

maze_object = maze.Maze(x_size, y_size)
maze_graphics = maze.MazeGraphics(x_size, y_size)

random.seed(a=3)

maze_object.clear()
maze_object.fill()

if algorithm == 1:
    maze_generator.recursive_backtracker(maze_graphics, maze_object)
elif algorithm == 2:
    maze_generator.hunt_and_kill(maze_graphics, maze_object)
elif algorithm == 3:
    maze_generator.eller(maze_graphics, maze_object)
elif algorithm == 4:
    maze_object.clear()
    maze_object.hunt_and_kill_fill()
    maze_generator.hunt_and_kill_mod(maze_graphics, maze_object)

    seed = 100500
    message = '11010101'

    encoder.encode(maze_graphics, maze_object, message, seed)

    decoded_message = decoder.decode(maze_graphics, maze_object, seed)

    print("The message " + decoded_message + " was decoded")
    print("Is it equal to initial message " + str(message == decoded_message))

    if message != decoded_message:
        print("Is initial message starts with decoded message at least " + str(message.startswith(decoded_message)))

        if message.startswith(decoded_message):
            print("Probably the embeddable capasity of given maze is to small for the message")

    print("\n\n")

maze_graphics.redraw(maze_object)

print("A* solution:")
start = time.time()
print(maze_solver.astar_solver(maze_graphics, maze_object, 5, 5, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))

print("BFS solution:")
start = time.time()
print(maze_solver.bfs_solver(maze_graphics, maze_object, 5, 5, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))

print("DFS solution:")
start = time.time()
print(maze_solver.dfs_solver(maze_graphics, maze_object, 5, 5, x_size, y_size))
end = time.time()
print("elapsed time: {} sec.".format(end - start))

print("iterative DFS solution:")
start = time.time()
path = maze_solver.dfs_iterative_solver(maze_graphics, maze_object, 5, 5, x_size, y_size)
print(path)
end = time.time()
print("elapsed time: {} sec.".format(end - start))

maze_graphics.redraw(maze_object)

maze_graphics.destroy()