import time
from colorama import Fore, Back, Style

from src.structure import Structure, structure_types, is_structure


class Game:
    def __init__(self, kingdom, stats):
        self.run = True
        self.kingdom = kingdom
        self.stats = stats

    def update_map(self):
        pass

    def render(self):
        self.update_map()
        for row in self.kingdom:
            for char in row:
                if char == " ":
                    print(" ", end="")
                elif is_structure(char):
                    print(structure_types[char]["visual"], end="")
            print()


class Stats:
    def __init__(self):
        self.difficulty = 2
        self.time = time.time()

    def render(self):
        print("Difficulty:", self.difficulty)
        print("Time:", (time.time() - self.time).__round__(2))
