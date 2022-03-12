import datetime
import os
import random
import time
import copy

from src.game import *
from src.kingdom import *
from src.structure import *
from src.troop import *

from src.stdin import inputx

KINGDOM_WIDTH = 75
KINGDOM_HEIGHT = 20

game = Game(Kingdom(KINGDOM_HEIGHT, KINGDOM_WIDTH))


def init():
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

    # for x in range(KINGDOM_WIDTH):
    #     for y in range(KINGDOM_HEIGHT):
    #         if (
    #             game.kingdom.kingdom[y][x] == "."
    #             and (x < game.castle.x - 2 or x > game.castle.x + game.castle.width + 1)
    #             and not (
    #                 x == 0
    #                 or x == KINGDOM_WIDTH - 1
    #                 or y == 0
    #                 or y == KINGDOM_HEIGHT - 1
    #             )
    #         ):
    #             if random.random() < 0.001:
    #                 game.cannons.append(Cannon(game, x, y))
    #             elif random.random() < 0.005:
    #                 game.walls.append(Wall(game, x, y))
    #             elif random.random() < 0.01:
    #                 game.residences.append(Residence(game, x, y))

    game.residences.append(Residence(game, 42, 12))
    game.residences.append(Residence(game, 30, 10))
    game.residences.append(Residence(game, 20, 18))
    game.residences.append(Residence(game, 5, 5))
    game.residences.append(Residence(game, 50, 3))

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


commands = []
REPLAY_MODE = False


def animate():
    while 1:
        if REPLAY_MODE:
            key = commands.pop(0)
            time.sleep(0.1)
        else:
            key = inputx()
            commands.append(key)

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

        if key == "h":
            for troop in [game.king] + game.barbarians:
                troop.max_hp = int(troop.max_hp * 1.5)
                troop.hp = min(troop.hp + 500, troop.max_hp)
        elif key == "r":
            for troop in [game.king] + game.barbarians:
                troop.damage = troop.damage * 2
                troop.speed = troop.speed * 2

        if game.king and key in ["w", "a", "s", "d"]:
            game.king.move(game, key)

        if key == "l":
            if game.king.weapon == "sword":
                game.king.weapon = "shotgun"
            else:
                game.king.weapon = "sword"

        if game.king and key == " ":
            if game.king.weapon == "sword":
                game.king.attack(game)
            elif game.king.weapon == "shotgun":
                game.king.attackShotgun(game)

        if len(game.barbarians) < 10:
            if key == "1":
                game.spawnBarbarian(0 + 1, 0)
            elif key == "2":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "3":
                game.spawnBarbarian(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "4":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        game.render()
        game.cannonInteraction()

        if game.king:
            game.tunnelInteraction()

        if len(game.barbarians):
            for barbarian in game.barbarians:
                barbarian.moveToNearestHostileStructure(game)


init()
replay_game = copy.deepcopy(game)
animate()
game = copy.deepcopy(replay_game)


with open(f"assets/replays/replay_{datetime.datetime.now()}.txt", "w") as f:
    f.write(str(commands))

commands = []
for i, file in enumerate(sorted(os.listdir("assets/replays"))):
    print(f"{i}: {file}")
print()

idx = int(input())
if idx < len(os.listdir("assets/replays")):
    with open(f"assets/replays/{file}", "r") as f:
        commands = eval(f.read())
    REPLAY_MODE = True
    animate()
