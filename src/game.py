import time

from src.structure import *
from src.troop import *


class Game:
    def __init__(self, kingdom):
        self.run = True

        self.kingdom = kingdom

        self.time = time.time()

        self.king = ""
        self.castle = ""
        self.walls = []
        self.residences = []
        self.cannons = []

        self.wallsDestroyed = 0
        self.residencesLooted = 0
        self.cannonsImpaired = 0

    def render(self):
        print("\033c", end="")

        print("Raiders of Hamdan")
        print("Time: " + str((time.time() - self.time).__round__(2)) + "s")

        self.kingdom.render(self)

        print("King's Health:", self.king.hp)
        print("King's Weapon:", self.king.weapon)

        print("Castle's Health:", self.castle.hp)

        print(
            "Residences Looted: "
            + str(self.residencesLooted)
            + "/"
            + str(len(self.residences) + self.residencesLooted)
        )

        print(
            "Cannons Impaired: "
            + str(self.cannonsImpaired)
            + "/"
            + str(len(self.cannons) + self.cannonsImpaired)
        )
