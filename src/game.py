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
        self.space_cannons = []

        self.tunnels = []
        self.barbarians = []
        self.archers = []
        self.balloons = []

        self.wallsDestroyed = 0
        self.residencesLooted = 0
        self.cannonsImpaired = 0
        self.spaceCannonsImpaired = 0

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
            print(
                "Player's Health:", str(self.player.hp) + "/" + str(self.player.max_hp)
            )
            print("Player's Weapon:", self.player.weapon)

        if self.castle:
            print(
                "Castle's Health:", str(self.castle.hp) + "/" + str(self.castle.max_hp)
            )

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

    def spawnBarbarian(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["B"]["code"]
        self.barbarians.append(Barbarian(self, x, y))

    def spawnArcher(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["A"]["code"]
        self.archers.append(Archer(self, x, y))

    def spawnBalloon(self, x, y):
        self.kingdom.kingdom[y][x] = troop_types["L"]["code"]
        self.balloons.append(Balloon(self, x, y))

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
                self.player.hp -= space_cannon.damage
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
                            barb.hp -= space_cannon.damage
                            if barb.hp <= 0:
                                self.barbarians.remove(barb)
                                self.kingdom.kingdom[barb.y][barb.x] = "."
                    break

            for space_cannon in self.space_cannons:
                for balloon in self.balloons:
                    if (
                        abs(balloon.x - space_cannon.x) <= space_cannon.range
                        and abs(balloon.y - space_cannon.y) <= space_cannon.range
                    ):
                        balloon.hp -= space_cannon.damage
                        if balloon.hp <= 0:
                            self.balloons.remove(balloon)
                            self.kingdom.kingdom[balloon.y][balloon.x] = "."
                        break

            for space_cannon in self.space_cannons:
                for archer in self.archers:
                    if (
                        abs(archer.x - space_cannon.x) <= space_cannon.range
                        and abs(archer.y - space_cannon.y) <= space_cannon.range
                    ):
                        archer.hp -= space_cannon.damage
                        if archer.hp <= 0:
                            self.archers.remove(archer)
                            self.kingdom.kingdom[archer.y][archer.x] = "."
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

    # def handleGameState(self):
    #     if self.player is None and len(self.barbarians) == 0:
    #         print("You lose!")
    #         return True
    #     elif self.castle is None and self.residences + self.walls + self.cannons == []:
    #         print("You win!")
    #         return True
    #     else:
    #         return False
