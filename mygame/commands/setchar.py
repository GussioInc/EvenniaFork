# mygame/commands/setchar.py

from evennia import Command

class CmdSetChar(Command):
    """
    Set a character's race, class, or level.

    Usage:
      +setchar <race|class|level> <key>
    """
    key = "+setchar"
    help_category = "admin"
    locks = "perm(Admin)"

    def func(self):
        """Implements the command."""
        if not self.args:
            self.msg("Usage: +setchar <race|class|level> <key>")
            return

        parts = self.args.split()
        if len(parts) != 2:
            self.msg("Usage: +setchar <race|class|level> <key>")
            return

        char_attribute, key = parts
        char_attribute = char_attribute.lower()
        key = key.lower()

        if char_attribute == "race":
            if key not in self.caller.race_handler.RACE_MAP:
                self.msg(f"Unknown race: {key}")
                return
            self.caller.db.race_key = key
            self.msg(f"Race set to {key}.")
        elif char_attribute == "class":
            if key not in self.caller.class_handler.CLASS_MAP:
                self.msg(f"Unknown class: {key}")
                return
            self.caller.db.class_key = key
            self.msg(f"Class set to {key}.")
        elif char_attribute == "level":
            try:
                level = int(key)
                if level < 1:
                    self.msg("Level must be a positive number.")
                    return
                self.caller.db.level = level
                self.msg(f"Level set to {level}.")
            except ValueError:
                self.msg("Level must be a number.")
        else:
            self.msg("Usage: +setchar <race|class|level> <key>")
