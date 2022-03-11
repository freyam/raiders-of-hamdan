import random
import time

from src.game import *
from src.kingdom import *
from src.structure import *
from src.troop import *

from src.stdin import inputx

KINGDOM_WIDTH = 75
KINGDOM_HEIGHT = 20

game = Game(Kingdom(KINGDOM_HEIGHT, KINGDOM_WIDTH))

castle = Castle(game, int(KINGDOM_WIDTH / 2 - 3), int(KINGDOM_HEIGHT / 2 - 2))
castle.display()

for x in range(castle.x - 2, castle.x + castle.width + 2):
    game.walls.append(Wall(game, x, castle.y - 2))
    game.walls.append(Wall(game, x, castle.y + castle.height + 1))

for y in range(castle.y - 2, castle.y + castle.height + 2):
    game.walls.append(Wall(game, castle.x - 2, y))
    game.walls.append(Wall(game, castle.x + castle.width + 1, y))


game.canons.append(Cannon(game, castle.x - 3, castle.y - 3))
game.canons.append(Cannon(game, castle.x + castle.width + 2, castle.y - 3))
game.canons.append(
    Cannon(game, castle.x + castle.width + 2, castle.y + castle.height + 2)
)
game.canons.append(Cannon(game, castle.x - 3, castle.y + castle.height + 2))


for x in range(KINGDOM_WIDTH):
    for y in range(KINGDOM_HEIGHT):
        if game.kingdom.kingdom[y][x] == "." and (
            x < castle.x - 2 or x > castle.x + castle.width + 1
        ):
            if random.random() < 0.01:
                game.residences.append(Residence(game, x, y))
            elif random.random() < 0.005:
                game.walls.append(Wall(game, x, y))
            elif random.random() < 0.0005:
                game.canons.append(Cannon(game, x, y))

for wall in game.walls:
    wall.display()

for residence in game.residences:
    residence.display()

for cannon in game.canons:
    cannon.display()

king = King(game, 1, 1)
king.display()


def animate():
    while game.run:
        key = inputx()

        if key == "q":
            game.run = False
            break

        if key == "w" or key == "a" or key == "s" or key == "d":
            king.move(game, key)

        game.render()

        time.sleep(1 / 30)


animate()
