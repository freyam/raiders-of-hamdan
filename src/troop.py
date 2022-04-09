import time
from src.structure import *


def log(msg):
    _ = input(msg)


troop_types = {
    "K": {
        "code": "K",
        "name": "king",
        "visual": "¶",
        "hp": 1000,
        "max_hp": 1000,
        "damage": 50,
        "speed": 1,
        "weapon": "standard",
        "color": "#E54F6D",  # red
        "color_light": "#F9B7C7",  # light red
        "color_lighter": "#FDE9F7",  # lighter red
    },
    "Q": {
        "code": "Q",
        "name": "queen",
        "visual": "¶",
        "hp": 1000,
        "max_hp": 1000,
        "damage": 30,
        "speed": 1,
        "weapon": "standard",
        "color": "#FF6EC7",  # pink
        "color_light": "#FFA9DE",  # light pink
        "color_lighter": "#FFE4F4",  # lighter pink
    },
    "B": {
        "code": "B",
        "name": "barbarian",
        "visual": "¤",
        "hp": 200,
        "max_hp": 200,
        "damage": 10,
        "speed": 1,
        "weapon": "standard",
        "color": "#f8bc80",  # light orange
        "color_light": "#f9d3b7",  # lighter orange
        "color_lighter": "#fde9f7",  # lightest orange
    },
    "A": {
        "code": "A",
        "name": "archer",
        "visual": "±",
        "hp": 100,
        "max_hp": 100,
        "damage": 5,
        "speed": 2,
        "weapon": "standard",
        "color": "#f8bc80",  # light orange
        "color_light": "#f9d3b7",  # lighter orange
        "color_lighter": "#fde9f7",  # lightest orange
    },
    "L": {
        "code": "L",
        "name": "balloon",
        "visual": "§",
        "hp": 150,
        "max_hp": 150,
        "damage": 20,
        "speed": 2,
        "weapon": "standard",
        "color": "#f8bc80",  # light orange
        "color_light": "#f9d3b7",  # lighter orange
        "color_lighter": "#fde9f7",  # lightest orange
    },
}


def is_troop(char):
    return char in troop_types


class Troop:
    def __init__(self, game, x, y, troop_code):
        self.game = game
        self.x = x
        self.y = y
        self.direction = "-"

        self.troop = troop_types[troop_code]
        self.code = self.troop["code"]
        self.name = self.troop["name"]
        self.visual = self.troop["visual"]
        self.hp = self.troop["hp"]
        self.max_hp = self.troop["max_hp"]
        self.damage = self.troop["damage"]
        self.speed = self.troop["speed"]
        self.weapon = self.troop["weapon"]
        self.color = self.troop["color"]
        self.color_light = self.troop["color_light"]
        self.color_lighter = self.troop["color_lighter"]

    def display(self):
        self.game.kingdom.kingdom[self.y][self.x] = self.code

    def get_color(self):
        if self.hp < self.structure["max_hp"] / 5:
            return self.color_lighter
        elif self.hp < self.structure["max_hp"] / 2:
            return self.color_light
        else:
            return self.color

    def move(self, game, key):
        if (
            key == "w"
            and self.y > 0
            and game.kingdom.kingdom[self.y - 1][self.x] == "."
        ):
            game.kingdom.kingdom[self.y - 1][self.x] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.y -= 1
        elif (
            key == "a"
            and self.x > 0
            and game.kingdom.kingdom[self.y][self.x - 1] == "."
        ):
            game.kingdom.kingdom[self.y][self.x - 1] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.x -= 1
        elif (
            key == "s"
            and self.y < len(game.kingdom.kingdom) - 1
            and game.kingdom.kingdom[self.y + 1][self.x] == "."
        ):
            game.kingdom.kingdom[self.y + 1][self.x] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.y += 1
        elif (
            key == "d"
            and self.x < len(game.kingdom.kingdom[0]) - 1
            and game.kingdom.kingdom[self.y][self.x + 1] == "."
        ):
            game.kingdom.kingdom[self.y][self.x + 1] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.x += 1

        if key in ["w", "a", "s", "d"]:
            self.direction = key

    def attack(self, game):
        attack_x, attack_y = self.x, self.y
        if self.direction == "w":
            attack_y -= 1
        elif self.direction == "a":
            attack_x -= 1
        elif self.direction == "s":
            attack_y += 1
        elif self.direction == "d":
            attack_x += 1

        if (
            attack_x < 0
            or attack_x >= len(game.kingdom.kingdom[0])
            or attack_y < 0
            or attack_y >= len(game.kingdom.kingdom)
        ):
            return

        if game.kingdom.kingdom[attack_y][attack_x] == ".":
            return

        if is_structure(game.kingdom.kingdom[attack_y][attack_x]):
            type = structure_types[game.kingdom.kingdom[attack_y][attack_x]]["code"]
            if type == "H":
                game.castle.hp -= self.damage

                if game.castle.hp < game.castle.max_hp / 3:
                    game.castle.color = game.castle.color_lighter
                elif game.castle.hp <= game.castle.max_hp / 2:
                    game.castle.color = game.castle.color_light

                if game.castle.hp <= 0:
                    game.castle = None
                    for y in range(len(game.kingdom.kingdom)):
                        for x in range(len(game.kingdom.kingdom[0])):
                            if game.kingdom.kingdom[y][x] == "H":
                                game.kingdom.kingdom[y][x] = "."
            elif type == "W":
                for i, wall in enumerate(game.walls):
                    if wall.x == attack_x and wall.y == attack_y:
                        game.walls[i].hp -= self.damage

                        if game.walls[i].hp < game.walls[i].max_hp / 3:
                            game.walls[i].color = game.walls[i].color_lighter
                        elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                            game.walls[i].color = game.walls[i].color_light

                        if game.walls[i].hp <= 0:
                            game.walls.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "C":
                for i, cannon in enumerate(game.cannons):
                    if cannon.x == attack_x and cannon.y == attack_y:
                        game.cannons[i].hp -= self.damage

                        if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                            game.cannons[i].color = game.cannons[i].color_lighter
                        elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                            game.cannons[i].color = game.cannons[i].color_light

                        if game.cannons[i].hp <= 0:
                            game.cannons.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "R":
                for i, residence in enumerate(game.residences):
                    if residence.x == attack_x and residence.y == attack_y:
                        game.residences[i].hp -= self.damage

                        if game.residences[i].hp < game.residences[i].max_hp / 3:
                            game.residences[i].color = game.residences[i].color_lighter
                        elif game.residences[i].hp <= game.residences[i].max_hp / 2:
                            game.residences[i].color = game.residences[i].color_light

                        if game.residences[i].hp <= 0:
                            game.residences.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "S":
                for i, space_cannon in enumerate(game.space_cannons):
                    if space_cannon.x == attack_x and space_cannon.y == attack_y:
                        game.space_cannons[i].hp -= self.damage

                        if game.space_cannons[i].hp < game.space_cannons[i].max_hp / 3:
                            game.space_cannons[i].color = game.space_cannons[
                                i
                            ].color_lighter
                        elif (
                            game.space_cannons[i].hp <= game.space_cannons[i].max_hp / 2
                        ):
                            game.space_cannons[i].color = game.space_cannons[
                                i
                            ].color_light

                        if game.space_cannons[i].hp <= 0:
                            game.space_cannons.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break


class Queen(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "Q")

    def display(self):
        return super().display()

    def move(self, game, key):
        return super().move(game, key)

    def attack(self, game):
        attack_x, attack_y = self.x, self.y

        if self.direction == "w":
            attack_y -= 8
        elif self.direction == "a":
            attack_x -= 8
        elif self.direction == "s":
            attack_y += 8
        elif self.direction == "d":
            attack_x += 8

        for y in range(attack_y - 2, attack_y + 3):
            for x in range(attack_x - 2, attack_x + 3):
                if (
                    x < 0
                    or x >= len(game.kingdom.kingdom[0])
                    or y < 0
                    or y >= len(game.kingdom.kingdom)
                ):
                    continue

                if is_structure(game.kingdom.kingdom[y][x]):
                    type = structure_types[game.kingdom.kingdom[y][x]]["code"]
                    if type == "H":
                        game.castle.hp -= self.damage

                        if game.castle.hp < game.castle.max_hp / 3:
                            game.castle.color = game.castle.color_lighter
                        elif game.castle.hp <= game.castle.max_hp / 2:
                            game.castle.color = game.castle.color_light

                        if game.castle.hp <= 0:
                            game.castle = None
                            for y in range(len(game.kingdom.kingdom)):
                                for x in range(len(game.kingdom.kingdom[0])):
                                    if game.kingdom.kingdom[y][x] == "H":
                                        game.kingdom.kingdom[y][x] = "."
                    elif type == "W":
                        for i, wall in enumerate(game.walls):
                            if wall.x == x and wall.y == y:
                                game.walls[i].hp -= self.damage

                                if game.walls[i].hp < game.walls[i].max_hp / 3:
                                    game.walls[i].color = game.walls[i].color_lighter
                                elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                                    game.walls[i].color = game.walls[i].color_light

                                if game.walls[i].hp <= 0:
                                    game.walls.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "C":
                        for i, cannon in enumerate(game.cannons):
                            if cannon.x == x and cannon.y == y:
                                game.cannons[i].hp -= self.damage

                                if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                                    game.cannons[i].color = game.cannons[
                                        i
                                    ].color_lighter
                                elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                                    game.cannons[i].color = game.cannons[i].color_light

                                if game.cannons[i].hp <= 0:
                                    game.cannons.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "R":
                        for i, residence in enumerate(game.residences):
                            if residence.x == x and residence.y == y:
                                game.residences[i].hp -= self.damage

                                if (
                                    game.residences[i].hp
                                    < game.residences[i].max_hp / 3
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_lighter
                                elif (
                                    game.residences[i].hp
                                    <= game.residences[i].max_hp / 2
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_light

                                if game.residences[i].hp <= 0:
                                    game.residences.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "S":
                        for i, space_cannon in enumerate(game.space_cannons):
                            if space_cannon.x == x and space_cannon.y == y:
                                game.space_cannons[i].hp -= self.damage

                                if (
                                    game.space_cannons[i].hp
                                    < game.space_cannons[i].max_hp / 3
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_lighter
                                elif (
                                    game.space_cannons[i].hp
                                    <= game.space_cannons[i].max_hp / 2
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_light

                                if game.space_cannons[i].hp <= 0:
                                    game.space_cannons.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break

    def attackSpecial(self, game):
        attack_x, attack_y = self.x, self.y

        if self.direction == "w":
            attack_y -= 16
        elif self.direction == "a":
            attack_x -= 16
        elif self.direction == "s":
            attack_y += 16
        elif self.direction == "d":
            attack_x += 16

        time.sleep(1)

        for y in range(attack_y - 4, attack_y + 5):
            for x in range(attack_x - 4, attack_x + 5):
                if (
                    x < 0
                    or x >= len(game.kingdom.kingdom[0])
                    or y < 0
                    or y >= len(game.kingdom.kingdom)
                ):
                    continue

                if is_structure(game.kingdom.kingdom[y][x]):
                    type = structure_types[game.kingdom.kingdom[y][x]]["code"]
                    if type == "H":
                        game.castle.hp -= self.damage

                        if game.castle.hp < game.castle.max_hp / 3:
                            game.castle.color = game.castle.color_lighter
                        elif game.castle.hp <= game.castle.max_hp / 2:
                            game.castle.color = game.castle.color_light

                        if game.castle.hp <= 0:
                            game.castle = None
                            for y in range(len(game.kingdom.kingdom)):
                                for x in range(len(game.kingdom.kingdom[0])):
                                    if game.kingdom.kingdom[y][x] == "H":
                                        game.kingdom.kingdom[y][x] = "."
                    elif type == "W":
                        for i, wall in enumerate(game.walls):
                            if wall.x == x and wall.y == y:
                                game.walls[i].hp -= self.damage

                                if game.walls[i].hp < game.walls[i].max_hp / 3:
                                    game.walls[i].color = game.walls[i].color_lighter
                                elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                                    game.walls[i].color = game.walls[i].color_light

                                if game.walls[i].hp <= 0:
                                    game.walls.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "C":
                        for i, cannon in enumerate(game.cannons):
                            if cannon.x == x and cannon.y == y:
                                game.cannons[i].hp -= self.damage

                                if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                                    game.cannons[i].color = game.cannons[
                                        i
                                    ].color_lighter
                                elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                                    game.cannons[i].color = game.cannons[i].color_light

                                if game.cannons[i].hp <= 0:
                                    game.cannons.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "R":
                        for i, residence in enumerate(game.residences):
                            if residence.x == x and residence.y == y:
                                game.residences[i].hp -= self.damage

                                if (
                                    game.residences[i].hp
                                    < game.residences[i].max_hp / 3
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_lighter
                                elif (
                                    game.residences[i].hp
                                    <= game.residences[i].max_hp / 2
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_light

                                if game.residences[i].hp <= 0:
                                    game.residences.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "S":
                        for i, space_cannon in enumerate(game.space_cannons):
                            if space_cannon.x == x and space_cannon.y == y:
                                game.space_cannons[i].hp -= self.damage

                                if (
                                    game.space_cannons[i].hp
                                    < game.space_cannons[i].max_hp / 3
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_lighter
                                elif (
                                    game.space_cannons[i].hp
                                    <= game.space_cannons[i].max_hp / 2
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_light

                                if game.space_cannons[i].hp <= 0:
                                    game.space_cannons.pop(i)
                                    game.kingdom.kingdom[y][x] = "."
                                break


class King(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "K")

    def display(self):
        return super().display()

    def move(self, game, key):
        return super().move(game, key)

    def attack(self, game):
        return super().attack(game)

    def attackSpecial(self, game):
        for direction in ["w", "a", "s", "d"]:
            attack_x, attack_y = self.x, self.y
            if direction == "w":
                attack_y -= 1
            elif direction == "a":
                attack_x -= 1
            elif direction == "s":
                attack_y += 1
            elif direction == "d":
                attack_x += 1

            if (
                attack_x < 0
                or attack_x >= len(game.kingdom.kingdom[0])
                or attack_y < 0
                or attack_y >= len(game.kingdom.kingdom)
            ):
                continue

            if game.kingdom.kingdom[attack_y][attack_x] == ".":
                continue

            if is_structure(game.kingdom.kingdom[attack_y][attack_x]):
                type = structure_types[game.kingdom.kingdom[attack_y][attack_x]]["code"]
                if type == "H":
                    game.castle.hp -= self.damage

                    if game.castle.hp < game.castle.max_hp / 3:
                        game.castle.color = game.castle.color_lighter
                    elif game.castle.hp <= game.castle.max_hp / 2:
                        game.castle.color = game.castle.color_light

                    if game.castle.hp <= 0:
                        game.castle = None
                        for y in range(len(game.kingdom.kingdom)):
                            for x in range(len(game.kingdom.kingdom[0])):
                                if game.kingdom.kingdom[y][x] == "H":
                                    game.kingdom.kingdom[y][x] = "."
                elif type == "W":
                    for i, wall in enumerate(game.walls):
                        if wall.x == attack_x and wall.y == attack_y:
                            game.walls[i].hp -= self.damage

                            if game.walls[i].hp < game.walls[i].max_hp / 3:
                                game.walls[i].color = game.walls[i].color_lighter
                            elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                                game.walls[i].color = game.walls[i].color_light

                            if game.walls[i].hp <= 0:
                                game.walls.pop(i)
                                game.kingdom.kingdom[attack_y][attack_x] = "."
                            break
                elif type == "C":
                    for i, cannon in enumerate(game.cannons):
                        if cannon.x == attack_x and cannon.y == attack_y:
                            game.cannons[i].hp -= self.damage

                            if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                                game.cannons[i].color = game.cannons[i].color_lighter
                            elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                                game.cannons[i].color = game.cannons[i].color_light

                            if game.cannons[i].hp <= 0:
                                game.cannons.pop(i)
                                game.kingdom.kingdom[attack_y][attack_x] = "."
                            break
                elif type == "R":
                    for i, residence in enumerate(game.residences):
                        if residence.x == attack_x and residence.y == attack_y:
                            game.residences[i].hp -= self.damage

                            if game.residences[i].hp < game.residences[i].max_hp / 3:
                                game.residences[i].color = game.residences[
                                    i
                                ].color_lighter
                            elif game.residences[i].hp <= game.residences[i].max_hp / 2:
                                game.residences[i].color = game.residences[
                                    i
                                ].color_light

                            if game.residences[i].hp <= 0:
                                game.residences.pop(i)
                                game.kingdom.kingdom[attack_y][attack_x] = "."
                            break
                elif type == "S":
                    for i, space_cannon in enumerate(game.space_cannons):
                        if space_cannon.x == attack_x and space_cannon.y == attack_y:
                            game.space_cannons[i].hp -= self.damage

                            if (
                                game.space_cannons[i].hp
                                < game.space_cannons[i].max_hp / 3
                            ):
                                game.space_cannons[i].color = game.space_cannons[
                                    i
                                ].color_lighter
                            elif (
                                game.space_cannons[i].hp
                                <= game.space_cannons[i].max_hp / 2
                            ):
                                game.space_cannons[i].color = game.space_cannons[
                                    i
                                ].color_light

                            if game.space_cannons[i].hp <= 0:
                                game.space_cannons.pop(i)
                                game.kingdom.kingdom[attack_y][attack_x] = "."
                            break


class Barbarian(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "B")

    def display(self):
        return super().display()

    def move(self, game, key):
        super().move(game, key)

    def attack(self, game):
        super().attack(game)

    def nearestHostileStructure(self, game):
        nearest_structure = None
        nearest_distance = None

        structures = (
            [game.castle]
            + game.walls
            + game.cannons
            + game.space_cannons
            + game.residences
        )

        for structure in structures:
            if structure and structure.hostile:
                distance = abs(self.x - structure.x) + abs(self.y - structure.y)
                if nearest_distance is None or distance < nearest_distance:
                    nearest_structure = structure
                    nearest_distance = distance

        return nearest_structure

    def moveToNearestHostileStructure(self, game):
        nearest_structure = self.nearestHostileStructure(game)

        if nearest_structure is None:
            return

        if nearest_structure.x > self.x:
            self.move(game, "d")
        elif nearest_structure.x < self.x:
            self.move(game, "a")
        elif nearest_structure.y > self.y:
            self.move(game, "s")
        elif nearest_structure.y < self.y:
            self.move(game, "w")

        if (
            abs(self.x - nearest_structure.x) <= 1
            and abs(self.y - nearest_structure.y) <= 1
        ) or (
            self.y + 1 >= len(game.kingdom.kingdom)
            or self.y - 1 < 0
            or self.x + 1 >= len(game.kingdom.kingdom[0])
            or self.x - 1 < 0
            or game.kingdom.kingdom[self.y + 1][self.x] in ["W", "H"]
            or game.kingdom.kingdom[self.y - 1][self.x] in ["W", "H"]
            or game.kingdom.kingdom[self.y][self.x + 1] in ["W", "H"]
            or game.kingdom.kingdom[self.y][self.x - 1] in ["W", "H"]
        ):
            self.attack(game)


class Archer(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "A")
        self.in_position = False

    def display(self):
        return super().display()

    def move(self, game, key):
        super().move(game, key)

    def attack(self, game):
        attack_x, attack_y = self.x, self.y

        if self.direction == "w":
            attack_y -= 1
        elif self.direction == "a":
            attack_x -= 1
        elif self.direction == "s":
            attack_y += 1
        elif self.direction == "d":
            attack_x += 1

        for y in range(attack_y - 4, attack_y + 4):
            for x in range(attack_x - 4, attack_x + 4):
                if (
                    x < 0
                    or x >= len(game.kingdom.kingdom[0])
                    or y < 0
                    or y >= len(game.kingdom.kingdom)
                ):
                    continue

                if is_structure(game.kingdom.kingdom[y][x]):
                    type = structure_types[game.kingdom.kingdom[y][x]]["code"]
                    if type == "H":
                        game.castle.hp -= self.damage

                        if game.castle.hp < game.castle.max_hp / 3:
                            game.castle.color = game.castle.color_lighter
                        elif game.castle.hp <= game.castle.max_hp / 2:
                            game.castle.color = game.castle.color_light

                        if game.castle.hp <= 0:
                            game.castle = None
                            self.in_position = False
                            for y in range(len(game.kingdom.kingdom)):
                                for x in range(len(game.kingdom.kingdom[0])):
                                    if game.kingdom.kingdom[y][x] == "H":
                                        game.kingdom.kingdom[y][x] = "."
                        break
                    elif type == "W":
                        for i, wall in enumerate(game.walls):
                            if wall.x == x and wall.y == y:
                                game.walls[i].hp -= self.damage

                                if game.walls[i].hp < game.walls[i].max_hp / 3:
                                    game.walls[i].color = game.walls[i].color_lighter
                                elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                                    game.walls[i].color = game.walls[i].color_light

                                if game.walls[i].hp <= 0:
                                    game.walls.pop(i)
                                    self.in_position = False
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "C":
                        for i, cannon in enumerate(game.cannons):
                            if cannon.x == x and cannon.y == y:
                                game.cannons[i].hp -= self.damage

                                if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                                    game.cannons[i].color = game.cannons[
                                        i
                                    ].color_lighter
                                elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                                    game.cannons[i].color = game.cannons[i].color_light

                                if game.cannons[i].hp <= 0:
                                    game.cannons.pop(i)
                                    self.in_position = False
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "R":
                        for i, residence in enumerate(game.residences):
                            if residence.x == x and residence.y == y:
                                game.residences[i].hp -= self.damage

                                if (
                                    game.residences[i].hp
                                    < game.residences[i].max_hp / 3
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_lighter
                                elif (
                                    game.residences[i].hp
                                    <= game.residences[i].max_hp / 2
                                ):
                                    game.residences[i].color = game.residences[
                                        i
                                    ].color_light

                                if game.residences[i].hp <= 0:
                                    game.residences.pop(i)
                                    self.in_position = False
                                    game.kingdom.kingdom[y][x] = "."
                                break
                    elif type == "S":
                        for i, space_cannon in enumerate(game.space_cannons):
                            if space_cannon.x == x and space_cannon.y == y:
                                game.space_cannons[i].hp -= self.damage

                                if (
                                    game.space_cannons[i].hp
                                    < game.space_cannons[i].max_hp / 3
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_lighter
                                elif (
                                    game.space_cannons[i].hp
                                    <= game.space_cannons[i].max_hp / 2
                                ):
                                    game.space_cannons[i].color = game.space_cannons[
                                        i
                                    ].color_light

                                if game.space_cannons[i].hp <= 0:
                                    game.space_cannons.pop(i)
                                    self.in_position = False
                                    game.kingdom.kingdom[y][x] = "."
                                break

    def nearestHostileStructure(self, game):
        nearest_structure = None
        nearest_distance = None

        structures = (
            [game.castle]
            + game.walls
            + game.cannons
            + game.space_cannons
            + game.residences
        )

        for structure in structures:
            if structure and structure.hostile:
                distance = abs(self.x - structure.x) + abs(self.y - structure.y)
                if nearest_distance is None or distance < nearest_distance:
                    nearest_structure = structure
                    nearest_distance = distance

        return nearest_structure

    def moveToNearestHostileStructure(self, game):
        nearest_structure = self.nearestHostileStructure(game)

        if nearest_structure is None:
            return

        if (
            abs(self.x - nearest_structure.x) <= 4
            and abs(self.y - nearest_structure.y) <= 4
            and (self.x == nearest_structure.x or self.y == nearest_structure.y)
        ):
            self.in_position = True

        if not self.in_position:
            if nearest_structure.x > self.x:
                self.move(game, "d")
            elif nearest_structure.x < self.x:
                self.move(game, "a")
            elif nearest_structure.y > self.y:
                self.move(game, "s")
            elif nearest_structure.y < self.y:
                self.move(game, "w")
        else:
            self.attack(game)

        # if self.in_position or (
        #     self.y + 1 >= len(game.kingdom.kingdom)
        #     or self.y - 1 < 0
        #     or self.x + 1 >= len(game.kingdom.kingdom[0])
        #     or self.x - 1 < 0
        #     or game.kingdom.kingdom[self.y + 1][self.x] in ["W", "H"]
        #     or game.kingdom.kingdom[self.y - 1][self.x] in ["W", "H"]
        #     or game.kingdom.kingdom[self.y][self.x + 1] in ["W", "H"]
        #     or game.kingdom.kingdom[self.y][self.x - 1] in ["W", "H"]
        # ):
        #     self.attack(game)


class Balloon(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "L")

    def display(self):
        return super().display()

    def move(self, game, key):
        if (
            key == "w"
            and self.y > 0
            and game.kingdom.kingdom[self.y - 1][self.x] == "."
        ):
            game.kingdom.kingdom[self.y - 1][self.x] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.y -= 1
        elif (
            key == "a"
            and self.x > 0
            and game.kingdom.kingdom[self.y][self.x - 1] == "."
        ):
            game.kingdom.kingdom[self.y][self.x - 1] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.x -= 1
        elif (
            key == "s"
            and self.y < len(game.kingdom.kingdom) - 1
            and game.kingdom.kingdom[self.y + 1][self.x] == "."
        ):
            game.kingdom.kingdom[self.y + 1][self.x] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.y += 1
        elif (
            key == "d"
            and self.x < len(game.kingdom.kingdom[0]) - 1
            and game.kingdom.kingdom[self.y][self.x + 1] == "."
        ):
            game.kingdom.kingdom[self.y][self.x + 1] = self.code
            game.kingdom.kingdom[self.y][self.x] = "."
            self.x += 1

        if key in ["w", "a", "s", "d"]:
            self.direction = key

    def attack(self, game):
        attack_x, attack_y = self.x, self.y

        if self.direction == "w":
            attack_y -= 1
        elif self.direction == "a":
            attack_x -= 1
        elif self.direction == "s":
            attack_y += 1
        elif self.direction == "d":
            attack_x += 1

        if (
            attack_x < 0
            or attack_x >= len(game.kingdom.kingdom[0])
            or attack_y < 0
            or attack_y >= len(game.kingdom.kingdom)
        ):
            return

        if game.kingdom.kingdom[attack_y][attack_x] == ".":
            return

        if is_structure(game.kingdom.kingdom[attack_y][attack_x]):
            type = structure_types[game.kingdom.kingdom[attack_y][attack_x]]["code"]
            if type == "H":
                game.castle.hp -= self.damage

                if game.castle.hp < game.castle.max_hp / 3:
                    game.castle.color = game.castle.color_lighter
                elif game.castle.hp <= game.castle.max_hp / 2:
                    game.castle.color = game.castle.color_light

                if game.castle.hp <= 0:
                    game.castle = None
                    for y in range(len(game.kingdom.kingdom)):
                        for x in range(len(game.kingdom.kingdom[0])):
                            if game.kingdom.kingdom[y][x] == "H":
                                game.kingdom.kingdom[y][x] = "."
            elif type == "W":
                for i, wall in enumerate(game.walls):
                    if wall.x == attack_x and wall.y == attack_y:
                        game.walls[i].hp -= self.damage

                        if game.walls[i].hp < game.walls[i].max_hp / 3:
                            game.walls[i].color = game.walls[i].color_lighter
                        elif game.walls[i].hp <= game.walls[i].max_hp / 2:
                            game.walls[i].color = game.walls[i].color_light

                        if game.walls[i].hp <= 0:
                            game.walls.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "C":
                for i, cannon in enumerate(game.cannons):
                    if cannon.x == attack_x and cannon.y == attack_y:
                        game.cannons[i].hp -= self.damage

                        if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                            game.cannons[i].color = game.cannons[i].color_lighter
                        elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                            game.cannons[i].color = game.cannons[i].color_light

                        if game.cannons[i].hp <= 0:
                            game.cannons.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "R":
                for i, residence in enumerate(game.residences):
                    if residence.x == attack_x and residence.y == attack_y:
                        game.residences[i].hp -= self.damage

                        if game.residences[i].hp < game.residences[i].max_hp / 3:
                            game.residences[i].color = game.residences[i].color_lighter
                        elif game.residences[i].hp <= game.residences[i].max_hp / 2:
                            game.residences[i].color = game.residences[i].color_light

                        if game.residences[i].hp <= 0:
                            game.residences.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "S":
                for i, space_cannon in enumerate(game.space_cannons):
                    if space_cannon.x == attack_x and space_cannon.y == attack_y:
                        game.space_cannons[i].hp -= self.damage

                        if game.space_cannons[i].hp < game.space_cannons[i].max_hp / 3:
                            game.space_cannons[i].color = game.space_cannons[
                                i
                            ].color_lighter
                        elif (
                            game.space_cannons[i].hp <= game.space_cannons[i].max_hp / 2
                        ):
                            game.space_cannons[i].color = game.space_cannons[
                                i
                            ].color_light

                        if game.space_cannons[i].hp <= 0:
                            game.space_cannons.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break

    def nearestHostileStructure(self, game):
        nearest_structure = None
        nearest_distance = None

        priority_structures = game.cannons + game.space_cannons

        if len(priority_structures) == 0:
            priority_structures = (
                [game.castle]
                + game.walls
                + game.cannons
                + game.space_cannons
                + game.residences
            )

        for structure in priority_structures:
            if structure and structure.hostile:
                distance = abs(self.x - structure.x) + abs(self.y - structure.y)
                if nearest_distance is None or distance < nearest_distance:
                    nearest_structure = structure
                    nearest_distance = distance

        return nearest_structure

    def moveToNearestHostileStructure(self, game):
        nearest_structure = self.nearestHostileStructure(game)

        if nearest_structure is None:
            return

        if nearest_structure.x > self.x:
            self.move(game, "d")
        elif nearest_structure.x < self.x:
            self.move(game, "a")
        elif nearest_structure.y > self.y:
            self.move(game, "s")
        elif nearest_structure.y < self.y:
            self.move(game, "w")

        if (
            abs(self.x - nearest_structure.x) <= 1
            and abs(self.y - nearest_structure.y) <= 1
        ) or (
            self.y + 1 >= len(game.kingdom.kingdom)
            or self.y - 1 < 0
            or self.x + 1 >= len(game.kingdom.kingdom[0])
            or self.x - 1 < 0
            or game.kingdom.kingdom[self.y + 1][self.x] in ["W", "H"]
            or game.kingdom.kingdom[self.y - 1][self.x] in ["W", "H"]
            or game.kingdom.kingdom[self.y][self.x + 1] in ["W", "H"]
            or game.kingdom.kingdom[self.y][self.x - 1] in ["W", "H"]
        ):
            self.attack(game)
