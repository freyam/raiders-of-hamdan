from src.structure import *
from src.troop import *
from src.colors import print_hex


class Kingdom:
    def __init__(self, height, width):
        self.kingdom = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(".")
            self.kingdom.append(row)

    def render(self):
        for row in self.kingdom:
            for char in row:
                if char == ".":
                    print(char, end="")
                elif is_structure(char):
                    print_hex(
                        structure_types[char]["visual"], structure_types[char]["color"]
                    )
                elif is_troop(char):
                    print_hex(troop_types[char]["visual"], troop_types[char]["color"])
            print()
