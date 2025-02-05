import curses
from curses import newwin, wrapper
import queue
import time

mazes = [
    [
        ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
    ],
    [
        ["#", "#", "#", "#", "O", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", "#", "#", "#", "#", "X", "#", "#", "#"],
    ]
]

# Function to print the maze in various stages as the algorithm tries to find the path
def print_maze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, GREEN)


def find_path(maze, stdscr):
    start = "O"
    end = "X"

    start_pos = start_location(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbours = find_neighbour(maze, row, col)

        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour

            if maze[r][c] == "#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)

        stdscr.getch()  # Wait for keypress to step through each iteration


def find_neighbour(maze, row, col):
    neighbours = []

    if row > 0:
        neighbours.append((row - 1, col))
    if row < len(maze) - 1:
        neighbours.append((row + 1, col))
    if col > 0:
        neighbours.append((row, col - 1))
    if col < len(maze[0]) - 1:
        neighbours.append((row, col + 1))

    return neighbours


# Function to find the start location in the maze
def start_location(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    for maze in mazes:
        find_path(maze, stdscr)
        stdscr.getch()  # Wait for keypress to move to the next maze


wrapper(main)
