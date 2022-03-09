troop_types = {
    "K": {
        "name": "king",
        "visual": "Π",
        "hp": 500,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#F05365",  # red
        "width": 3,
        "height": 4,
    },
    "B": {
        "name": "barbarian",
        "visual": "Ψ",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#96ADC8",  # grey
        "width": 1,
        "height": 1,
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
        self.name = self.structure["name"]
        self.visual = self.structure["visual"]
        self.hp = self.structure["hp"]
        self.hostile = self.structure["hostile"]
        self.range = self.structure["range"]
        self.damage = self.structure["damage"]
        self.color = self.structure["color"]
        self.width = self.structure["width"]
        self.height = self.structure["height"]

    def draw(self):
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                self.game.kingdom[y][x] = self.visual
        return self
