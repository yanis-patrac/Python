import tkinter as tk
from src.main_game import main_game

class menu:
    def __init__(self, menu_callback):
        self.menu_callback = menu_callback
        self.menu = tk.Tk()
        self.menu.title("Menu")
        self.menu.geometry("400x200")
        self.menu.resizable(False, False)
        self.menu.config(bg="white")

        self.create_widgets()
        self.menu.mainloop()
        
    def create_widgets(self):
        self.title_label = tk.Label(self.menu, text="Minesweeper", font=("Arial", 24), bg="white")
        self.title_label.pack(pady=20)

        self.difficulty_label = tk.Label(self.menu, text="Choose Difficulty:", font=("Arial", 14), bg="white")
        self.difficulty_label.pack()
        self.difficulty_var = tk.StringVar(self.menu)
        self.difficulty_var.set("Easy")
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_menu = tk.OptionMenu(self.menu, self.difficulty_var, *self.difficulty_options)
        self.difficulty_menu.pack(pady=10)

        self.start_button = tk.Button(self.menu, text="Start", font=("Arial", 12), command=self.start_game)
        self.start_button.pack(pady=10)
    
    def start_game(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            rows, cols, num_mines = 10, 10, 10
        elif difficulty == "Medium":
            rows, cols, num_mines = 20, 20, 50
        else:  # Hard
            rows, cols, num_mines = 30, 30, 100
        self.menu.destroy()
        main_game(rows, cols, num_mines,self.menu_callback)