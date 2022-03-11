structure_types = {
    "H": {
        "code": "H",
        "name": "castle",
        "visual": "Π",
        "hp": 500,
        "max_hp": 500,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#fbe08f",  # saffron
        "color_light": "#fbdb7c",  # light saffron
        "color_lighter": "#fdf0c8",  # lighter saffron
        "width": 3,
        "height": 4,
    },
    "R": {
        "code": "R",
        "name": "residence",
        "visual": "Δ",
        "hp": 200,
        "max_hp": 200,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#65f053",  # green
        "color_light": "#c6f9bf",  # light green
        "color_lighter": "#e6fde3",  # lighter green
        "width": 1,
        "height": 1,
    },
    "W": {
        "code": "W",
        "name": "wall",
        "visual": "▓",
        "hp": 200,
        "max_hp": 200,
        "hostile": True,
        "range": None,
        "damage": None,
        "color": "#96ADC8",  # grey
        "color_light": "#96ADC8",  # light grey
        "color_lighter": "#96ADC8",  # lighter grey
        "width": 1,
        "height": 1,
    },
    "C": {
        "code": "C",
        "name": "cannon",
        "visual": "Ψ",
        "hp": 200,
        "max_hp": 200,
        "hostile": True,
        "range": 5,
        "damage": 10,
        "color": "#5365f0",  # blue
        "color_light": "#b3c6f9",  # light blue
        "color_lighter": "#d3e6fd",  # lighter blue
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
        self.max_hp = self.structure["max_hp"]
        self.hostile = self.structure["hostile"]
        self.range = self.structure["range"]
        self.damage = self.structure["damage"]
        self.color = self.structure["color"]
        self.color_light = self.structure["color_light"]
        self.color_lighter = self.structure["color_lighter"]
        self.width = self.structure["width"]
        self.height = self.structure["height"]

    def display(self):
        for yy in range(self.y, self.y + self.height):
            for xx in range(self.x, self.x + self.width):
                self.game.kingdom.kingdom[yy][xx] = self.code

    def get_color(self):
        if self.hp < self.hp / 5:
            return self.color_lighter
        elif self.hp < self.hp / 2:
            return self.color_light
        else:
            return self.color


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
