import time
from colorama import Fore, Back, Style

from src.structure import Structure, structure_types


class Game:
    def __init__(self, kingdom, stats):
        self.run = True
        self.kingdom = kingdom
        self.stats = stats

    def render(self):
        for row in self.kingdom:
            for char in row:
                if char == " ":
                    print(" ", end="")
                else:
                    structure_code = char
                    x = self.kingdom.index(row)
                    y = row.index(char)
                    tile = Structure(self, x, y, structure_code)
                    tile.draw()
                    print(tile.visual, end="")
            print()


class Stats:
    def __init__(self):
        self.difficulty = 2
        self.time = time.time()

    def render(self):
        print("Difficulty:", self.difficulty)
        print("Time:", (time.time() - self.time).__round__(2))
