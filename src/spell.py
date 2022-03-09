spell_types = {"rage": {"active": False}, "heal": {"active": False}}


class Spell:
    def __init__(self, game, x, y, spell_code):
        self.game = game
        self.spell = spell_types[spell_code]
        self.name = self.spell["name"]
        self.active = self.spell["active"]
