class Spell:
    def __init__(
        self,
        game,
        name,
        active,
    ):
        self.game = game
        self.name = name
        self.active = active
        self.timeActivated = 0
        self.timeDeactivated = 0


class RageSpell(Spell):
    def __init__(self, game):
        super().__init__(game, "Rage", False)

    def action(game):
        for troop in [game.player] + game.barbarians:
            troop.damage = int(troop.damage * 1.5)
            troop.speed = int(troop.speed * 1.5)


class HealSpell(Spell):
    def __init__(self, game):
        super().__init__(game, "Heal", False)

    def action(game):
        for troop in [game.player] + game.barbarians:
            troop.max_hp = int(troop.max_hp * 1.5)
            troop.hp = min(troop.hp + 500, troop.max_hp)
