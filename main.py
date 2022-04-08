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

    # game.tunnels.append(Tunnel(game, 0, 0))
    game.tunnels.append(Tunnel(game, KINGDOM_WIDTH - 1, 0))
    game.tunnels.append(Tunnel(game, KINGDOM_WIDTH - 1, KINGDOM_HEIGHT - 1))
    game.tunnels.append(Tunnel(game, 0, KINGDOM_HEIGHT - 1))

    for x in range(game.castle.x - 2, game.castle.x + game.castle.width + 2):
        game.walls.append(Wall(game, x, game.castle.y - 2))
        game.walls.append(Wall(game, x, game.castle.y + game.castle.height + 1))

    for y in range(game.castle.y - 2, game.castle.y + game.castle.height + 2):
        game.walls.append(Wall(game, game.castle.x - 2, y))
        game.walls.append(Wall(game, game.castle.x + game.castle.width + 1, y))

    game.space_cannons.append(SpaceCannon(game, game.castle.x - 3, game.castle.y - 3))
    game.space_cannons.append(
        SpaceCannon(game, game.castle.x + game.castle.width + 2, game.castle.y - 3)
    )
    game.space_cannons.append(
        SpaceCannon(
            game,
            game.castle.x + game.castle.width + 2,
            game.castle.y + game.castle.height + 2,
        )
    )
    game.space_cannons.append(
        SpaceCannon(game, game.castle.x - 3, game.castle.y + game.castle.height + 2)
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

    for space_cannon in game.space_cannons:
        space_cannon.display()

    player_choice = input("(k)ing or (q)ueen? ")
    game.player = King(game, 1, 1) if player_choice == "k" else Queen(game, 1, 1)

    game.player.display()


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

        if game.player is None and len(game.barbarians) == 0:
            print("\033c")
            print("You Lost!")
            exit(0)
            break

        if (
            game.castle == None
            and len(game.residences) == 0
            and len(game.cannons) == 0
            and len(game.space_cannons) == 0
        ):
            print("\033c")
            print("You Won!")
            exit(0)
            break

        if key == "q":
            exit(0)
            break
        elif key == "p":
            game.pause = not game.pause
            continue

        if game.pause:
            continue

        game.time += 1 / 10

        if key == "h":
            for troop in [game.player] + game.barbarians:
                troop.max_hp = int(troop.max_hp * 1.5)
                troop.hp = min(troop.hp + 500, troop.max_hp)
        elif key == "r":
            for troop in [game.player] + game.barbarians:
                troop.damage = troop.damage * 2
                troop.speed = troop.speed * 2

        if game.player and key in ["w", "a", "s", "d"]:
            game.player.move(game, key)

        if key == "l":
            if game.player.weapon == "standard":
                game.player.weapon = "special"
            else:
                game.player.weapon = "standard"

        if game.player and key == " ":
            if game.player.weapon == "standard":
                game.player.attack(game)
            elif game.player.weapon == "special":
                game.player.attackSpecial(game)

        if len(game.barbarians) < 6:
            if key == "1":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "2":
                game.spawnBarbarian(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "3":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        if len(game.archers) < 6:
            if key == "4":
                game.spawnArcher(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "5":
                game.spawnArcher(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "6":
                game.spawnArcher(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        if len(game.balloons) < 3:
            if key == "7":
                game.spawnBalloon(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "8":
                game.spawnBalloon(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "9":
                game.spawnBalloon(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        game.cannonInteraction()
        game.spaceCannonInteraction()

        if game.player:
            game.tunnelInteraction()

        if len(game.barbarians):
            for barbarian in game.barbarians:
                barbarian.moveToNearestHostileStructure(game)

        if len(game.archers):
            for archer in game.archers:
                archer.moveToNearestHostileStructure(game)

        if len(game.balloons):
            for balloon in game.balloons:
                balloon.moveToNearestHostileStructure(game)

        game.render()


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
