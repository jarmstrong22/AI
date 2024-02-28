import tkinter as tk
import random
from queue import PriorityQueue

class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.h = 0
        self.parent = None

    def __lt__(self, other):
        return self.h < other.h

class MazeGame:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.agent_pos = (3, 0)
        self.goal_pos = (self.rows - 1, self.cols - 1)
        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]
        self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.heuristic(self.agent_pos)

        self.cell_size = 75
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()
        self.find_path()

    def draw_maze(self):
        for x in range(self.rows):
            for y in range(self.cols):
                color = 'maroon' if self.maze[x][y] == 1 else 'white'
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size,
                                             (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill=color)

    def heuristic(self, pos):
        return ((pos[0] - self.goal_pos[0]) ** 2 + (pos[1] - self.goal_pos[1]) ** 2) ** 0.5

    def find_path(self):
        open_set = PriorityQueue()
        open_set.put(self.cells[self.agent_pos[0]][self.agent_pos[1]])

        while not open_set.empty():
            current_cell = open_set.get()

            if (current_cell.x, current_cell.y) == self.goal_pos:
                self.reconstruct_path()
                break

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            random.shuffle(directions)  # Shuffle directions to move randomly

            for dx, dy in directions:
                new_x, new_y = current_cell.x + dx, current_cell.y + dy

                if 0 <= new_x < self.rows and 0 <= new_y < self.cols and not self.cells[new_x][new_y].is_wall:
                    if self.cells[new_x][new_y].h == 0:
                        self.cells[new_x][new_y].h = self.heuristic((new_x, new_y))
                        self.cells[new_x][new_y].parent = current_cell
                        open_set.put(self.cells[new_x][new_y])

    def reconstruct_path(self):
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        while current_cell.parent:
            x, y = current_cell.x, current_cell.y
            self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size,
                                         (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill='green')
            current_cell = current_cell.parent


maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

root = tk.Tk()
root.title("Greedy Best-First Search Maze")


game = MazeGame(root, maze)

root.mainloop()