"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from evennia import scripts

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        super().at_object_creation()
        # By default, rooms are not outdoors
        self.db.is_outdoors = False

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        """
        # Get the default room description
        description = super().return_appearance(looker, **kwargs)

        # If the room is outdoors, add the weather description
        if self.db.is_outdoors:
            weather_script = scripts.get_script("weather_script")
            if weather_script:
                weather_desc = weather_script.get_weather_desc()
                description += f"\\n\\n{weather_desc}"

        return description
