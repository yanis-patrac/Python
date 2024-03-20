import tkinter as tk
class win_or_loose:
    def __init__(self,result,time,master, menu_callback):
        self.master = master
        self.top_master = tk.Toplevel(master)
        self.result = result
        self.menu_callback = menu_callback
        self.time = time
        
        self.create_widgets()
    
    def create_widgets(self):
        self.title_label = tk.Label(self.top_master, text="Result", font=("Arial", 24), bg="white")
        self.title_label.pack(pady=20)

        self.result_label = tk.Label(self.top_master, text=self.result, font=("Arial", 14), bg="white")
        self.result_label.pack()

        self.time_label = tk.Label(self.top_master, text="Time: " + str(self.time), font=("Arial", 14), bg="white")
        self.time_label.pack(pady=10)

        self.restart_button = tk.Button(self.top_master, text="Return menu", font=("Arial", 12), command=self.menu)
        self.restart_button.pack(pady=10)
        
    def menu(self):
        self.top_master.destroy()
        self.master.destroy()
        self.menu_callback(self.menu_callback)