# TODO - Implementation Uncertainties

This file tracks design questions and areas where the `crawl.txt` help files are ambiguous. We can review this file in subsequent sessions to make decisions on how to proceed.

## Core Combat Mechanics

The current combat calculation is a placeholder. To faithfully recreate the MUD, we need to implement a system based on Armor Class (AC), Hitroll, and Damroll.

*   **Armor Class (AC)**: The `HELP ARMOR CLASS` entry states "A lower AC is better." How should AC be calculated? It seems to be a combination of armor worn, Dexterity, level, and spells. We need to define the formula for this.
*   **Hitroll**: This attribute adds a bonus to the chance to hit. How does it interact with the target's AC? Is it a direct comparison (e.g., `roll + hitroll vs. AC`) or a more complex formula?
*   **Damroll**: This attribute adds a bonus to damage on each successful hit. Should this be a flat addition to the weapon's base damage?
*   **Implementation**: Where should this logic live? It seems like the `at_damage` hook in `characters.py` is a good place for the final damage calculation, but the "to-hit" roll should happen before that, likely in the `CombatHandler`.

## Death, Corpses, and Experience Loss

The `HELP CHEATING DEATH` and `HELP DYING` entries describe a clear death cycle.

*   **Experience Loss**: What is the formula for XP loss on death? Is it a flat percentage of the current level's XP?
*   **Corpse Mechanics**:
    *   A corpse is created on death, holding all the character's equipment. Should this be a new object typeclass?
    *   Corpses decay after "about 3 real-life hours". We will need a script to handle this cleanup.
    *   The `get corpse` command is mentioned. How does this differ from `get all from corpse`?
*   **Recall Point**: Characters return to their "recall point" on death. We need a way to set and store this location on the character.
*   **Corpse Keepers**: The `HELP CORPSE KEEPER` mentions an NPC that can retrieve a corpse for a fee. This will be a good feature to add after the basic death mechanics are in place.

## Economy and Items

The MUD has shops for buying and selling, and a bank for storing gold.

*   **Shops**: We will need to create a new NPC typeclass for shopkeepers, with a custom `list`, `buy`, and `sell` command set. How is the sell price determined? Is it a percentage of the item's value?
*   **Bank**: The bank allows depositing and withdrawing gold. We'll need a "banker" NPC and a way to store the player's bank balance on their character.
*   **Item Properties**: To support shops and a more detailed game world, items will need more properties:
    *   **Equipment Slots**: Where can the item be worn? (e.g., head, body, legs, hands).
    *   **Weapon/Armor Types**: `HELP ARMOR TYPES` and `HELP PROFICIENCIES` mention types like `Plate`, `Leather`, `Slash`, `Pierce`. These will be important for class restrictions and skill bonuses.
    *   **Value**: How much is the item worth in gold?

## Grouping Mechanics

The `HELP GROUP` entry describes how players can form groups.

*   **Experience Sharing**: How is XP shared among group members? Is it split evenly? Do members have to be in the same room or area?
*   **Group Commands**: We will need to implement the `group` command to invite players and the `gt` (group tell) command for communication.

## Racial Innate Abilities

**Design Note (2025-11-07):** Most innate abilities are the spell or skill of the same name, but without a cooldown timer. This should be the default implementation approach.

The `crawl.txt` file lists many innate abilities for races. The exact mechanics for these are not always clear.

*   **Fly**: (Aarakocra, Archon, Avatar, Daemon, Draconian, Fairy, DemiGod, Elemental)
    *   Should this be an active command (`fly`) or a passive flag?
    *   If passive, how does it interact with the environment? (e.g., allows entering rooms with a "fly-only" flag, avoids floor traps, etc.)
    *   Does it have a movement point cost?

*   **Infrared Vision / Cat Eyes**: (Many races)
    *   Should this automatically allow seeing in dark rooms without a light source?
    *   Is there a difference between "Infrared Vision" and "Cat Eyes"?

*   **Resistances**: (e.g., Aarakocra's `Resist Lightning`, Barbarian's `Resist Poison` and `Resist Magic`)
    *   What percentage of damage reduction should these provide? (e.g., 25%, 50%?)
    *   Should `Resist Magic` apply to all magical damage, or just a chance to resist debuffs?

*   **Immunities**: (e.g., Archon's `Immune Poison`, `Immune Weapon`)
    *   `Immune Poison`: Does this prevent all poison effects, including damage and stat drains?
    *   `Immune Weapon`: Does this mean immunity to all non-magical physical damage?

*   **Regeneration**: (Alaghi, Arch-Devil, etc.)
    *   How fast should this be? (e.g., X HP per minute)
    *   Does it work in combat?

*   **Specific Abilities**:
    *   `Beak Dive` (Aarakocra): What are the mechanics of this skill? Damage, cooldown?
    *   `Breath Weapon` (Draconian): The help file is ambiguous about which colors have which breath weapons.
    *   `Disguise` (Changeling): How should this work? Can the player choose a specific appearance?

## Incomplete Help Files

*   `HELP BIRTH`: Marked as "Not implemented yet". Should we implement a family/birth system?
*   `[Review]` tags: Many files are marked with `[Review]`. We will need to make design decisions for these.

## Character Creation

*   How should the initial race and class selection be presented to the player? The current system defaults to a Human Warrior. We will need to create a character creation menu system.

## Skill & Spell Mechanics

*   **Damage Formulas**: The help files rarely specify exact damage. I will need to devise balanced formulas for skills and spells (e.g., `Bash`, `Kick`). The initial implementation will be a best guess based on descriptions.
*   **Success Chances**: Skills like `Disarm` or `Bash` (for stunning) will require a success chance calculation, likely based on attacker's skill/stats vs. defender's stats. These will be implemented with placeholder logic for now.
*   **Mage Spell Assumptions**:
    *   `Burning Hands`: Implemented as a simple low-damage direct-damage spell.
    *   `Chill Touch`: Implemented as a low-damage spell that also applies a short-duration Strength debuff. The debuff amount is currently a fixed value.
    *   `Armor`: Implemented as a buff that provides a fixed amount of damage reduction. This is a temporary stand-in for a proper Armor Class (AC) system.
    *   `Invisibility`: Implemented as a simple "invisibility" buff. The game logic does not yet check for this buff to prevent targeting.
