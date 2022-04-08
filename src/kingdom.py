from src.structure import *
from src.troop import *
from src.colors import *


class Kingdom:
    def __init__(self, height, width):
        self.kingdom = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(".")
            self.kingdom.append(row)

    def render(self, game):
        for _, row in enumerate(self.kingdom):
            for _, char in enumerate(row):
                if char == ".":
                    print(char, end="")
                elif is_structure(char):
                    x = row.index(char)
                    y = self.kingdom.index(row)

                    type = structure_types[game.kingdom.kingdom[y][x]]["code"]
                    if type == "H":
                        print_hex(
                            structure_types[char]["visual"], game.castle.get_color()
                        )
                    elif type == "C":
                        for cannon in game.cannons:
                            if cannon.x == x and cannon.y == y:
                                print_hex(
                                    structure_types[char]["visual"], cannon.get_color()
                                )
                                break
                    elif type == "W":
                        for wall in game.walls:
                            if wall.x == x and wall.y == y:
                                print_hex(
                                    structure_types[char]["visual"],
                                    wall.get_color(),
                                )
                                break
                    elif type == "R":
                        for residence in game.residences:
                            if residence.x == x and residence.y == y:
                                print_hex(
                                    structure_types[char]["visual"],
                                    residence.get_color(),
                                )
                                break
                    else:
                        print_hex(
                            structure_types[char]["visual"],
                            structure_types[char]["color"],
                        )
                elif is_troop(char):
                    print_hex(troop_types[char]["visual"], troop_types[char]["color"])
            print()
