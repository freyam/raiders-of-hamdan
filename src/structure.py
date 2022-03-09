structure_types = {
    "H": {
        "name": "castle",
        "visual": "Π",
        "hp": 500,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#F05365",  # red
        "width": 3,
        "height": 4,
    },
    "R": {
        "name": "residence",
        "visual": "Δ",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#98DFAF",  # green
        "width": 1,
        "height": 1,
    },
    "W": {
        "name": "wall",
        "visual": "φ",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#414288",  # blue
        "width": 1,
        "height": 1,
    },
    "C": {
        "name": "cannon",
        "visual": "Ψ",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#96ADC8",  # grey
        "width": 1,
        "height": 1,
    },
    "T": {
        "name": "tunnel",
        "visual": "Θ",
        "hp": 100,
        "hostile": False,
        "range": None,
        "damage": None,
        "color": "#F0F0F0",  # white
        "width": 1,
        "height": 1,
    },
    "X": {
        "name": "border",
        "visual": "■",
        "hp": 100,
        "hostile": False,
        "range": None,
        "damage": None,
        "color": "#202A25",  # dark green
        "width": 1,
        "height": 1,
    },
    " ": {
        "name": "empty",
        "visual": " ",
        "hp": 0,
        "hostile": False,
        "range": None,
        "damage": None,
        "color": "#000000",  # black
        "width": 1,
        "height": 1,
    },
}


def is_structure(char):
    return char in structure_types


class Structure:
    def __init__(self, game, x, y, structure_code):
        self.game = game
        self.x = x
        self.y = y

        self.structure = structure_types[structure_code]
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
