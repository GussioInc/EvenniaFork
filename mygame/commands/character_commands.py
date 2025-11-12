# mygame/commands/character_commands.py

from evennia import Command
from world.utils import get_proficiency_rating

class CmdSkills(Command):
    """
    Displays your known skills and their proficiency.

    Usage:
      skills
    """
    key = "skills"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Implements the skills command."""
        caller = self.caller

        if not caller.db.known_skills:
            caller.msg("You have not learned any skills yet.")
            return

        table = self.styled_table("|wSkill", "|wProficiency", "|wMax")

        for skill_key, data in sorted(caller.db.known_skills.items()):
            prof_rating = get_proficiency_rating(data.get("proficiency", 1))
            max_rating = get_proficiency_rating(data.get("max", 100))
            table.add_row(skill_key, prof_rating, max_rating)

        caller.msg(str(table))
