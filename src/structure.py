from colorama import Fore, Back, Style

structure_types = {
    "H": {
        "code": "H",
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
        "code": "R",
        "name": "residence",
        "visual": "Δ",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#65f053",  # green
        "width": 1,
        "height": 1,
    },
    "W": {
        "code": "W",
        "name": "wall",
        "visual": "▓",
        "hp": 100,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#5365f0",  # blue
        "width": 1,
        "height": 1,
    },
    "C": {
        "code": "C",
        "name": "cannon",
        "visual": "Ψ",
        "hp": 100,
        "hostile": True,
        "range": 5,
        "damage": 10,
        "color": "#96ADC8",  # grey
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
        self.code = self.structure["code"]
        self.name = self.structure["name"]
        self.visual = self.structure["visual"]
        self.hp = self.structure["hp"]
        self.hostile = self.structure["hostile"]
        self.range = self.structure["range"]
        self.damage = self.structure["damage"]
        self.color = self.structure["color"]
        self.width = self.structure["width"]
        self.height = self.structure["height"]

    def display(self):
        for yy in range(self.y, self.y + self.height):
            for xx in range(self.x, self.x + self.width):
                self.game.kingdom.kingdom[yy][xx] = self.code


class Castle(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "H")

    def display(self):
        return super().display()


class Residence(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "R")

    def display(self):
        return super().display()


class Wall(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "W")

    def display(self):
        return super().display()


class Cannon(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "C")

    def display(self):
        return super().display()
