# mygame/commands/datetime.py

from evennia import Command
from evennia.utils import gametime
import time

class CmdGameTime(Command):
    """
    Shows the current in-game time and date.

    Usage:
      time
    """
    key = "time"
    help_category = "General"

    def func(self):
        """Displays the in-game time."""
        game_time_str = gametime.get_gametime_string()
        self.caller.msg(f"The current game time is: {game_time_str}")

class CmdRealTime(Command):
    """
    Shows the current real-world server time.

    Usage:
      date
    """
    key = "date"
    help_category = "General"

    def func(self):
        """Displays the real-world time."""
        real_time_str = time.strftime("%A, %B %d, %Y, %I:%M:%S %p %Z")
        self.caller.msg(f"The current server time is: {real_time_str}")

class CmdCalendar(Command):
    """
    Shows information about the game's calendar.

    Usage:
      calendar
    """
    key = "calendar"
    help_category = "General"

    def func(self):
        """Displays calendar information."""
        self.caller.msg("This is a placeholder for the calendar command.")
