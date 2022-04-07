import time

from src.structure import *
from src.troop import *
from src.spell import *


class Game:
    def __init__(self, kingdom):
        self.pause = False

        self.kingdom = kingdom

        self.time = 0

        self.player = None
        self.castle = None

        self.walls = []
        self.residences = []
        self.cannons = []

        self.tunnels = []
        self.barbarians = []

        self.wallsDestroyed = 0
        self.residencesLooted = 0
        self.cannonsImpaired = 0

        self.spells = [
            RageSpell(self),
            HealSpell(self),
        ]

    def render(self):
        print("\033c", end="")

        print("Raiders of Hamdan")
        print("Time: " + str(self.time.__round__(1)) + "s")

        self.kingdom.render(self)

        if self.player:
            print("King's Health:", str(self.player.hp) + "/" + str(self.player.max_hp))
            print("King's Weapon:", self.player.weapon)

        if self.castle:
            print(
                "Castle's Health:", str(self.castle.hp) + "/" + str(self.castle.max_hp)
            )

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

    def spawnBarbarian(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["B"]["code"]
        self.barbarians.append(Barbarian(self, x, y))

    def cannonInteraction(self):
        for cannon in self.cannons:
            if (
                self.player
                and abs(self.player.x - cannon.x) <= cannon.range
                and abs(self.player.y - cannon.y) <= cannon.range
            ):
                self.player.hp -= cannon.damage
                if self.player.hp <= 0:
                    self.player = None
                    for y in range(len(self.kingdom.kingdom)):
                        for x in range(len(self.kingdom.kingdom[0])):
                            if self.kingdom.kingdom[y][x] == "H":
                                self.kingdom.kingdom[y][x] = "."
                break

        for cannon in self.cannons:
            for barbarian in self.barbarians:
                if (
                    abs(barbarian.x - cannon.x) <= cannon.range
                    and abs(barbarian.y - cannon.y) <= cannon.range
                ):
                    barbarian.hp -= cannon.damage
                    if barbarian.hp <= 0:
                        self.barbarians.remove(barbarian)
                        self.kingdom.kingdom[barbarian.y][barbarian.x] = "."
                    break

    def tunnelInteraction(self):
        for tunnel in self.tunnels:
            if (
                abs(self.player.x - tunnel.x) <= 2
                and abs(self.player.y - tunnel.y) <= 2
            ):
                if self.player.hp < self.player.max_hp:
                    self.player.hp += 5
                break

    def handleGameState(self):
        if self.player is None and len(self.barbarians) == 0:
            print("You lose!")
            return True
        elif self.castle is None and self.residences + self.walls + self.cannons == []:
            print("You win!")
            return True
        else:
            return False
