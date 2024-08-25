import tkinter as tk
from tkinter import messagebox

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.unlocked = False

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Layout Planner")
        self.geometry("600x600")
        self.tiles = {}
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=20)
        self.initialize_grid(6)
        self.create_buttons()

    def initialize_grid(self, initial_tiles):
        for i in range(initial_tiles):
            for j in range(initial_tiles):
                self.tiles[(i, j)] = Tile(i, j)
                self.tiles[(i, j)].unlocked = True
                self.create_tile_button(i, j)

    def create_tile_button(self, x, y):
        btn = tk.Button(self.grid_frame, text="", width=4, height=2,
                        command=lambda: self.on_tile_click(x, y))
        btn.grid(row=x, column=y)
        self.update_tile_button(x, y, btn)

    def on_tile_click(self, x, y):
        if not self.tiles[(x, y)].unlocked:
            self.tiles[(x, y)].unlocked = True
            self.update_tile_button(x, y)
        else:
            messagebox.showinfo("Info", "Tile already unlocked!")

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

        add_building_button = tk.Button(self, text="Add Building", command=self.add_building)
        add_building_button.pack(side=tk.LEFT, padx=10)

    def unlock_tile(self):
        # Code to unlock a tile (This can be expanded to unlock a tile based on user input)
        x, y = self.get_next_locked_tile()
        if x is not None and y is not None:
            self.tiles[(x, y)].unlocked = True
            self.update_tile_button(x, y)
        else:
            messagebox.showinfo("Info", "All tiles are unlocked!")

    def get_next_locked_tile(self):
        for (x, y), tile in self.tiles.items():
            if not tile.unlocked:
                return x, y
        return None, None

    def add_building(self):
        # Placeholder for adding building logic
        messagebox.showinfo("Info", "Feature to add building coming soon!")

# Running the app
if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
