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

player_choice = input("(k)ing or (q)ueen? ")


def init():
    game.player = King(game, 1, 1) if player_choice == "k" else Queen(game, 1, 1)
    game.castle = Castle(game, int(KINGDOM_WIDTH / 2 - 3), int(KINGDOM_HEIGHT / 2 - 2))
    game.castle.display()

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
    game.space_cannons.append(
        SpaceCannon(game, game.castle.x + game.castle.width + 2, game.castle.y - 3)
    )
    game.cannons.append(
        Cannon(
            game,
            game.castle.x + game.castle.width + 2,
            game.castle.y + game.castle.height + 2,
        )
    )
    game.space_cannons.append(
        SpaceCannon(game, game.castle.x - 3, game.castle.y + game.castle.height + 2)
    )

    hostile_structure_prob = None

    if game.level == 1:
        hostile_structure_prob = 0
    elif game.level == 2:
        hostile_structure_prob = 0.001
    elif game.level == 3:
        hostile_structure_prob = 0.0015

    for x in range(KINGDOM_WIDTH):
        for y in range(KINGDOM_HEIGHT):
            if (
                game.kingdom.kingdom[y][x] == "."
                and (x < game.castle.x - 2 or x > game.castle.x + game.castle.width + 1)
                and not (
                    x == 0
                    or x == KINGDOM_WIDTH - 1
                    or y == 0
                    or y == KINGDOM_HEIGHT - 1
                )
            ):
                if random.random() < hostile_structure_prob:
                    game.cannons.append(Cannon(game, x, y))
                elif random.random() < hostile_structure_prob * 2:
                    game.space_cannons.append(SpaceCannon(game, x, y))

    for x in range(KINGDOM_WIDTH):
        for y in range(KINGDOM_HEIGHT):
            if (
                game.kingdom.kingdom[y][x] == "."
                and (x < game.castle.x - 2 or x > game.castle.x + game.castle.width + 1)
                and not (
                    x == 0
                    or x == KINGDOM_WIDTH - 1
                    or y == 0
                    or y == KINGDOM_HEIGHT - 1
                )
            ):
                if random.random() < 0.005:
                    game.residences.append(Residence(game, x, y))
                elif random.random() < 0.01:
                    game.walls.append(Wall(game, x, y))

    game.castle.display()

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

        if (
            game.player is None
            and game.deployed["barbarians"] == 6
            and game.deployed["archers"] == 6
            and game.deployed["balloons"] == 3
        ):
            print("\033c")
            print("You Lost!")
            exit(0)
            break
        elif (
            game.castle == None
            and len(game.residences) == 0
            and len(game.cannons) == 0
            and len(game.space_cannons) == 0
        ):
            if game.level == 3:
                print("\033c")
                print("You Won!")
                exit(0)
                break

            game.level += 1

            for x in range(KINGDOM_WIDTH):
                for y in range(KINGDOM_HEIGHT):
                    game.kingdom.kingdom[y][x] = "."

            game.time = 0

            game.player = None
            game.castle = None

            game.walls = []
            game.residences = []
            game.cannons = []
            game.space_cannons = []

            game.tunnels = []
            game.barbarians = []
            game.archers = []
            game.balloons = []

            game.deployed = {"barbarians": 0, "archers": 0, "balloons": 0}

            init()
            animate()

        if key == "q":
            exit(0)
            break
        elif key == "p":
            game.pause = not game.pause
            continue

        if game.pause:
            continue

        game.time += 1 / 10

        if key == "m":
            game.showGrass = not game.showGrass

        if key == "n":
            game.showHUD = not game.showHUD

        troops = game.barbarians + game.archers + game.balloons

        if key == "h":
            for troop in [game.player] + troops:
                troop.max_hp = int(troop.max_hp * 1.5)
                troop.hp = min(troop.hp + 500, troop.max_hp)
        elif key == "r":
            for troop in [game.player] + troops:
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

        if game.deployed["barbarians"] < 5:
            if key == "1":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "2":
                game.spawnBarbarian(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "3":
                game.spawnBarbarian(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        if game.deployed["archers"] < 5:
            if key == "4":
                game.spawnArcher(KINGDOM_WIDTH - 1 - 1, 0)
            elif key == "5":
                game.spawnArcher(0 + 1, KINGDOM_HEIGHT - 1)
            elif key == "6":
                game.spawnArcher(KINGDOM_WIDTH - 1 - 1, KINGDOM_HEIGHT - 1)

        if game.deployed["balloons"] < 2:
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

        for troop in troops:
            troop.moveToNearestHostileStructure(game)

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
