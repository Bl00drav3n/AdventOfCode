'''
Immune System:
228 units each with 8064 hit points (weak to cold) with an attack that does 331 cold damage at initiative 8
284 units each with 5218 hit points (immune to slashing, fire; weak to radiation) with an attack that does 160 radiation damage at initiative 10
351 units each with 4273 hit points (immune to radiation) with an attack that does 93 bludgeoning damage at initiative 2
2693 units each with 9419 hit points (immune to radiation; weak to bludgeoning) with an attack that does 30 cold damage at initiative 17
3079 units each with 4357 hit points (weak to radiation, cold) with an attack that does 13 radiation damage at initiative 1
906 units each with 12842 hit points (immune to fire) with an attack that does 100 fire damage at initiative 6
3356 units each with 9173 hit points (immune to fire; weak to bludgeoning) with an attack that does 24 radiation damage at initiative 9
61 units each with 9474 hit points with an attack that does 1488 bludgeoning damage at initiative 11
1598 units each with 10393 hit points (weak to fire) with an attack that does 61 cold damage at initiative 20
5022 units each with 6659 hit points (immune to bludgeoning, fire, cold) with an attack that does 12 radiation damage at initiative 15

Infection:
120 units each with 14560 hit points (weak to radiation, bludgeoning; immune to cold) with an attack that does 241 radiation damage at initiative 18
8023 units each with 19573 hit points (immune to bludgeoning, radiation; weak to cold, slashing) with an attack that does 4 bludgeoning damage at initiative 4
3259 units each with 24366 hit points (weak to cold; immune to slashing, radiation, bludgeoning) with an attack that does 13 slashing damage at initiative 16
4158 units each with 13287 hit points with an attack that does 6 fire damage at initiative 12
255 units each with 26550 hit points with an attack that does 167 bludgeoning damage at initiative 5
5559 units each with 21287 hit points with an attack that does 5 slashing damage at initiative 13
2868 units each with 69207 hit points (weak to bludgeoning; immune to fire) with an attack that does 33 cold damage at initiative 14
232 units each with 41823 hit points (immune to bludgeoning) with an attack that does 359 bludgeoning damage at initiative 3
729 units each with 41762 hit points (weak to bludgeoning, fire) with an attack that does 109 fire damage at initiative 7
3690 units each with 36699 hit points with an attack that does 17 slashing damage at initiative 19
'''

IMMUNE_SYSTEM = 0
INFECTION = 1

COLD = 0
SLASHING = 1
FIRE = 2
RADIATION = 3
BLUDGEONING = 4
SLASHING = 5

class Group():
    def __init__(self, group, units, hp, damage, damagetype, inititative, weaknesses, immunities):
        self.group = group
        self.units = units
        self.hp = hp
        self.damage = damage
        self.damagetype = damagetype
        self.initiative = inititative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def eff_dmg(self):
        return self.units * self.damage

    def print(self):
        print(self.units, 'units each with', self.hp, 'hit points with an attack that does', self.damage, 'damage at initiative', self.initiative)

def calc_damage(attacker, defender):
    if defender.immunities and attacker.damagetype in defender.immunities:
        return 0

    if defender.weaknesses and attacker.damagetype in defender.weaknesses:
        dmg_mul = 2
    else:
        dmg_mul = 1

    return dmg_mul * attacker.eff_dmg()

# you can tell I'm not even trying any more
def battle(groups):
    sel_groups = groups.copy()
    sel_groups.sort(key=lambda group: group.units * group.damage, reverse=True)
    targets = sel_groups.copy()
    battle_map = {}
    
    for attacker in sel_groups:
        target = None
        if targets:
            max_damage = 0
            for defender in filter(lambda g: g.group != attacker.group, targets):
                damage = calc_damage(attacker, defender)
                if damage > max_damage or (damage == max_damage and target and defender.eff_dmg() > target.eff_dmg()):
                    target = defender
                    max_damage = damage
            if target:
                targets.remove(target)
        battle_map[attacker] = target

    for attacker in groups[:]:
        defender = battle_map[attacker]
        if defender and attacker.units > 0:
            damage = calc_damage(attacker, defender)
            defender.units -= damage // defender.hp
            if defender.units <= 0:
                defender.units = 0
                groups.remove(defender)

    imm = list(filter(lambda g: g.group == IMMUNE_SYSTEM, groups))
    inf = list(filter(lambda g: g.group == INFECTION, groups))
    if len(imm) == 0 or len(inf) == 0:
        print("Immune System has", len(imm), "groups remaining:", sum(map(lambda g: g.units, imm)))
        print("Infection has", len(inf), "groups remaining:", sum(map(lambda g: g.units, inf)))
        return False
    
    return True

def create_groups(boost):
    immunesystem = [
        Group(IMMUNE_SYSTEM, 228, 8064, 331, COLD, 8, [COLD], None),
        Group(IMMUNE_SYSTEM, 284, 5218, 160, RADIATION, 10, [RADIATION], [SLASHING, FIRE]),
        Group(IMMUNE_SYSTEM, 351, 4273, 93, BLUDGEONING, 2, None, [RADIATION]),
        Group(IMMUNE_SYSTEM, 2693, 9419, 30, COLD, 17, [BLUDGEONING], [RADIATION]),
        Group(IMMUNE_SYSTEM, 3079, 4357, 13, RADIATION, 1, [RADIATION, COLD], None),
        Group(IMMUNE_SYSTEM, 906, 12842, 100, FIRE, 6, None, [FIRE]),
        Group(IMMUNE_SYSTEM, 3356, 9173, 24, RADIATION, 9, [BLUDGEONING], [FIRE]),
        Group(IMMUNE_SYSTEM, 61, 9474, 1488, BLUDGEONING, 11, None, None),
        Group(IMMUNE_SYSTEM, 1598, 10393, 61, COLD, 20, [FIRE], None),
        Group(IMMUNE_SYSTEM, 5022, 6659, 12, RADIATION, 15, None, [BLUDGEONING, FIRE, COLD])
    ]
    for group in immunesystem:
        group.damage += boost

    infection = [
        Group(INFECTION, 120, 14560, 241, RADIATION, 18, [RADIATION, BLUDGEONING], [COLD]),
        Group(INFECTION, 8023, 19573, 4, BLUDGEONING, 4, [COLD, SLASHING], [BLUDGEONING, RADIATION]),
        Group(INFECTION, 3259, 24366, 13, SLASHING, 16, [COLD], [SLASHING, RADIATION, BLUDGEONING]),
        Group(INFECTION, 4158, 13287, 6, FIRE, 12, None, None),
        Group(INFECTION, 255, 26550, 167, BLUDGEONING, 5, None, None),
        Group(INFECTION, 5559, 21287, 5, SLASHING, 13, None, None),
        Group(INFECTION, 2868, 69207, 33, COLD, 14, [BLUDGEONING], [FIRE]),
        Group(INFECTION, 232, 41823, 359, BLUDGEONING, 3, None, [BLUDGEONING]),
        Group(INFECTION, 729, 41762, 109, FIRE, 7, [BLUDGEONING, FIRE], None),
        Group(INFECTION, 3690, 36699, 17, SLASHING, 19, None, None),
    ]

    groups = immunesystem + infection
    groups.sort(key=lambda group: group.initiative, reverse=True)
    return groups

#PART 1:
group = create_groups(boost=0)
while battle(group): pass

#PART 2:
#Boost found empirically by nested intervals
group = create_groups(boost=79)
while battle(group): pass
