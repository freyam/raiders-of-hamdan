from src.structure import *
from src.troop import *
from src.spell import *


class Game:
    def __init__(self, kingdom):
        self.level = 1

        self.pause = False

        self.kingdom = kingdom

        self.time = 0

        self.showHUD = False
        self.showGrass = True

        self.player = None
        self.castle = None

        self.walls = []
        self.residences = []
        self.cannons = []
        self.space_cannons = []

        self.tunnels = []
        self.barbarians = []
        self.archers = []
        self.balloons = []

        self.deployed = {"barbarians": 0, "archers": 0, "balloons": 0}

        self.spells = [
            RageSpell(self),
            HealSpell(self),
        ]

    def render(self):
        print("\033c", end="")

        print("Raiders of Hamdan")
        print("Level " + str(self.level) + " Time: " + str(int(self.time)) + "s")

        self.kingdom.render(self)

        if self.player:
            print(
                "Player's Health:", str(self.player.hp) + "/" + str(self.player.max_hp)
            )
            print("Player's Weapon:", self.player.weapon)

        if self.castle:
            print(
                "Castle's Health:", str(self.castle.hp) + "/" + str(self.castle.max_hp)
            )

        if self.showHUD:

            print("Residences: ", end="")
            if len(self.residences) == 0:
                print("None")
            else:
                print()
            for residence in self.residences:
                print(
                    "  "
                    + str(residence.x)
                    + ","
                    + str(residence.y)
                    + ": "
                    + str(residence.hp)
                    + "/"
                    + str(residence.max_hp)
                )

            print("Cannons: ", end="")
            if len(self.cannons) == 0:
                print("None")
            else:
                print()
            for cannon in self.cannons:
                print(
                    "  "
                    + str(cannon.x)
                    + ","
                    + str(cannon.y)
                    + ": "
                    + str(cannon.hp)
                    + "/"
                    + str(cannon.max_hp)
                )

            print("Space Cannons: ", end="")
            if len(self.space_cannons) == 0:
                print("None")
            else:
                print()
            for space_cannon in self.space_cannons:
                print(
                    "  "
                    + str(space_cannon.x)
                    + ","
                    + str(space_cannon.y)
                    + ": "
                    + str(space_cannon.hp)
                    + "/"
                    + str(space_cannon.max_hp)
                )

            print("Barbarians: ", end="")
            if len(self.barbarians) == 0:
                print("None")
            else:
                print()
            for barbarian in self.barbarians:
                print(
                    "  "
                    + str(barbarian.x)
                    + ","
                    + str(barbarian.y)
                    + ": "
                    + str(barbarian.hp)
                    + "/"
                    + str(barbarian.max_hp)
                )

            print("Archers: ", end="")
            if len(self.archers) == 0:
                print("None")
            else:
                print()
            for archer in self.archers:
                print(
                    "  "
                    + str(archer.x)
                    + ","
                    + str(archer.y)
                    + ": "
                    + str(archer.hp)
                    + "/"
                    + str(archer.max_hp)
                    + " "
                    + str(archer.in_position)
                )

            print("Balloons: ", end="")
            if len(self.balloons) == 0:
                print("None")
            else:
                print()
            for balloon in self.balloons:
                print(
                    "  "
                    + str(balloon.x)
                    + ","
                    + str(balloon.y)
                    + ": "
                    + str(balloon.hp)
                    + "/"
                    + str(balloon.max_hp)
                )

    def spawnBarbarian(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["B"]["code"]
        self.barbarians.append(Barbarian(self, x, y))
        self.deployed["barbarians"] += 1

    def spawnArcher(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["A"]["code"]
        self.archers.append(Archer(self, x, y))
        self.deployed["archers"] += 1

    def spawnBalloon(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["L"]["code"]
        self.balloons.append(Balloon(self, x, y))
        self.deployed["balloons"] += 1

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

        for cannon in self.cannons:
            for archer in self.archers:
                if (
                    abs(archer.x - cannon.x) <= cannon.range
                    and abs(archer.y - cannon.y) <= cannon.range
                ):
                    archer.hp -= cannon.damage
                    if archer.hp <= 0:
                        self.archers.remove(archer)
                        self.kingdom.kingdom[archer.y][archer.x] = "."
                    break

    def spaceCannonInteraction(self):
        for space_cannon in self.space_cannons:
            if (
                self.player
                and abs(self.player.x - space_cannon.x) <= space_cannon.range
                and abs(self.player.y - space_cannon.y) <= space_cannon.range
            ):
                self.player.hp -= 1 * space_cannon.damage
                if self.player.hp <= 0:
                    self.player = None
                    for y in range(len(self.kingdom.kingdom)):
                        for x in range(len(self.kingdom.kingdom[0])):
                            if self.kingdom.kingdom[y][x] == "H":
                                self.kingdom.kingdom[y][x] = "."
                break

        for space_cannon in self.space_cannons:
            for barbarian in self.barbarians:
                if (
                    abs(barbarian.x - space_cannon.x) <= space_cannon.range
                    and abs(barbarian.y - space_cannon.y) <= space_cannon.range
                ):
                    for barb in self.barbarians:
                        if (
                            abs(barb.x - barbarian.x) <= 3
                            and abs(barb.y - barbarian.y) <= 3
                        ):
                            barb.hp -= 2 * space_cannon.damage
                            if barb.hp <= 0:
                                self.barbarians.remove(barb)
                                self.kingdom.kingdom[barb.y][barb.x] = "."
                    break

        for space_cannon in self.space_cannons:
            for archer in self.archers:
                if (
                    abs(archer.x - space_cannon.x) <= space_cannon.range
                    and abs(archer.y - space_cannon.y) <= space_cannon.range
                ):
                    for ar in self.archers:
                        if abs(ar.x - archer.x) <= 3 and abs(ar.y - archer.y) <= 3:
                            ar.hp -= 2 * space_cannon.damage
                            if ar.hp <= 0:
                                self.archers.remove(ar)
                                self.kingdom.kingdom[ar.y][ar.x] = "."
                    break

        for space_cannon in self.space_cannons:
            for balloon in self.balloons:
                if (
                    abs(balloon.x - space_cannon.x) <= space_cannon.range
                    and abs(balloon.y - space_cannon.y) <= space_cannon.range
                ):
                    for bal in self.balloons:
                        if abs(bal.x - balloon.x) <= 3 and abs(bal.y - balloon.y) <= 3:
                            bal.hp -= 2 * space_cannon.damage
                            if bal.hp <= 0:
                                self.balloons.remove(bal)
                                self.kingdom.kingdom[bal.y][bal.x] = "."
                    break

    def tunnelInteraction(self):
        for tunnel in self.tunnels:
            if (
                abs(self.player.x - tunnel.x) <= 2
                and abs(self.player.y - tunnel.y) <= 2
            ):
                if self.player.hp < self.player.max_hp:
                    self.player.hp += 5

                if self.player.hp > self.player.max_hp:
                    self.player.hp = self.player.max_hp
                break
