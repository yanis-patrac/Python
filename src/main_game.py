import random
import time
from src.case import Case
from src.win_loose import win_or_loose
import tkinter as tk

class main_game:
    def __init__(self, rows, cols, num_mines, menu_callback):
        self.master = tk.Tk()
        self.master.title("Minesweeper")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.num_flags = 0
        self.num_question_marks = 0
        self.num_mines_found = 0
        self.board = [[Case() for i in range(cols)] for j in range(rows)]
        
        self.first_click = True
        self.timer_running = False
        self.start_time = None
        self.menu_callback = menu_callback

        self.create_widgets()
        self.master.mainloop()
    
    def create_widgets(self):
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        self.reset_button.pack()

        self.timer_label = tk.Label(self.master, text="Time: 0")
        self.timer_label.pack()

        self.info_frame = tk.Frame(self.master)
        self.info_frame.pack()

        self.mines_label = tk.Label(self.info_frame, text="Mines: " + str(self.num_mines))
        self.mines_label.pack(side=tk.LEFT)

        self.flags_label = tk.Label(self.info_frame, text="Flags: 0")
        self.flags_label.pack(side=tk.LEFT)

        self.question_marks_label = tk.Label(self.info_frame, text="Question Marks: 0")
        self.question_marks_label.pack(side=tk.LEFT)

        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        self.buttons = [[tk.Button(self.game_frame, width=2, height=1, command=lambda row=i, col=j: self.reveal(row, col),bg="gray") for j in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].grid(row=i, column=j)
                self.buttons[i][j].bind("<Button-3>", lambda event, row=i, col=j: self.toggle_flag(event, row, col))
                self.buttons[i][j].bind("<Button-1>", lambda event, row=i, col=j: self.first_click_handler(event, row, col))
        
    def first_click_handler(self, event, row, col):
        if self.first_click:
            self.first_click = False
            self.place_mines(row, col)
            self.reveal(row, col)

    def place_mines(self, row, col):
        exclude_list = [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        
        mines_placed = 0
        while mines_placed < self.num_mines:
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)
            if not self.board[random_row][random_col].is_mine and (random_row, random_col) not in exclude_list:
                self.board[random_row][random_col].is_mine = True
                mines_placed += 1
        
        self.calculate_adjacent_mines()

    def calculate_adjacent_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.board[i][j].is_mine:
                    count = 0
                    for x in range(max(0, i - 1), min(self.rows, i + 2)):
                        for y in range(max(0, j - 1), min(self.cols, j + 2)):
                            if self.board[x][y].is_mine:
                                count += 1
                    self.board[i][j].adjacent_mines = count

    def reveal(self, row, col):
        if not self.timer_running:
            self.start_timer()

        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return
        if self.board[row][col].is_revealed or self.board[row][col].is_flagged:
            return

        self.board[row][col].is_revealed = True
        self.buttons[row][col].config(state="disabled", bg="white")

        if self.board[row][col].is_mine:
            self.end_game(False)
            return
        elif self.board[row][col].adjacent_mines == 0:
            for x in range(max(0, row - 1), min(self.rows, row + 2)):
                for y in range(max(0, col - 1), min(self.cols, col + 2)):
                    self.reveal(x, y)
        else:
            self.buttons[row][col].config(text=self.board[row][col].adjacent_mines)

    def toggle_flag(self, event, row, col):
        if self.board[row][col].is_revealed:
            return

        if not self.board[row][col].is_flagged and not self.board[row][col].is_questioned:
            self.board[row][col].is_flagged = True
            self.buttons[row][col].config(text="F",bg="orange")
            self.num_flags += 1
            if self.board[row][col].is_mine:
                self.num_mines_found += 1
                self.win_condition()
        elif self.board[row][col].is_flagged:
            self.board[row][col].is_flagged = False
            self.board[row][col].is_questioned = True
            self.buttons[row][col].config(text="?",bg="yellow")
            self.num_flags -= 1
            self.num_question_marks += 1
        elif self.board[row][col].is_questioned:
            self.board[row][col].is_questioned = False
            self.buttons[row][col].config(text="",bg="gray")
            self.num_question_marks -= 1

        self.update_info_labels()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = round(time.time() - self.start_time)
            self.timer_label.config(text="Time: " + str(self.elapsed_time))
            self.timer_label.after(1000, self.update_timer)

    def end_game(self, win):
        self.timer_running = False
        if win:
            win_or_loose("You win", self.elapsed_time, self.master, self.menu_callback)
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j].is_mine:
                        self.buttons[i][j].config(text="*")
            win_or_loose("You lost", self.elapsed_time, self.master, self.menu_callback)

    def reset_game(self):
        self.game_frame.destroy()
        self.timer_label.destroy()
        self.reset_button.destroy()
        self.info_frame.destroy()
        self.__init__(self.master, self.rows, self.cols, self.num_mines)

    def update_info_labels(self):
        self.flags_label.config(text="Flags: " + str(self.num_flags))
        self.question_marks_label.config(text="Question Marks: " + str(self.num_question_marks))
        
    
    def win_condition(self):
        if self.num_mines_found == self.num_mines:
            self.end_game(True)