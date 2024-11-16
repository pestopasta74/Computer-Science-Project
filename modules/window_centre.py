# This module is used to center the window on the screen
import tkinter as tk

def center_window(self, original_size):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    window_width, window_height = [int(x) for x in original_size.split("x")]

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    self.geometry(f"{window_width}x{window_height}+{x}+{y}")
