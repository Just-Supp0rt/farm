import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.unlocked = False

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Layout Planner")
        self.geometry("800x800")
        self.tiles = {}
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=20)
        self.initialize_grid(8, 8)
        self.unlock_initial_tiles()
        self.create_buttons()

    def initialize_grid(self, max_x, max_y):
        for i in range(max_x):
            for j in range(max_y):
                self.tiles[(i, j)] = Tile(i, j)
                self.create_tile_button(i, j)

    def unlock_initial_tiles(self):
        # Unlock 2 tiles right and 3 tiles down, 6 in total
        initial_unlocked_positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
        for x, y in initial_unlocked_positions:
            self.tiles[(x, y)].unlocked = True
            self.update_tile_button(x, y)

    def create_tile_button(self, x, y):
        btn = tk.Button(self.grid_frame, text="", width=4, height=2,
                        command=lambda: self.on_tile_click(x, y))
        btn.grid(row=x, column=y)
        self.update_tile_button(x, y, btn)

    def on_tile_click(self, x, y):
        if not self.tiles[(x, y)].unlocked:
            messagebox.showinfo("Info", "Tile is locked. Unlock it first!")
        else:
            messagebox.showinfo("Info", "Tile is already unlocked.")

    def update_tile_button(self, x, y, btn=None):
        if btn is None:
            btn = self.grid_frame.grid_slaves(row=x, column=y)[0]
        if self.tiles[(x, y)].unlocked:
            btn.config(bg="lightgreen", state="disabled")
        else:
            btn.config(bg="lightgrey", state="normal")

    def create_buttons(self):
        unlock_button = tk.Button(self, text="Unlock Tile", command=self.unlock_tile)
        unlock_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(self, text="Save Layout", command=self.save_layout)
        save_button.pack(side=tk.LEFT, padx=10)

        load_button = tk.Button(self, text="Load Layout", command=self.load_layout)
        load_button.pack(side=tk.LEFT, padx=10)

    def unlock_tile(self):
        x = simpledialog.askinteger("Input", "Enter the X coordinate of the tile to unlock:")
        y = simpledialog.askinteger("Input", "Enter the Y coordinate of the tile to unlock:")
        if (x, y) in self.tiles:
            if not self.tiles[(x, y)].unlocked:
                self.tiles[(x, y)].unlocked = True
                self.update_tile_button(x, y)
            else:
                messagebox.showinfo("Info", "Tile is already unlocked!")
        else:
            messagebox.showinfo("Info", "Invalid coordinates. Tile does not exist.")

    def save_layout(self):
        layout = {"tiles": {}}
        for (x, y), tile in self.tiles.items():
            # Convert the (x, y) tuple to a string key
            key = f"{x},{y}"
            layout["tiles"][key] = {"unlocked": tile.unlocked}
        with open("grid_layout.json", "w") as file:
            json.dump(layout, file)
        messagebox.showinfo("Info", "Layout saved successfully!")

    def load_layout(self):
        try:
            with open("grid_layout.json", "r") as file:
                layout = json.load(file)
            for key, tile_info in layout["tiles"].items():
                # Convert the string key back to a tuple (x, y)
                x, y = map(int, key.split(","))
                self.tiles[(x, y)].unlocked = tile_info["unlocked"]
                self.update_tile_button(x, y)
            messagebox.showinfo("Info", "Layout loaded successfully!")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved layout found.")

# Running the app
if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
