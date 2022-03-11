import time
from colorama import Fore, Back, Style

from src.structure import *


class Game:
    def __init__(self, kingdom):
        self.run = True
        self.kingdom = kingdom
        self.time = time.time()
        self.walls = []
        self.residences = []
        self.canons = []

    def render(self):
        print("\033c", end="")

        print("Kingdom of Hamdan")

        self.kingdom.render()

        print("Time: " + str((time.time() - self.time).__round__(2)) + "s")
        print("Residences Left: " + str(len(self.residences)))
        print("Walls Left: " + str(len(self.walls)))
        print("Canons Left: " + str(len(self.canons)))
