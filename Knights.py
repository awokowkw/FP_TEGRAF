import tkinter as tk

N = 8
CELL = 70
PADDING = 30

moves = [
    (2, 1), (1, 2),
    (-1, 2), (-2, 1),
    (-2, -1), (-1, -2),
    (1, -2), (2, -1)
]

def is_valid(x, y, board):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def count_degree(x, y, board):
    c = 0
    for dx, dy in moves:
        if is_valid(x + dx, y + dy, board):
            c += 1
    return c

def solve_tour(board, x, y, step, closed, start):
    """Hybrid Warnsdorff + Backtracking"""
    if step == N * N:
        if closed:
            sx, sy = start
            return any((abs(x - (sx + dx)) == 0 and abs(y - (sy + dy)) == 0)
                       or (abs(x - sx), abs(y - sy)) == (2, 1)
                       for dx, dy in moves)
        return True

    next_moves = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board):
            deg = count_degree(nx, ny, board)
            next_moves.append((deg, nx, ny))

    next_moves.sort(key=lambda t: t[0])  # Warnsdorff

    for _, nx, ny in next_moves:
        board[nx][ny] = step
        if solve_tour(board, nx, ny, step + 1, closed, start):
            return True
        board[nx][ny] = -1  # backtrack

    return False

def knights_tour(sx, sy, closed=False):
    board = [[-1] * N for _ in range(N)]
    board[sx][sy] = 0
    solve_tour(board, sx, sy, 1, closed, (sx, sy))
    return board

def draw_tour(board):
    win = tk.Tk()
    win.title("Knight's Tour")

    size = N * CELL + PADDING*2
    canvas = tk.Canvas(win, width=size, height=size, bg="white")
    canvas.pack()

    for i in range(N+1):
        canvas.create_line(PADDING, PADDING + i*CELL,
                           PADDING + N*CELL, PADDING + i*CELL)
        canvas.create_line(PADDING + i*CELL, PADDING,
                           PADDING + i*CELL, PADDING + N*CELL)

    pos = {}
    for r in range(N):
        for c in range(N):
            pos[board[r][c]] = (r, c)

    for k in range(63):
        r1, c1 = pos[k]
        r2, c2 = pos[k+1]

        x1 = PADDING + c1*CELL + CELL//2
        y1 = PADDING + r1*CELL + CELL//2
        x2 = PADDING + c2*CELL + CELL//2
        y2 = PADDING + r2*CELL + CELL//2

        canvas.create_line(x1, y1, x2, y2, width=2)

    r0, c0 = pos[0]
    x0 = PADDING + c0*CELL + CELL//2
    y0 = PADDING + r0*CELL + CELL//2
    canvas.create_oval(x0-8, y0-8, x0+8, y0+8, fill="green")

    rE, cE = pos[63]
    xE = PADDING + cE*CELL + CELL//2
    yE = PADDING + rE*CELL + CELL//2
    canvas.create_oval(xE-8, yE-8, xE+8, yE+8, fill="red")

    win.mainloop()

print("Knight's Tour (Hybrid Warnsdorff + Backtracking)")
sx = int(input("Start row 0-7: "))
sy = int(input("Start col 0-7: "))

print("1. Open Tour")
print("2. Closed Tour")
mode = int(input("Mode (1/2): "))

board = knights_tour(sx, sy, closed=(mode == 2))
draw_tour(board)
