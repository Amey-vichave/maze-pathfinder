import curses
import time
from curses import wrapper
import queue




maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(stdscr: curses.window, maze, path= []):
    green = curses.color_pair(1)
    red = curses.color_pair(2)
    for i , row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", red)
            else: 
                stdscr.addstr(i, j*2, value, green)


def find_start(stdscr: curses.window, maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_path(stdscr: curses.window, maze):
    start = 'O'
    end = 'X'
    start_pos = find_start(stdscr, maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row , col = current_pos

        stdscr.clear()
        print_maze(stdscr, maze, path )
        time.sleep(0.2)
        stdscr.refresh()
        
        if maze[row] [col] == end:
            return path
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            r, c = neighbor
            if maze [r] [c] == "#":
                continue

            new_path = path + [neighbor]
            q.put ((neighbor, new_path))
            visited.add(neighbor)
    return None

def find_neighbors( maze, row, col):
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col +1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr: curses.window):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(stdscr, maze)


    stdscr.getch()

wrapper(main) 