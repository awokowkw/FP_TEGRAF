import tkinter as tk
from tkinter import messagebox
import random

moves_x = [2, 1, -1, -2, -2, -1, 1, 2]
moves_y = [1, 2,  2,  1, -1, -2, -2, -1]

def valid(x, y, board):
    return (0 <= x < 8 and 0 <= y < 8 and board[x][y] == -1)

def get_degree(x, y, board):
    deg = 0
    for i in range(8):
        nx = x + moves_x[i]
        ny = y + moves_y[i]
        if valid(nx, ny, board):
            deg += 1
    return deg

def knights_tour_open(start_x, start_y):
    board = [[-1 for _ in range(8)] for _ in range(8)]
    board[start_x][start_y] = 0

    x, y = start_x, start_y

    for step in range(1, 64):
        min_deg = 9
        nx, ny = -1, -1

        for i in range(8):
            new_x = x + moves_x[i]
            new_y = y + moves_y[i]

            if valid(new_x, new_y, board):
                deg = get_degree(new_x, new_y, board)
                if deg < min_deg:
                    min_deg = deg
                    nx, ny = new_x, new_y

        if nx == -1:
            return None

        board[nx][ny] = step
        x, y = nx, ny

    return board


def knights_tour_closed(start_x, start_y):
    attempts = 0

    while True:
        attempts += 1

        board = [[-1 for _ in range(8)] for _ in range(8)]
        board[start_x][start_y] = 0

        x, y = start_x, start_y

        dirs = list(range(8))
        random.shuffle(dirs)

        valid_tour = True

        for step in range(1, 64):
            min_deg = 9
            nx, ny = -1, -1

            random.shuffle(dirs)
            for i in dirs:
                new_x = x + moves_x[i]
                new_y = y + moves_y[i]

                if valid(new_x, new_y, board):
                    deg = get_degree(new_x, new_y, board)
                    if deg < min_deg:
                        min_deg = deg
                        nx, ny = new_x, new_y

            if nx == -1:
                valid_tour = False
                break

            board[nx][ny] = step
            x, y = nx, ny

        if not valid_tour:
            continue

        for i in range(8):
            if (x + moves_x[i] == start_x and y + moves_y[i] == start_y):
                print("Closed tour ditemukan setelah percobaan:", attempts)
                return board


class KnightGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour - Pilih Start")

        self.canvas = tk.Canvas(root, width=640, height=640)
        self.canvas.pack()

        self.cell_size = 80
        self.start_x = 0
        self.start_y = 0

        self.draw_board()

        self.canvas.bind("<Button-1>", self.pick_start)

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Open Tour", command=self.run_open_tour,
                  font=("Arial", 14), width=12).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="Closed Tour", command=self.run_closed_tour,
                  font=("Arial", 14), width=12).grid(row=0, column=1, padx=10)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#D2B48C", "#8B5A2B"]

        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="black")

        self.highlight_start()

    def highlight_start(self):
        self.canvas.delete("start")
        x = self.start_y * self.cell_size + 40
        y = self.start_x * self.cell_size + 40
        self.canvas.create_oval(
            x-20, y-20, x+20, y+20,
            fill="skyblue", tags="start"
        )

    def pick_start(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        self.start_x = row
        self.start_y = col

        self.draw_board()

    def display_numbers(self, board):
        self.canvas.delete("numbers")

        for r in range(8):
            for c in range(8):
                step = board[r][c]
                x = c * self.cell_size + 40
                y = r * self.cell_size + 40
                self.canvas.create_text(x, y, text=str(step),
                                        font=("Arial", 14, "bold"),
                                        fill="black", tags="numbers")

    def draw_path(self, board):
        self.canvas.delete("path")

        coords = [None] * 64

        for r in range(8):
            for c in range(8):
                step = board[r][c]
                x = c * self.cell_size + 40
                y = r * self.cell_size + 40
                coords[step] = (x, y)

        for i in range(63):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            self.canvas.create_line(x1, y1, x2, y2,
                                    width=2, fill="black",
                                    tags="path")

    def run_open_tour(self):
        self.draw_board()
        board = knights_tour_open(self.start_x, self.start_y)

        if board is None:
            messagebox.showerror("Error", "Open Tour gagal ditemukan.")
            return

        self.display_numbers(board)
        self.draw_path(board)

    def run_closed_tour(self):
        self.draw_board()
        board = knights_tour_closed(self.start_x, self.start_y)

        if board is None:
            messagebox.showerror("Error", "Closed Tour gagal ditemukan.")
            return

        self.display_numbers(board)
        self.draw_path(board)


# Run GUI
root = tk.Tk()
KnightGUI(root)
root.mainloop()
