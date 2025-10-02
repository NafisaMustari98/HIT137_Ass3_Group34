import config 
from gui_interface import AIGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AIGUI(root)
    root.mainloop()