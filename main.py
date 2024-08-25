import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.unlocked = False
        self.occupied = False

class Building:
    def __init__(self, width, height, mandatory=True):
        self.width = width
        self.height = height
        self.mandatory = mandatory
        self.rotated = False  # To track if the building is rotated

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.rotated = not self.rotated

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grid Layout Planner")
        self.geometry("600x600")
        self.tiles = {}
        self.buildings = []
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
            messagebox.showinfo("Info", "Tile is locked. Unlock it first!")
            return

        if self.buildings:
            building = self.buildings[-1]
            if self.can_place_building(x, y, building):
                self.place_building(x, y, building)
                self.buildings.pop()
            else:
                messagebox.showinfo("Info", "Building cannot fit here.")
        else:
            messagebox.showinfo("Info", "No building selected.")

    def can_place_building(self, x, y, building):
        # Check if the building can be placed on the grid starting at (x, y)
        for i in range(building.width):
            for j in range(building.height):
                if (x + i, y + j) not in self.tiles or not self.tiles[(x + i, y + j)].unlocked or self.tiles[(x + i, y + j)].occupied:
                    return False
        return True

    def place_building(self, x, y, building):
        # Place the building on the grid and mark the tiles as occupied
        for i in range(building.width):
            for j in range(building.height):
                self.tiles[(x + i, y + j)].occupied = True
                btn = self.grid_frame.grid_slaves(row=x + i, column=y + j)[0]
                btn.config(bg="blue" if building.mandatory else "orange")

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

        rotate_building_button = tk.Button(self, text="Rotate Building", command=self.rotate_building)
        rotate_building_button.pack(side=tk.LEFT, padx=10)

        expand_right_button = tk.Button(self, text="Expand Right", command=lambda: self.expand_grid(direction="right"))
        expand_right_button.pack(side=tk.LEFT, padx=10)

        expand_down_button = tk.Button(self, text="Expand Down", command=lambda: self.expand_grid(direction="down"))
        expand_down_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(self, text="Save Layout", command=self.save_layout)
        save_button.pack(side=tk.LEFT, padx=10)

        load_button = tk.Button(self, text="Load Layout", command=self.load_layout)
        load_button.pack(side=tk.LEFT, padx=10)

    def unlock_tile(self):
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
        # Get building dimensions from user
        width = simpledialog.askinteger("Input", "Enter building width (in grid units):", minvalue=1)
        height = simpledialog.askinteger("Input", "Enter building height (in grid units):", minvalue=1)
        if width and height:
            mandatory = messagebox.askyesno("Mandatory?", "Is this building mandatory?")
            building = Building(width, height, mandatory)
            self.buildings.append(building)
            messagebox.showinfo("Info", f"Building {width}x{height} added. Click on the grid to place it.")

    def rotate_building(self):
        if self.buildings:
            building = self.buildings[-1]
            building.rotate()
            messagebox.showinfo("Info", f"Building rotated to {building.width}x{building.height}. Click on the grid to place it.")
        else:
            messagebox.showinfo("Info", "No building to rotate.")

    def expand_grid(self, direction):
        max_x = max(tile.x for tile in self.tiles.values())
        max_y = max(tile.y for tile in self.tiles.values())
        if direction == "right":
            for i in range(max_x + 1):
                self.tiles[(i, max_y + 1)] = Tile(i, max_y + 1)
                self.create_tile_button(i, max_y + 1)
        elif direction == "down":
            for j in range(max_y + 1):
                self.tiles[(max_x + 1, j)] = Tile(max_x + 1, j)
                self.create_tile_button(max_x + 1, j)

    def save_layout(self):
        layout = {"tiles": {}, "buildings": []}
        for (x, y), tile in self.tiles.items():
            layout["tiles"][(x, y)] = {"unlocked": tile.unlocked, "occupied": tile.occupied}
        for building in self.buildings:
            layout["buildings"].append({"width": building.width, "height": building.height, "mandatory": building.mandatory, "rotated": building.rotated})
        with open("grid_layout.json", "w") as file:
            json.dump(layout, file)
        messagebox.showinfo("Info", "Layout saved successfully!")

    def load_layout(self):
        try:
            with open("grid_layout.json", "r") as file:
                layout = json.load(file)
            for (x, y), tile_info in layout["tiles"].items():
                self.tiles[(x, y)] = Tile(x, y)
                self.tiles[(x, y)].unlocked = tile_info["unlocked"]
                self.tiles[(x, y)].occupied = tile_info["occupied"]
                self.update_tile_button(x, y)
            self.buildings = []
            for building_info in layout["buildings"]:
                building = Building(building_info["width"], building_info["height"], building_info["mandatory"])
                if building_info["rotated"]:
                    building.rotate()
                self.buildings.append(building)
            messagebox.showinfo("Info", "Layout loaded successfully!")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved layout found.")

# Running the app
if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
