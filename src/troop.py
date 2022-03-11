troop_types = {
    "K": {
        "code": "K",
        "name": "king",
        "visual": "¶",
        "hp": 1000,
        "damage": None,
        "color": "#9898f9",  # purple
    },
    "B": {
        "code": "B",
        "name": "barbarian",
        "visual": "⚫",
        "hp": 200,
        "damage": None,
        "color": "#f8bc80",  # light orange
    },
}


def is_troop(char):
    return char in troop_types


class Troop:
    def __init__(self, game, x, y, troop_code):
        self.game = game
        self.x = x
        self.y = y

        self.troop = troop_types[troop_code]
        self.code = self.troop["code"]
        self.name = self.troop["name"]
        self.visual = self.troop["visual"]
        self.hp = self.troop["hp"]
        self.damage = self.troop["damage"]
        self.color = self.troop["color"]

    def display(self):
        self.game.kingdom.kingdom[self.y][self.x] = self.code


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


class Barbarian(Troop):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "B")

    def display(self):
        return super().display()
