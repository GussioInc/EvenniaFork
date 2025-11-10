# mygame/world/races.py

class BaseRace:
    """Base template for all races."""
    key = "base"
    max_stats = {
        "STR": 18, "INT": 18, "WIS": 18, "DEX": 18, "CON": 18, "CHA": 18
    }
    innate_abilities = []

class Human(BaseRace):
    """The Human race."""
    key = "human"

class Aarakocra(BaseRace):
    """The Aarakocra race."""
    key = "aarakocra"
    max_stats = {"STR": 17, "INT": 18, "WIS": 18, "DEX": 19, "CON": 17, "CHA": 18}
    innate_abilities = ["fly", "beak_dive"]

class Alaghi(BaseRace):
    """The Alaghi race."""
    key = "alaghi"
    max_stats = {"STR": 20, "INT": 16, "WIS": 18, "DEX": 18, "CON": 18, "CHA": 18}
    innate_abilities = ["beastial_strength", "hide"]

class Archon(BaseRace):
    """The Archon remort race."""
    key = "archon"
    max_stats = {"STR": 19, "INT": 19, "WIS": 20, "DEX": 18, "CON": 20, "CHA": 20}
    innate_abilities = ["infrared_vision", "fly", "immune_poison", "resist_magic", "immune_weapon"]

class Avatar(BaseRace):
    """The Avatar remort race."""
    key = "avatar"
    max_stats = {"STR": 21, "INT": 22, "WIS": 22, "DEX": 20, "CON": 20, "CHA": 23}
    innate_abilities = ["cat_eyes", "bless", "fly", "sanctuary", "phase_blur"]

class Barbarian(BaseRace):
    """The Barbarian race."""
    key = "barbarian"
    max_stats = {"STR": 20, "INT": 16, "WIS": 16, "DEX": 18, "CON": 19, "CHA": 17}
    innate_abilities = ["resist_poison", "resist_magic"]

class Bugbear(BaseRace):
    """The Bugbear race."""
    key = "bugbear"
    max_stats = {"STR": 19, "INT": 16, "WIS": 17, "DEX": 18, "CON": 18, "CHA": 17}
    innate_abilities = ["infrared_vision", "sneak"]

class Bullywug(BaseRace):
    """The Bullywug race."""
    key = "bullywug"
    max_stats = {"STR": 18, "INT": 17, "WIS": 18, "DEX": 19, "CON": 18, "CHA": 16}
    innate_abilities = ["swim", "hide", "cat_eyes"]

class Centaur(BaseRace):
    """The Centaur race."""
    key = "centaur"
    max_stats = {"STR": 19, "INT": 15, "WIS": 15, "DEX": 16, "CON": 20, "CHA": 18}
    innate_abilities = ["infrared_vision", "regeneration"]

class Changeling(BaseRace):
    """The Changeling race."""
    key = "changeling"
    max_stats = {"STR": 18, "INT": 18, "WIS": 18, "DEX": 18, "CON": 18, "CHA": 18}
    innate_abilities = ["disguise"]

class Daemon(BaseRace):
    """The Daemon remort race."""
    key = "daemon"
    max_stats = {"STR": 21, "INT": 20, "WIS": 20, "DEX": 21, "CON": 21, "CHA": 23}
    innate_abilities = ["infrared_vision", "regeneration", "fly", "sanctuary", "phase_blur"]

class DemiGod(BaseRace):
    """The Demi-God remort race."""
    key = "demi-god"
    max_stats = {"STR": 23, "INT": 23, "WIS": 23, "DEX": 23, "CON": 23, "CHA": 23}
    innate_abilities = ["cat_eyes", "sanctuary", "phase_blur", "mystic_shield", "regeneration", "fly"]

class Draconian(BaseRace):
    """The Draconian race."""
    key = "draconian"
    max_stats = {"STR": 19, "INT": 17, "WIS": 17, "DEX": 17, "CON": 18, "CHA": 18}
    innate_abilities = ["infrared_vision", "fly", "breath_weapon"]

class Drow(BaseRace):
    """The Drow race."""
    key = "drow"
    max_stats = {"STR": 17, "INT": 20, "WIS": 18, "DEX": 20, "CON": 16, "CHA": 18}
    innate_abilities = ["infrared_vision", "resist_magic"]

class Dwarf(BaseRace):
    """The Dwarf race."""
    key = "dwarf"
    max_stats = {"STR": 20, "INT": 16, "WIS": 18, "DEX": 16, "CON": 20, "CHA": 17}
    innate_abilities = ["infrared_vision"]

class Eldar(BaseRace):
    """The Eldar remort race."""
    key = "eldar"
    max_stats = {"STR": 18, "INT": 19, "WIS": 19, "DEX": 19, "CON": 18, "CHA": 19}
    innate_abilities = ["cat_eyes", "bless", "armor"]

class Elemental(BaseRace):
    """The Elemental remort race."""
    key = "elemental"
    max_stats = {"STR": 22, "INT": 20, "WIS": 20, "DEX": 21, "CON": 21, "CHA": 23}
    innate_abilities = ["infrared_vision", "regeneration", "levitation", "sanctuary", "mage_gauntlets", "phase_blur"]

class Elf(BaseRace):
    """The Elf race."""
    key = "elf"
    max_stats = {"STR": 18, "INT": 18, "WIS": 18, "DEX": 19, "CON": 17, "CHA": 18}
    innate_abilities = ["infrared_vision", "tumble"]

class Fairy(BaseRace):
    """The Fairy race."""
    key = "fairy"
    max_stats = {"STR": 14, "INT": 20, "WIS": 18, "DEX": 20, "CON": 16, "CHA": 18}
    innate_abilities = ["fly", "sanctuary"]

class Flind(BaseRace):
    """The Flind race."""
    key = "flind"
    max_stats = {"STR": 19, "INT": 18, "WIS": 18, "DEX": 18, "CON": 18, "CHA": 17}
    innate_abilities = ["hide", "rabid_bite"]

class Giant(BaseRace):
    """The Giant race."""
    key = "giant"
    max_stats = {"STR": 21, "INT": 14, "WIS": 16, "DEX": 14, "CON": 21, "CHA": 14}
    innate_abilities = ["intimidate", "extra_damage"]

class Giff(BaseRace):
    """The Giff race."""
    key = "giff"
    max_stats = {"STR": 20, "INT": 17, "WIS": 18, "DEX": 17, "CON": 19, "CHA": 18}
    innate_abilities = ["resist_magic", "regeneration"]

class Githzerai(BaseRace):
    """The Githzerai race."""
    key = "githzerai"
    max_stats = {"STR": 18, "INT": 18, "WIS": 18, "DEX": 18, "CON": 18, "CHA": 18}
    innate_abilities = ["fade"]

class Gnoll(BaseRace):
    """The Gnoll race."""
    key = "gnoll"
    max_stats = {"STR": 18, "INT": 16, "WIS": 17, "DEX": 18, "CON": 18, "CHA": 17}
    innate_abilities = ["infrared_vision"]

class Gnome(BaseRace):
    """The Gnome race."""
    key = "gnome"
    max_stats = {"STR": 17, "INT": 19, "WIS": 19, "DEX": 18, "CON": 16, "CHA": 18}
    innate_abilities = ["infrared_vision", "resist_magic"]

class Golem(BaseRace):
    """The Golem remort race."""
    key = "golem"
    max_stats = {"STR": 19, "INT": 18, "WIS": 18, "DEX": 19, "CON": 19, "CHA": 18}
    innate_abilities = ["armor", "vorpal_plating", "regeneration"]

class HalfElf(BaseRace):
    """The Half-Elf race."""
    key = "half-elf"
    max_stats = {"STR": 18, "INT": 18, "WIS": 18, "DEX": 18, "CON": 17, "CHA": 18}
    innate_abilities = ["infrared_vision"]

class HalfOgre(BaseRace):
    """The Half-Ogre race."""
    key = "half-ogre"
    max_stats = {"STR": 20, "INT": 16, "WIS": 17, "DEX": 16, "CON": 20, "CHA": 16}
    innate_abilities = ["infrared_vision"]

class HalfOrc(BaseRace):
    """The Half-Orc race."""
    key = "half-orc"
    max_stats = {"STR": 19, "INT": 17, "WIS": 17, "DEX": 17, "CON": 19, "CHA": 17}
    innate_abilities = ["infrared_vision"]

class Halfling(BaseRace):
    """The Halfling race."""
    key = "halfling"
    max_stats = {"STR": 16, "INT": 18, "WIS": 18, "DEX": 20, "CON": 18, "CHA": 18}
    innate_abilities = ["detect_evil", "hide", "accuracy"]

class Lich(BaseRace):
    """The Lich remort race."""
    key = "lich"
    max_stats = {"STR": 17, "INT": 20, "WIS": 19, "DEX": 18, "CON": 20, "CHA": 18}
    innate_abilities = ["infrared_vision", "regeneration", "resist_cold", "immune_poison", "resist_magic", "immune_weapon"]

class Lizardman(BaseRace):
    """The Lizardman race."""
    key = "lizardman"
    max_stats = {"STR": 18, "INT": 17, "WIS": 17, "DEX": 17, "CON": 19, "CHA": 17}
    innate_abilities = ["waterbreath", "infrared_vision"]

class Minotaur(BaseRace):
    """The Minotaur race."""
    key = "minotaur"
    max_stats = {"STR": 20, "INT": 16, "WIS": 17, "DEX": 17, "CON": 19, "CHA": 17}
    innate_abilities = ["infrared_vision", "horn_butt"]

class Prophet(BaseRace):
    """The Prophet remort race."""
    key = "prophet"
    max_stats = {"STR": 18, "INT": 19, "WIS": 20, "DEX": 18, "CON": 20, "CHA": 20}
    innate_abilities = ["infrared_vision", "sense_life", "regeneration", "resist_magic", "immune_poison", "immune_weapon"]

class Ratman(BaseRace):
    """The Ratman race."""
    key = "ratman"
    max_stats = {"STR": 18, "INT": 17, "WIS": 17, "DEX": 19, "CON": 18, "CHA": 17}
    innate_abilities = ["infrared_vision"]
