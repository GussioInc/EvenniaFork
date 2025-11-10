r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "mygame"

######################################################################
# Gametime setup
######################################################################

TIME_FACTOR = 48.0
TIME_GAME_EPOCH = 0
TIME_UNITS = {
    "sec": 1,
    "min": 60,
    "hr": 3600,
    "day": 86400,
    "week": 604800,
    "month": 3024000, # 35 days
    "year": 51408000, # 17 months
}
TIME_MONTH_NAMES = [
    "Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6", "Month 7", "Month 8",
    "Month 9", "Month 10", "Month 11", "Month 12", "Month 13", "Month 14", "Month 15", "Month 16", "Month 17"
]
TIME_WEEK_NAMES = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
TIME_DAY_NAMES = TIME_WEEK_NAMES
TIME_NR_MONTHS = 17
TIME_DAYS_PER_MONTH = 35
TIME_WEEKS_PER_MONTH = 5
TIME_DAYS_PER_WEEK = 7


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
