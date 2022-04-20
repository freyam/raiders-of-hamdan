structure_types = {
    "H": {
        "code": "H",
        "name": "castle",
        "visual": "Π",
        "hp": 2000,
        "max_hp": 2000,
        "hostile": True,
        "range": None,
        "space-range": None,
        "damage": None,
        "color": "#ED6124",  # saffron
        "color_light": "#F6A27B",  # saffron
        "color_lighter": "#FEE3D1",  # light saffron
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
        "space-range": None,
        "damage": None,
        "color": "#6DE54F",  # green
        "color_light": "#A8D26D",  # light green
        "color_lighter": "#F4F269",  # lighter green
        "width": 1,
        "height": 1,
    },
    "W": {
        "code": "W",
        "name": "wall",
        "visual": "▓",
        "hp": 200,
        "max_hp": 200,
        "hostile": False,
        "range": None,
        "space-range": None,
        "damage": None,
        "color": "#5B5A59",  # grey
        "color_light": "#9F9F9E",  # light grey
        "color_lighter": "#E3E3E3",  # lighter grey
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
        "space-range": 0,
        "damage": 7,
        "color": "#0D41E1",  # blue
        "color_light": "#0A85ED",  # light blue
        "color_lighter": "#07C8F9",  # lighter blue
        "width": 1,
        "height": 1,
    },
    "S": {
        "code": "S",
        "name": "space-cannon",
        "visual": "Ψ",
        "hp": 200,
        "max_hp": 200,
        "hostile": True,
        "range": 5,
        "space-range": 5,
        "damage": 4,
        "color": "#5BF6D0",  # green
        "color_light": "#B7FBEA",  # light green
        "color_lighter": "#EFFEFA",  # lighter green
        "width": 1,
        "height": 1,
    },
    "T": {
        "code": "T",
        "name": "tunnel",
        "visual": "□",
        "hp": None,
        "max_hp": None,
        "hostile": False,
        "range": None,
        "space-range": None,
        "damage": None,
        "color": "#FF51EB",  # pink
        "color_light": "#FF51EB",  # light pink
        "color_lighter": "#FF51EB",  # lighter pink
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
        self.space_range = self.structure["space-range"]

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
        if self.hp < self.max_hp / 5:
            return self.color_lighter
        elif self.hp < self.max_hp / 2:
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


class SpaceCannon(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "S")

    def display(self):
        return super().display()


class Tunnel(Structure):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "T")

    def display(self):
        return super().display()
