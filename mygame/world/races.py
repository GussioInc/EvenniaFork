# mygame/world/races.py

class BaseRace:
    """Base template for all races."""
    key = "base"
    desc = "This is the base race."
    max_stats = {
        "str": 18, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 18
    }
    innate_abilities = []
    classes_allowed = []

class Human(BaseRace):
    key = "human"
    desc = "Go to the nearest mirror and have a look. Maybe not the finest specimen, but you'll suffice. :)"
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 18}
    innate_abilities = ["sense stealth", "battle tactics"]
    classes_allowed = ["Priest", "Monk", "DarKnight", "Bard", "Wizard", "Druid", "Ranger", "Paladin", "Swordsman", "Assassin", "Rogue", "Pirate", "Necromancer"]

class Elf(BaseRace):
    key = "elf"
    desc = "Elves consider themselves to be 'firstborn'. Their long lifespan sometimes makes them arrogant towards their distant human cousins. They have slender lithe bodies with long, fair hair."
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 19, "con": 17, "cha": 18}
    innate_abilities = ["infravision", "tumble"]

class HalfElf(BaseRace):
    key = "half-elf"
    desc = "Part human, part elf - they prefer to be called half elf rather than half human. They are often rejected both among the elves and the humans. They share the long lifespan of the elves but have a more muscular body than elves in general."
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 18}
    innate_abilities = ["infravision", "sense passages"]
    classes_allowed = ["Priest", "Bard", "Wizard", "Druid", "Ranger", "Paladin", "Swordsman", "Warrior/Thief", "Warrior/Cleric", "Thief/Cleric", "Warrior/Magic-User", "Thief/Magic-User", "Warrior/Thief/Cleric", "Warrior/Thief/Magic-User", "Warrior/Cleric/Magic-User"]

class Dwarf(BaseRace):
    key = "dwarf"
    desc = "Don't make the mistake of calling them a dwarf. These short but stout people have biceps like a maidens waist. And we are not talking about an elf maiden. Stocky fellows who love beer, they are often described.  Besides that they fancy gold and a good fight."
    max_stats = {"str": 20, "int": 16, "wis": 18, "dex": 16, "con": 20, "cha": 17}
    innate_abilities = ["infravision"]

class Gnome(BaseRace):
    key = "gnome"
    desc = "Gnomes are distant cousins to the dwarves and halflings. They are of the same height, but not as stocky as their fellow dwarves. They are however not a trifle smarter than them.  They are often found aroung the world trying to solve the most ridiculous problems."
    max_stats = {"str": 16, "int": 20, "wis": 18, "dex": 20, "con": 18, "cha": 18}
    innate_abilities = ["infravision", "hide"]
    classes_allowed = ["Priest", "Swordsman", "Rogue", "Warrior/Thief", "Thief/Illusionist", "Warrior/Illusionist", "Warrior/Thief/Illusionist", "Warrior/Cleric/Illusionist"]

class Halfling(BaseRace):
    key = "halfling"
    desc = "These small people are often underestimated because of their size. That is their advantage however. Most halflings are peace loving and lazy, seldom leaving their village to roam among the 'giants', but there are young adventurous ones that will lighten your purse if you don't watch out."
    max_stats = {"str": 16, "int": 18, "wis": 18, "dex": 20, "con": 18, "cha": 18}
    innate_abilities = ["detect evil", "hide", "accuracy"]

class Barbarian(BaseRace):
    key = "barbarian"
    desc = "Not known for their intelligence, barbarians can be your good friend in a knock-down fight."
    max_stats = {"str": 19, "int": 17, "wis": 16, "dex": 17, "con": 19, "cha": 18}
    innate_abilities = ["berzerk", "intimidate"]

class HalfOrc(BaseRace):
    key = "half-orc"
    desc = "These poor 'cretins' were born after the orc raids on human villages, and are despised in general. They have the body of the orc and the brain of the human. They are fierce fighters and thus sometimes accepted in the cities."
    max_stats = {"str": 19, "int": 16, "wis": 16, "dex": 16, "con": 18, "cha": 16}
    innate_abilities = ["resist poison", "regeneration"]

class HalfOgre(BaseRace):
    key = "half-ogre"
    desc = "Long ago the Irda was among the fairest people on the realms. Perverted by evil magic, some have turned to the hideous Ogres. Some of them have escaped this perversion to some degree though. Stronger than the general human, the curse makes them little a dull-witted."
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 18}
    innate_abilities = ["tough skin", "parrying"]

class Changeling(BaseRace):
    key = "changeling"
    desc = "A rare race whose origins are unknown. It is said they can shift into another form."
    max_stats = {"str": 16, "int": 18, "wis": 16, "dex": 16, "con": 16, "cha": 16}
    innate_abilities = ["regeneration", "polymorph"]
    classes_allowed = ["All", "except Necromancer"]

class Fairy(BaseRace):
    key = "fairy"
    desc = "Small with gossamer wings, these playful legendary people often try to find someone to harass or joke with. They are extremely difficult to catch and often magical. If you see one, befriend it or flee!"
    max_stats = {"str": 14, "int": 20, "wis": 18, "dex": 20, "con": 16, "cha": 18}
    innate_abilities = ["fly", "sanctuary"]
    classes_allowed = ["Wizard", "Druid", "Ranger", "Warrior/Cleric", "Thief/Cleric", "Warrior/Thief/Mage"]

class Minotaur(BaseRace):
    key = "minotaur"
    desc = "Minotaurs have their own code of honor. The one still standing is the winner. These bull-like creatures are extremely strong. Even unarmed they can dismember you with their horns. Since their appearance is often intimidating enough, they seldom use their wits."
    max_stats = {"str": 20, "int": 14, "wis": 14, "dex": 18, "con": 20, "cha": 16}
    innate_abilities = ["horn butt", "intimidate"]

class Ratman(BaseRace):
    key = "ratman"
    desc = "With cruel magic, an unknown god made the sewer rats larger and more intelligent - ratmen. They are still considered to be vermin among the local people though, but accepted by most."
    max_stats = {"str": 18, "int": 17, "wis": 18, "dex": 20, "con": 17, "cha": 17}
    innate_abilities = ["sneak", "hide", "parrying"]

class Drow(BaseRace):
    key = "drow"
    desc = "These cousins to the surface elves are feared for their cruelty. They dwell in the darkness and have some innate magic abilities. They feel awkward out in the sun since their eyes have long been adjusted to darkness."
    max_stats = {"str": 18, "int": 19, "wis": 18, "dex": 18, "con": 18, "cha": 17}
    innate_abilities = ["infravision", "detect good"]

class Lizardman(BaseRace):
    key = "lizardman"
    desc = "Of unknown origin, these creatures have been on the realm probably longer than any other race. They usually avoid civilization and are hermits even among themselves. Their size and fearful snapping tail makes them worthy opponents indeed."
    max_stats = {"str": 20, "int": 16, "wis": 17, "dex": 18, "con": 18, "cha": 16}
    innate_abilities = ["tail lash", "intimidate"]

class Giant(BaseRace):
    key = "giant"
    desc = "Giants are a race of humanoids, approximately 10-14 feet tall. Giants make superb fighters because of their incredible strength, and reasonable clerics. They'd make good thieves if all locks could be overcome by brute force, but they still make damn good battering rams."
    max_stats = {"str": 21, "int": 14, "wis": 16, "dex": 14, "con": 21, "cha": 14}
    innate_abilities = ["intimidate", "extra damage"]

class Draconian(BaseRace):
    key = "draconian"
    desc = "Draconians are half-humanoid, half-dragon hybrid. Draconians make good fighters, mages and thieves generally. All Draconians are large creatures, with large wings on their backs which enable them to fly well for their bulk."
    max_stats = {"str": 19, "int": 17, "wis": 16, "dex": 17, "con": 19, "cha": 17}
    innate_abilities = ["fly", "detect good"]

class Centaur(BaseRace):
    key = "centaur"
    desc = "The Centaur is a half-man, half horse hybrid. Centaurs excel in classes related to woodlands, and make decent bards and priests as well. Most Centaurs are fond of good food and drinks, making them unpredictable and a pain in the neck at times."
    max_stats = {"str": 19, "int": 15, "wis": 15, "dex": 16, "con": 20, "cha": 18}
    innate_abilities = ["infravision", "regeneration"]

class Aarakocra(BaseRace):
    key = "aarakocra"
    desc = "A race of intelligent bird-men who live only among the highest mountain peaks. They have a wingspan of nearly 20 feet, and the males have very colorful plumage. Aarakocra are strong swift fliers, and use this to a great advantage. As a race they have only recently come into contact with humans and their ilk."
    max_stats = {"str": 17, "int": 18, "wis": 18, "dex": 19, "con": 17, "cha": 18}
    innate_abilities = ["fly", "beak dive"]

class Alaghi(BaseRace):
    key = "alaghi"
    desc = "A race of forest-dwelling humanoids with barrel chests, short legs, and long powerful arms. Alaghi are covered from head to toe with long thick hair. They stand well over 6 feet tall and weigh more than 300 pounds. They are a shy and peaceful race with a driving curiosity - it is this curiosity that has brought them out of hiding recently to join the other races of Mystical."
    max_stats = {"str": 20, "int": 16, "wis": 18, "dex": 18, "con": 18, "cha": 18}
    innate_abilities = ["beastial strength", "hide"]
    classes_allowed = ["Druid", "Ranger", "Swordsman", "Warrior/Cleric", "Warrior/Thief", "Thief/Cleric", "Warrior/Thief/Cleric"]

class Bugbear(BaseRace):
    key = "bugbear"
    desc = "Generally thought to be a race of 'monsters'. Bugbears stand about 7 feet in height with very muscular frames. They have thick hides and coarse dark hair. Most Bugbears live by plundering and ambush, taking slaves and eating anything they can kill. Some unusual representatives of the species who struggle to control their vicious temperment and natural inclination to bully others have been recently observed consorting in the towns and villages of Mystical."
    max_stats = {"str": 19, "int": 17, "wis": 18, "dex": 18, "con": 18, "cha": 17}
    innate_abilities = ["infravision", "beastial strength"]
    classes_allowed = ["Priest", "Assassin", "Swordsman", "Rogue", "Warrior/Thief", "Warrior/Cleric", "Thief/Cleric", "Warrior/Thief/Cleric"]

class Bullywug(BaseRace):
    key = "bullywug"
    desc = "Bipedal frog-like amphibians, usually inhabiting swamps, are strong swimmers and equally comfortable in or out of water. They are covered with a smooth green hide with huge frog-like faces and bulging eyes. They do not actually walk, as such, but hop."
    max_stats = {"str": 18, "int": 17, "wis": 18, "dex": 19, "con": 18, "cha": 16}
    innate_abilities = ["swim", "hide", "cat eyes"]

class Flind(BaseRace):
    key = "flind"
    desc = "Flinds are a sort of cross between a hyena and a human. They are covered with mangy brown fur, with bestial muzzles and long muscular limbs. Flinds tend to be organized and less savage than most humanoids. Still, they are quick to violence, but are more likely to consider the consequences first, then plan a careful attack later."
    max_stats = {"str": 19, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 17}
    innate_abilities = ["hide", "rabid bite"]
    classes_allowed = ["Priest", "DarKnight", "Swordsman", "Rogue", "Warrior/Thief", "Warrior/Cleric", "Warrior/Thief/Cleric"]

class Giff(BaseRace):
    key = "giff"
    desc = "A race of hulking, powerfully muscled mercenaries that resemble bipedal hippopotami. Giff are not known as towers of intellect, but they are strong and loyal. Giff society honors most the fighting prowess of an individual. Thus, they are some of the greatest warriors in the history of Mystical."
    max_stats = {"str": 20, "int": 17, "wis": 18, "dex": 17, "con": 19, "cha": 18}
    innate_abilities = ["resist magic", "regeneration"]

class Githzerai(BaseRace):
    key = "githzerai"
    desc = "A race of thin and gaunt people, with sharp features and thin faces. They are nomadic by nature, with no known homeland, but are fiercely loyal to each other. Where they come from has become a bit of a mystery on Mystical - if the Githzerai know, none of them are talking."
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 18, "con": 18, "cha": 18}
    innate_abilities = ["fade"]
    classes_allowed = ["Monk", "DarKnight", "Wizard", "Assassin", "Swordsman", "Rogue", "Warrior/Magic-User", "Thief/Magic-User", "Warrior/Thief/Magic-User"]

class Gnoll(BaseRace):
    key = "gnoll"
    desc = "Gnolls are a race of hyena-like scavengers, with a disposition to match. They are among the most chaotic of all the races of Mystical, finding it hard to see past the moment. Some members of the race do try to overcome their short tempers, and natural tendency to lie, cheat, and steal."
    max_stats = {"str": 19, "int": 17, "wis": 18, "dex": 18, "con": 18, "cha": 17}
    innate_abilities = ["unfair fight", "rabid bite"]
    classes_allowed = ["Priest", "DarKnight", "Swordsman", "Rogue", "Warrior/Thief"]

class Wemic(BaseRace):
    key = "wemic"
    desc = "Wemics are centaur-like creatures with the bodies of lions and the torso of humans. Wemics are nomads and never build a permanent home. Wemics are a very warlike race of people, they are also extremely curious about the world."
    max_stats = {"str": 18, "int": 18, "wis": 18, "dex": 17, "con": 19, "cha": 19}
    innate_abilities = ["pounce"]
