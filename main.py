from re import S
import colorama
import copy
import sys
import time
from colorama import Fore, Back, Style

from src.game import Game, Stats
from src.stdin import inputx

# from src.structure import Structure
# from src.king import King


kingdom = []
with open("assets/kingdom.txt") as f:
    for line in f:
        kingdom.append(line.strip())

stats = Stats()
game = Game(kingdom, stats)

while game.run:
    key = inputx()

    if key == "q":
        game.run = False
        break

    print("\033c", end="")
    game.render()
    stats.render()

    time.sleep(1 / 30)
