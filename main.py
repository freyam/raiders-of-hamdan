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

game.castle = Castle(game, int(KINGDOM_WIDTH / 2 - 3), int(KINGDOM_HEIGHT / 2 - 2))
game.castle.display()

for x in range(game.castle.x - 2, game.castle.x + game.castle.width + 2):
    game.walls.append(Wall(game, x, game.castle.y - 2))
    game.walls.append(Wall(game, x, game.castle.y + game.castle.height + 1))

for y in range(game.castle.y - 2, game.castle.y + game.castle.height + 2):
    game.walls.append(Wall(game, game.castle.x - 2, y))
    game.walls.append(Wall(game, game.castle.x + game.castle.width + 1, y))


game.cannons.append(Cannon(game, game.castle.x - 3, game.castle.y - 3))
game.cannons.append(
    Cannon(game, game.castle.x + game.castle.width + 2, game.castle.y - 3)
)
game.cannons.append(
    Cannon(
        game,
        game.castle.x + game.castle.width + 2,
        game.castle.y + game.castle.height + 2,
    )
)
game.cannons.append(
    Cannon(game, game.castle.x - 3, game.castle.y + game.castle.height + 2)
)


for x in range(KINGDOM_WIDTH):
    for y in range(KINGDOM_HEIGHT):
        if game.kingdom.kingdom[y][x] == "." and (
            x < game.castle.x - 2 or x > game.castle.x + game.castle.width + 1
        ):
            if random.random() < 0.01:
                game.residences.append(Residence(game, x, y))
            elif random.random() < 0.001:
                game.walls.append(Wall(game, x, y))
            elif random.random() < 0.0005:
                game.cannons.append(Cannon(game, x, y))

for wall in game.walls:
    wall.display()

for residence in game.residences:
    residence.display()

for cannon in game.cannons:
    cannon.display()

game.king = King(game, 1, 1)
game.king.display()


def animate():
    while game.run:
        key = inputx()

        if key == "q":
            game.run = False
            break

        if key in ["w", "a", "s", "d"]:
            game.king.move(game, key)

        if key == " ":
            game.king.attack(game, game.king.weapon)

        game.render()

        time.sleep(1 / 30)


animate()
