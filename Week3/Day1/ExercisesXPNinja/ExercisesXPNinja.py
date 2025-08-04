import time
import os

class GameOfLife:
    def __init__(self, rows, cols, initial_state=None):
        self.rows = rows
        self.cols = cols
        self.grid = initial_state or [[0 for _ in range(cols)] for _ in range(rows)]

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            print("".join("  " if cell == 0 else "██" for cell in row))
        print("\n")

    def count_neighbors(self, row, col):
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def update(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)
                if self.grid[r][c] == 1 and neighbors in [2, 3]:
                    new_grid[r][c] = 1
                elif self.grid[r][c] == 0 and neighbors == 3:
                    new_grid[r][c] = 1
        self.grid = new_grid

    def is_extinct(self):
        return all(cell == 0 for row in self.grid for cell in row)

    def run(self, generations=100, delay=0.1):
        for i in range(generations):
            print(f"Generation {i+1}")
            self.display()
            self.update()
            if self.is_extinct():
                print("💀 All cells are dead. Game over.")
                break
            time.sleep(delay)

# === Gosper Glider Gun ===
def gosper_glider_gun():
    rows, cols = 20, 40
    grid = [[0]*cols for _ in range(rows)]

    gun_coords = [
        (5,1),(5,2),(6,1),(6,2),
        (5,11),(6,11),(7,11),
        (4,12),(8,12),
        (3,13),(9,13),(3,14),(9,14),
        (6,15),
        (4,16),(8,16),
        (5,17),(6,17),(7,17),
        (6,18),
        (3,21),(4,21),(5,21),
        (3,22),(4,22),(5,22),
        (2,23),(6,23),
        (1,25),(2,25),(6,25),(7,25),
        (3,35),(4,35),(3,36),(4,36)
    ]

    for r, c in gun_coords:
        if r < rows and c < cols:
            grid[r][c] = 1
    return grid

# === Lancement ===
if __name__ == "__main__":
    initial = gosper_glider_gun()
    game = GameOfLife(rows=20, cols=40, initial_state=initial)
    game.run(generations=200, delay=0.1)
