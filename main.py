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

game.tunnels.append(Tunnel(game, 0, 0))
game.tunnels.append(Tunnel(game, KINGDOM_WIDTH - 1, 0))
game.tunnels.append(Tunnel(game, KINGDOM_WIDTH - 1, KINGDOM_HEIGHT - 1))
game.tunnels.append(Tunnel(game, 0, KINGDOM_HEIGHT - 1))

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
        if (
            game.kingdom.kingdom[y][x] == "."
            and (x < game.castle.x - 2 or x > game.castle.x + game.castle.width + 1)
            and not (
                x == 0 or x == KINGDOM_WIDTH - 1 or y == 0 or y == KINGDOM_HEIGHT - 1
            )
        ):
            if random.random() < 0.001:
                game.cannons.append(Cannon(game, x, y))
            elif random.random() < 0.005:
                game.walls.append(Wall(game, x, y))
            elif random.random() < 0.01:
                game.residences.append(Residence(game, x, y))


for tunnel in game.tunnels:
    tunnel.display()

for wall in game.walls:
    wall.display()

for residence in game.residences:
    residence.display()

for cannon in game.cannons:
    cannon.display()


game.king = King(game, 1, 1)
game.king.display()


def animate():
    while 1:
        key = inputx()

        if game.king is None and len(game.barbarians) == 0:
            print("\033c")
            print("You Lost!")
            break

        if game.castle == None and len(game.residences) == 0 and len(game.cannons) == 0:
            print("\033c")
            print("You Won!")
            break

        if key == "q":
            break
        elif key == "p":
            game.pause = not game.pause
            continue

        if game.pause:
            continue

        game.time += 1 / 10

        if game.king and key in ["w", "a", "s", "d"]:
            game.king.move(game, key)

        if game.king and key == " ":
            game.king.attack(game, game.king.weapon)

        if len(game.barbarians) < 10:
            if key == "1":
                game.spawnBarbarian(0 + 1, 0)
            elif key == "2":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "3":
                game.spawnBarbarian(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "4":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        if key == "h":
            for troop in [game.king] + game.barbarians:
                troop.max_hp = int(troop.max_hp * 1.5)
                troop.hp = min(troop.hp + 500, troop.max_hp)
        elif key == "r":
            for troop in [game.king] + game.barbarians:
                troop.damage = troop.damage * 2
                troop.speed = troop.speed * 2

        game.render()
        game.cannonInteraction()

        if game.king:
            game.tunnelInteraction()

        if len(game.barbarians):
            for barbarian in game.barbarians:
                barbarian.moveToNearestHostileStructure(game)


animate()
