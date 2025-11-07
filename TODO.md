# TODO - Implementation Uncertainties

This file tracks design questions and areas where the `crawl.txt` help files are ambiguous. We can review this file in subsequent sessions to make decisions on how to proceed.

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
