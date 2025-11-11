# mygame/world/classes.py

PROFICIENCY_MAP = {
    "awful": 10, "bad": 20, "poor": 30, "average": 40, "fair": 50,
    "good": 60, "very good": 70, "excellent": 80, "superb": 90, "perfect": 100,
}

ARMOR_TYPES = {"cloth": 1, "leather": 2, "mail": 3, "plate": 4}

class BaseClass:
    key = "base"
    armor_restriction = ARMOR_TYPES["plate"]
    skills = {}

class Rogue(BaseClass):
    key = "rogue"
    armor_restriction = ARMOR_TYPES["leather"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "pierce": 80, "scan": 80,
        "caution": 80, "sneak": 80, "swim": 80, "pick lock": 80, "dodge": 90, "climb": 80,
        "hide": 80, "throw": 80, "second attack": 80, "first aid": 80, "backstab": 80,
        "unfair fight": 80, "bluff": 80, "steal": 80, "escape": 80, "tumble": 80,
        "blindfight": 80, "kick": 80, "riding landbased": 80, "fan of knives": 80,
        "elite bluff": 80, "stun": 80, "disarm foe": 80, "poison blade": 80,
        "sense stealth": 60, "dual weapons": 80, "parrying": 80, "mounted battle": 80,
        "elite poison blade": 80, "scout": 40, "first to attack": 80, "legsweep": 80,
        "critical hit": 80, "taunt": 80, "third attack": 80, "neutralize poison": 80,
        "kick dirt": 80, "track": 40, "circle around": 80, "thieves guild": 80,
        "push": 80, "extra damage": 80, "assassinate": 60, "riding airborne": 80,
        "ambush": 80, "preparation": 80, "lethal blow": 80, "elite backstab": 80,
    }

class Paladin(BaseClass):
    key = "paladin"
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "reverse vitalize sta": 80,
        "spellcasting": 100, "pierce": 80, "scan": 80, "rescue": 80, "swim": 70, "climb": 80,
        "first aid": 80, "second attack": 80, "spellcraft": 50, "two-handed weapon": 80,
        "parrying": 80, "mounted battle": 80, "kick": 80, "bash": 80, "sense stealth": 80,
        "riding landbased": 80, "dodge": 60, "battle tactics": 80, "escape": 80, "blindfight": 80,
        "smite": 80, "third attack": 80, "push": 80, "first to attack": 80, "scout": 40,
        "dual weapons": 80, "critical hit": 80, "heroic rescue": 80, "vitalize mana": 80,
        "vitalize stamina": 80, "disarm foe": 80, "throw": 80, "extra damage": 80,
        "shield block": 80, "riding airborne": 80, "wrath": 80, "shield bash": 80, "lethal blow": 80,
        "reverse vitalize man": 80, "sense traps": 60, "read essence": 50, "psychic blast": 50,
        "accuracy": 50, "summon mount": 80, "armor": 50, "divine storm": 80, "detect evil": 80,
        "cure light": 80, "dispel evil": 90, "detect magic": 80, "bless": 20, "detect invisibility": 80,
        "word of healing": 60, "protection from evil": 80, "haste": 80, "cure blind": 60,
        "cure critic": 60, "summon": 20, "relocate": 80, "remove poison": 40, "remove curse": 80,
        "sense life": 60, "turn undead": 30, "heal": 40, "charge wand": 40, "sanctuary": 40,
        "group heal": 80, "divine wrath": 80, "regeneration": 20, "mystic shield": 10, "lay on hands": 80,
    }

class Monk(BaseClass):
    key = "monk"
    armor_restriction = ARMOR_TYPES["leather"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "martial arts": 80, "reverse vitalize sta": 80,
        "spellcasting": 100, "pierce": 80, "scan": 80, "swim": 80, "quivering palm": 80, "first aid": 80,
        "climb": 80, "spellcraft": 80, "track": 40, "spin kick": 80, "kick": 80, "pugilism": 80, "parrying": 70,
        "second attack": 80, "dodge": 80, "rescue": 80, "riding landbased": 80, "vitalize mana": 80,
        "blindfight": 80, "tumble": 80, "escape": 80, "critical hit": 80, "third attack": 80,
        "vitalize stamina": 80, "sense stealth": 80, "throw": 80, "disarm foe": 80, "meditate": 80,
        "fourth attack": 80, "neutralize poison": 80, "extra damage": 80, "strike": 80, "riding airborne": 80,
        "jab": 80, "fifth attack": 80, "shield block": 80, "lethal blow": 80, "read essence": 80, "armor": 80,
        "cure light": 60, "sense traps": 80, "detect magic": 80, "detect evil": 80, "protection from good": 80,
        "word of healing": 60, "detect invisibility": 80, "protection from evil": 60, "detect poison": 80,
        "bless": 80, "flesh restore": 80, "blindness": 60, "summon mount": 80, "remove curse": 80,
        "remove poison": 70, "detect good": 80, "cure blind": 60, "strength": 80, "haste": 80,
        "cure critic": 60, "sense life": 60, "locate object": 80, "flesh anew": 80, "accuracy": 70,
        "heal": 60, "word of recall": 60, "group heal": 80, "sanctuary": 80, "regeneration": 80, "fly": 80,
        "dexterity": 80, "portal": 80, "mystical coat": 80, "charisma": 80,
    }

class Druid(BaseClass):
    key = "druid"
    armor_restriction = ARMOR_TYPES["leather"]
    skills = {
        "stab": 40, "bludgeon": 80, "slash": 20, "chop": 30, "spellcraft": 80, "spellcasting": 100,
        "pierce": 80, "scan": 80, "swim": 80, "first aid": 80, "climb": 80, "riding landbased": 80,
        "vitalize mana": 80, "second attack": 80, "throw": 80, "track": 40, "dodge": 60,
        "critical hit": 80, "parrying": 50, "meditate": 60, "riding airborne": 80, "smash": 80,
        "dire strike": 80, "sense stealth": 40, "swipe": 80, "fade": 80, "flank attack": 80, "furious howl": 80,
        "armor": 80, "cure light": 80, "earthquake": 100, "thorn blast": 80, "read essence": 80,
        "reverse vitalize man": 80, "word of healing": 80, "bless": 80, "detect magic": 80,
        "protection from good": 80, "cat eyes": 80, "detect evil": 80, "chill touch": 80, "sense traps": 80,
        "detect invisibility": 80, "detect poison": 80, "flesh restore": 80, "blindness": 80,
        "protection from evil": 80, "shocking sphere": 80, "cure blind": 80, "detect good": 80,
        "cure critic": 80, "remove curse": 80, "dispel evil": 80, "sense life": 80, "rejuvenation": 80,
        "poison": 80, "summon mount": 80, "remove poison": 80, "star flare": 80, "strength": 80,
        "flesh anew": 80, "frostbite": 80, "word of recall": 80, "haste": 80, "enchant weapon": 80,
        "sanctuary": 80, "heal": 80, "flame blade": 80, "infravision": 80, "harm": 80, "recharge light": 80,
        "entangle": 80, "regeneration": 80, "levitation": 80, "summon": 80, "group heal": 80,
        "relocate": 80, "fog": 80, "fly": 80, "charm person": 80, "identify": 80, "slow": 80,
        "fear": 80, "group recall": 80, "psychic blast": 80, "wizard shield": 80, "mystical coat": 80,
        "accuracy": 80, "acid blast": 80, "vorpal plating": 80, "portal": 80, "charge wand": 80,
        "dire bear form": 80, "invisibility": 80, "rimefang": 80, "group relocate": 80, "flood": 80,
        "dire wolf form": 80, "blaze": 80, "mage gauntlets": 80, "lightning breath": 80, "cyclone": 80,
    }

class Bard(BaseClass):
    key = "bard"
    armor_restriction = ARMOR_TYPES["mail"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "spellcasting": 100, "pierce": 80,
        "scan": 80, "swim": 80, "climb": 80, "track": 40, "caution": 80, "parrying": 60,
        "second attack": 80, "two-handed weapon": 80, "riding landbased": 80, "bluff": 80,
        "spellcraft": 40, "unfair fight": 80, "backstab": 60, "disarm foe": 80, "sneak": 80,
        "kick": 80, "sense stealth": 50, "taunt": 80, "mounted battle": 80, "bash": 80,
        "scout": 80, "hide": 80, "circle around": 50, "dodge": 70, "pick lock": 80,
        "third attack": 80, "throw": 80, "critical hit": 80, "tumble": 80, "vitalize mana": 80,
        "shield block": 80, "escape": 80, "riding airborne": 80, "ambush": 80, "kick dirt": 80,
        "shield bash": 80, "assassinate": 50, "song of battle": 80, "song of summoning": 80,
        "song of power": 80, "strength": 40, "summon mount": 80, "magic missile": 80, "armor": 60,
        "cure light": 70, "arc fire": 60, "cure blind": 50, "burning hands": 60, "detect magic": 80,
        "protection from good": 80, "song of rejuvenation": 80, "vorpal plating": 60,
        "detect evil": 80, "blindness": 80, "chill touch": 60, "detect invisibility": 80,
        "bless": 60, "color spray": 50, "warstrike": 60, "shocking grasp": 60, "flesh restore": 60,
        "song of haste": 80, "enchant weapon": 80, "curse": 80, "fireball": 60, "remove curse": 50,
        "teleport": 50, "cure critic": 60, "flame blade": 40, "remove poison": 50, "cat eyes": 40,
        "invisibility": 60, "lightning bolt": 60, "psychic blast": 80, "read essence": 40,
        "protection from evil": 80, "sleep": 80, "word of healing": 40, "flesh anew": 50,
        "mage gauntlets": 40, "ice storm": 60, "detect good": 80, "earthquake": 50, "sanctuary": 50,
        "summon": 40, "spectre touch": 50, "relocate": 80, "group relocate": 80, "dispel evil": 50,
        "necrotic strike": 50, "levitation": 60, "shocking sphere": 50, "charm person": 80,
        "heal": 50, "song of restoration": 80, "accuracy": 40, "frostbite": 50, "sense life": 60,
        "harm": 50, "poison": 40, "quick fix": 60, "regeneration": 50, "haste": 40, "lightning breath": 60,
        "acid breath": 60, "locate object": 80, "group heal": 80, "frost breath": 60, "infravision": 40,
        "gas breath": 60, "charge wand": 40, "fly": 60, "fire breath": 60, "star flare": 50,
        "word of recall": 80, "group recall": 80, "beacon": 80, "constitution": 80, "song of devastation": 80,
        "wizard shield": 40, "reverse vitalize man": 40,
    }

class Assassin(BaseClass):
    key = "assassin"
    armor_restriction = ARMOR_TYPES["leather"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 40, "pierce": 80, "scan": 80, "caution": 80,
        "break": 80, "hide": 80, "swim": 80, "sneak": 80, "backstab": 80, "climb": 80, "throw": 80,
        "poison blade": 80, "dodge": 90, "bluff": 80, "tumble": 80, "second attack": 80, "escape": 80,
        "unfair fight": 80, "disarm foe": 80, "riding landbased": 80, "elite bluff": 80, "kick": 80,
        "blindfight": 80, "sense stealth": 80, "pick lock": 80, "stun": 80, "critical hit": 80,
        "elite poison blade": 80, "track": 60, "dual weapons": 80, "parrying": 80, "fan of knives": 80,
        "circle around": 80, "first to attack": 80, "scout": 80, "intimidate": 80, "third attack": 80,
        "assassinate": 80, "kick dirt": 80, "extra damage": 80, "neutralize poison": 80,
        "riding airborne": 80, "ambush": 80, "lethal blow": 80, "elite backstab": 80, "summon mount": 80,
    }

class DarkKnight(BaseClass):
    key = "darkknight"
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "reverse vitalize sta": 80, "spellcasting": 100,
        "pierce": 80, "scan": 80, "lifebreaker": 80, "swim": 60, "rescue": 80, "climb": 80, "second attack": 80,
        "spellcraft": 40, "two-handed weapon": 80, "parrying": 80, "caution": 80, "unfair fight": 80,
        "mounted battle": 80, "kick": 80, "battle tactics": 80, "bash": 80, "sense stealth": 80,
        "riding landbased": 80, "souldrinker": 80, "berzerk": 80, "headbang": 80, "dodge": 60,
        "kick dirt": 80, "escape": 80, "third attack": 80, "blindfight": 80, "sneak": 80,
        "first to attack": 80, "scout": 40, "hide": 80, "dual weapons": 80, "vitalize stamina": 80,
        "critical hit": 80, "track": 40, "vitalize mana": 80, "disarm foe": 80, "push": 80, "throw": 80,
        "intimidate": 80, "shield block": 80, "extra damage": 80, "riding airborne": 80, "shield bash": 80,
        "lethal blow": 80, "unholy fist": 80, "reverse vitalize man": 60, "malfesor": 80,
        "psychic blast": 60, "summon mount": 80, "magic missile": 70, "cat eyes": 40, "detect magic": 80,
        "arc fire": 60, "burning hands": 60, "protection from good": 80, "vorpal plating": 50,
        "levitation": 40, "accuracy": 50, "color spray": 50, "blindness": 60, "invisibility": 40,
        "warstrike": 50, "infravision": 40, "strength": 50, "shocking grasp": 50, "curse": 60,
        "fireball": 60, "flame blade": 40, "lightning bolt": 60, "fly": 40, "mage gauntlets": 40,
        "ice storm": 40, "death and decay": 80, "charm person": 40, "sleep": 60, "locate object": 40,
        "quick fix": 60, "beacon": 80, "poison": 50, "lightning breath": 40, "charge wand": 40,
        "acid breath": 40, "detect invisibility": 80, "bloodlust": 80, "frost breath": 40,
        "gas breath": 40, "teleport": 40, "fire breath": 40, "word of recall": 40, "necrotic strike": 80,
        "rimefang": 40, "group recall": 80, "identify": 40, "haste": 60, "mystic shield": 40,
    }

class Ranger(BaseClass):
    key = "ranger"
    armor_restriction = ARMOR_TYPES["mail"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "track": 80, "archery": 80, "spellcasting": 100,
        "pierce": 80, "scan": 80, "caution": 80, "point-blank shot": 80, "swim": 80, "sneak": 80,
        "climb": 80, "second attack": 80, "two-handed weapon": 80, "scout": 80, "kick": 80, "mounted battle": 80,
        "parrying": 60, "concussive shot": 80, "rescue": 80, "blindfight": 80, "riding landbased": 80,
        "barrage": 80, "spellcraft": 80, "third attack": 80, "headbang": 80, "battle tactics": 80,
        "disarm foe": 80, "sense stealth": 80, "hide": 80, "bash": 80, "first to attack": 80,
        "dodge": 80, "critical hit": 80, "wrath": 80, "poison blade": 80, "piercing shot": 80,
        "heroic rescue": 80, "vitalize stamina": 80, "kick dirt": 80, "throw": 80, "vitalize mana": 80,
        "extra damage": 80, "tumble": 80, "escape": 80, "push": 80, "dual weapons": 80, "riding airborne": 80,
        "meditate": 40, "shield bash": 80, "lethal blow": 80, "cat eyes": 80, "wildfire": 80,
        "detect magic": 80, "sense life": 80, "infravision": 80, "summon mount": 80, "protection from good": 80,
        "blindness": 50, "armor": 60, "detect poison": 10, "poison": 80, "cure light": 70,
        "detect evil": 80, "detect invisibility": 80, "magic missile": 50, "strength": 40,
        "remove poison": 80, "haste": 70, "frostbite": 60, "bless": 60, "detect good": 80,
        "fog": 60, "earthquake": 40, "entangle": 80, "charge wand": 40, "summon": 40,
        "relocate": 80, "locate object": 40, "enchant weapon": 50, "word of recall": 40, "heal": 40,
        "fly": 60, "group recall": 80, "identify": 40, "group heal": 80, "dexterity": 80,
    }

class Priest(BaseClass):
    key = "priest"
    armor_restriction = ARMOR_TYPES["mail"]
    skills = {
        "bludgeon": 80, "spellcraft": 80, "reverse vitalize sta": 80, "spellcasting": 100, "pierce": 80,
        "scan": 80, "first aid": 80, "climb": 80, "swim": 60, "track": 20, "riding landbased": 80,
        "second attack": 80, "parrying": 50, "throw": 80, "critical hit": 80, "vitalize mana": 80,
        "dodge": 60, "riding airborne": 80, "fade": 80, "armor": 80, "cure light": 80, "mind jab": 80,
        "detect magic": 80, "sense traps": 80, "word of healing": 80, "protection from good": 80,
        "read essence": 80, "detect invisibility": 80, "bless": 80, "chill touch": 80, "detect evil": 80,
        "invisibility": 80, "flesh restore": 80, "curse": 80, "blindness": 80, "cure blind": 80,
        "detect poison": 80, "detect good": 80, "earthquake": 80, "mind blade": 80, "remove curse": 80,
        "strength": 80, "cat eyes": 80, "cure critic": 80, "remove poison": 80, "spectre touch": 80,
        "poison": 80, "protection from evil": 80, "flesh anew": 80, "flame blade": 80, "summon mount": 80,
        "psychic blast": 80, "recharge light": 80, "dispel evil": 80, "sanctuary": 80, "sense life": 80,
        "summon": 80, "relocate": 80, "levitation": 80, "shocking sphere": 80, "haste": 80, "heal": 80,
        "frostbite": 80, "harm": 80, "accuracy": 80, "word of recall": 80, "turn undead": 80,
        "locate object": 80, "group heal": 80, "infravision": 80, "fly": 80, "regeneration": 80,
        "star flare": 80, "group recall": 80, "divine storm": 80, "identify": 80, "charge wand": 80,
        "charm person": 80, "toxic cloud": 80, "slow": 80, "portal": 80, "mystic shield": 80,
        "death strike": 80, "rimefang": 80, "restoration": 80, "holy word restore": 80,
        "purify": 80, "holy word reckoning": 80, "mystical coat": 80, "wisdom": 80, "guardian angel": 80,
    }

class Swordsman(BaseClass):
    key = "swordsman"
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "reverse vitalize sta": 80, "pierce": 80,
        "scan": 80, "caution": 80, "second attack": 80, "swim": 80, "parrying": 90, "climb": 80,
        "two-handed weapon": 80, "unfair fight": 80, "kick": 80, "rescue": 80, "bash": 80,
        "sense stealth": 80, "platebreaker": 80, "headbang": 80, "berzerk": 80, "dodge": 60,
        "battle tactics": 80, "blindfight": 80, "riding landbased": 80, "whirlwind": 80, "escape": 80,
        "mortal strike": 80, "third attack": 80, "mounted battle": 80, "defensive stance": 80,
        "disarm foe": 80, "first to attack": 80, "vitalize stamina": 80, "scout": 40, "push": 80,
        "dual weapons": 80, "critical hit": 80, "taunt": 80, "fourth attack": 80, "kick dirt": 80,
        "rage": 80, "heroic rescue": 80, "shield block": 80, "intimidate": 80, "throw": 80,
        "extra damage": 80, "fifth attack": 80, "track": 40, "riding airborne": 80,
        "shield bash": 80, "pugilism": 80, "lethal blow": 80, "summon mount": 80,
    }

class Wizard(BaseClass):
    key = "wizard"
    armor_restriction = ARMOR_TYPES["cloth"]
    skills = {
        "stab": 40, "bludgeon": 40, "slash": 30, "chop": 10, "spellcraft": 80, "spellcasting": 100,
        "pierce": 80, "scan": 80, "swim": 60, "first aid": 80, "climb": 80, "throw": 80,
        "riding landbased": 80, "escape": 80, "vitalize mana": 80, "second attack": 80,
        "critical hit": 80, "parrying": 50, "dodge": 60, "fade": 80, "riding airborne": 80,
        "magic missile": 80, "cat eyes": 80, "reverse vitalize man": 80, "detect magic": 80,
        "read essence": 60, "detect invisibility": 80, "arc fire": 80, "protection from good": 80,
        "sense traps": 80, "burning hands": 80, "vorpal plating": 80, "invisibility": 80,
        "flame blade": 80, "blindness": 80, "color spray": 80, "strength": 60, "enchant weapon": 80,
        "teleport": 80, "warstrike": 80, "detect evil": 80, "levitation": 80, "locate object": 80,
        "star flare": 80, "shocking grasp": 80, "curse": 80, "psychic blast": 80, "fireball": 80,
        "relocate": 80, "infravision": 80, "sleep": 80, "earthquake": 10, "summon mount": 80,
        "fly": 80, "lightning bolt": 80, "mage gauntlets": 60, "charm person": 60,
        "recharge light": 40, "ice storm": 80, "haste": 80, "poison": 60, "sense life": 80,
        "charge wand": 80, "word of recall": 80, "lightning breath": 80, "acid breath": 80,
        "wizard shield": 80, "frost breath": 80, "gas breath": 80, "fire breath": 80, "identify": 80,
        "phase blur": 20, "death strike": 80, "beacon": 80, "accuracy": 80, "regeneration": 10,
        "group recall": 80, "power word paralyze": 20, "rimefang": 80, "slow": 80, "mystic shield": 60,
        "portal": 80, "maelstrom": 80, "limited invulnerabil": 30, "armor": 10, "group relocate": 80,
        "power word blind": 30, "gravity focus": 80, "mystical coat": 60, "intelligence": 80,
        "wish": 80, "tensers transformati": 80, "power word kill": 10, "invulnerability": 10,
        "familiar": 80,
    }

class Necromancer(BaseClass):
    key = "necromancer"
    armor_restriction = ARMOR_TYPES["cloth"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "spellcraft": 80, "spellcasting": 100,
        "pierce": 80, "scan": 80, "swim": 80, "climb": 80, "riding landbased": 80, "throw": 80,
        "critical hit": 80, "vitalize mana": 80, "second attack": 80, "parrying": 50, "dodge": 60,
        "riding airborne": 80, "fade": 80, "pestilential blast": 80, "raise skeleton": 80,
        "detect magic": 80, "curse": 100, "invisibility": 80, "burning hands": 80, "strength": 80,
        "poison": 90, "sense traps": 80, "blindness": 80, "shocking sphere": 80, "vorpal plating": 80,
        "detect poison": 80, "summon mount": 80, "psychic blast": 80, "detect invisibility": 80,
        "shocking grasp": 80, "raise zombie": 80, "locate object": 80, "death and decay": 80,
        "fly": 80, "haste": 80, "chill touch": 80, "raise mage": 80, "harm": 80, "soul coil": 100,
        "sense life": 80, "necrotic strike": 80, "slow": 80, "relocate": 80, "spectre touch": 80,
        "rimefang": 80, "sleep": 80, "acid blast": 80, "charge wand": 80, "portal": 80, "energy drain": 80,
        "maelstrom": 80, "death touch": 100, "death coil": 100, "death strike": 90, "raise vampire": 80,
        "fear": 80, "cat eyes": 80, "mystical coat": 80, "raise dead": 80, "tensers transformati": 80,
        "wizard shield": 80, "raise dracolich": 80,
    }

class Pirate(BaseClass):
    key = "pirate"
    armor_restriction = ARMOR_TYPES["mail"]
    skills = {
        "stab": 80, "bludgeon": 80, "slash": 80, "chop": 80, "swim": 100, "pierce": 80, "scan": 80,
        "climb": 80, "sneak": 80, "caution": 80, "kick": 80, "two-handed weapon": 80, "bash": 80,
        "riding landbased": 80, "platebreaker": 80, "wrath": 80, "whirlwind": 80, "unfair fight": 80,
        "dodge": 60, "second attack": 80, "backstab": 80, "escape": 80, "headbang": 80, "bluff": 80,
        "pick lock": 80, "disarm foe": 80, "parrying": 70, "battle tactics": 80, "hide": 80,
        "steal": 80, "tumble": 80, "scout": 80, "rescue": 80, "berzerk": 80, "throw": 80,
        "blindfight": 80, "defensive stance": 80, "third attack": 80, "critical hit": 80,
        "poison blade": 80, "track": 40, "vitalize stamina": 80, "shield block": 80,
        "extra damage": 80, "riding airborne": 80, "motley crew": 80, "fourth attack": 80,
        "pugilism": 80, "shield bash": 80, "push": 80, "kick dirt": 80, "rage": 80,
        "chokehold": 80, "assassinate": 50, "double cross": 80, "thrust": 80, "summon mount": 80,
    }
