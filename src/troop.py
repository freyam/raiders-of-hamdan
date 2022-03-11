from src.structure import *

troop_types = {
    "K": {
        "code": "K",
        "name": "king",
        "visual": "¶",
        "hp": 1000,
        "max_hp": 1000,
        "damage": 100,
        "weapon": "sword",
        "color": "#E54F6D",  # red
        "color_light": "#F9B7C7",  # light red
        "color_lighter": "#FDE9F7",  # lighter red
    },
    "B": {
        "code": "B",
        "name": "barbarian",
        "visual": "⚫",
        "hp": 200,
        "max_hp": 200,
        "damage": 100,
        "weapon": "sword",
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
        self.weapon = self.troop["weapon"]
        self.color = self.troop["color"]
        self.color_light = self.troop["color_light"]
        self.color_lighter = self.troop["color_lighter"]

    def display(self):
        self.game.kingdom.kingdom[self.y][self.x] = self.code

    def get_color(self):
        if self.hp < self.structure["hp"] / 5:
            return self.color_lighter
        elif self.hp < self.structure["hp"] / 2:
            return self.color_light
        else:
            return self.color


class King(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "K")

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

    def attack(self, game, weapon):
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

        if weapon == "camel_gun":
            self.damage *= 2
        elif weapon == "sword":
            self.damage = 50

        if is_structure(game.kingdom.kingdom[attack_y][attack_x]):
            type = structure_types[game.kingdom.kingdom[attack_y][attack_x]]["code"]
            if type == "H":
                game.castle.hp -= self.damage

                if game.castle.hp <= 0:
                    game.castle = ""
                    for y in range(len(game.kingdom.kingdom)):
                        for x in range(len(game.kingdom.kingdom[0])):
                            if game.kingdom.kingdom[y][x] == "H":
                                game.kingdom.kingdom[y][x] = "."
            elif type == "W":
                for i, wall in enumerate(game.walls):
                    if wall.x == attack_x and wall.y == attack_y:
                        game.walls[i].hp -= self.damage

                        if game.walls[i].hp <= 0:
                            game.walls.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                        break
            elif type == "C":
                for i, cannon in enumerate(game.cannons):
                    if cannon.x == attack_x and cannon.y == attack_y:
                        game.cannons[i].hp -= self.damage
                        # print(
                        #     str(game.cannons[i].hp) + " " + str(game.cannons[i].color)
                        # )
                        # x = input()

                        if game.cannons[i].hp < game.cannons[i].max_hp / 3:
                            game.cannons[i].color = game.cannons[i].color_lighter
                        elif game.cannons[i].hp <= game.cannons[i].max_hp / 2:
                            game.cannons[i].color = game.cannons[i].color_light

                        if game.cannons[i].hp <= 0:
                            game.cannons.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                            game.cannonsImpaired += 1
                        break
            elif type == "R":
                for i, residence in enumerate(game.residences):
                    if residence.x == attack_x and residence.y == attack_y:
                        game.residences[i].hp -= self.damage

                        if game.residences[i].hp <= 0:
                            game.residences.pop(i)
                            game.kingdom.kingdom[attack_y][attack_x] = "."
                            game.residencesLooted += 1
                        break


class Barbarian(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "B")

    def display(self):
        return super().display()
