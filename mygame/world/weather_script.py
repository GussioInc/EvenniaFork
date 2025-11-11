# mygame/world/weather_script.py

from evennia import DefaultScript
from evennia.utils import gametime
import math
import random

# Constants
DAYS_PER_YEAR = 595  # 17 months * 35 days
# Seasons are roughly a quarter of the year
SPRING_STARTS = 1
SUMMER_STARTS = 149
AUTUMN_STARTS = 298
WINTER_STARTS = 447

# Solstices and Equinoxes (approximate days of the year)
SUMMER_SOLSTICE = 223  # Mid-summer, longest day
WINTER_SOLSTICE = 521  # Mid-winter, shortest day

# Day length variation in minutes (90 minutes total / 2 for each side of noon)
DAYLIGHT_VARIATION_MINUTES = 45

WEATHER_PATTERNS = {
    "Spring": ["a gentle breeze blows", "a light rain falls", "the sun shines brightly"],
    "Summer": ["the sun beats down mercilessly", "a warm wind rustles the leaves", "the air is hot and still"],
    "Autumn": ["a crisp wind blows", "the sky is overcast", "a cool rain falls"],
    "Winter": ["a cold wind blows from the north", "snowflakes drift down from the sky", "the air is frigid"]
}

# Change weather every X in-game hours
WEATHER_UPDATE_RATE = 3

class WeatherScript(DefaultScript):
    """
    This script manages the global weather, seasons, and day/night cycle.
    """
    def at_script_creation(self):
        """Called when the script is first created."""
        self.key = "weather_script"
        self.desc = "Manages weather, seasons, and day/night."
        # Set the ticker to run once per in-game hour.
        # 3600 game seconds / 48 time_factor = 75 real seconds.
        self.interval = 75
        self.persistent = True

        # Store the current state
        self.db.is_day = True
        self.db.current_weather = "clear"
        self.db.last_weather_change = gametime.gametime()

    def get_day_of_year(self):
        """Calculates the current day of the year (1-595)."""
        time_info = gametime.get_gametime_info()
        # Month is 1-indexed, so we subtract 1
        day_of_year = (time_info["month"] - 1) * gametime.DAYS_PER_MONTH + time_info["day"]
        return day_of_year

    def get_season(self):
        """Determines the current season."""
        day = self.get_day_of_year()
        if WINTER_STARTS <= day or day < SUMMER_STARTS:
            return "Winter"
        elif SUMMER_STARTS <= day < AUTUMN_STARTS:
            return "Summer"
        elif AUTUMN_STARTS <= day < WINTER_STARTS:
            return "Autumn"
        else: # Spring is the default
            return "Spring"

    def get_sunrise_sunset(self):
        """
        Calculates the sunrise and sunset time for the current day.
        The calculation uses a cosine wave to create a smooth variation
        in day length throughout the year.
        """
        day = self.get_day_of_year()

        # Calculate the deviation in minutes from the 6am/6pm standard
        # cos peaks at 1, so we use -(...) to make summer have the biggest negative deviation (earliest sunrise)
        deviation_minutes = -DAYLIGHT_VARIATION_MINUTES * math.cos(2 * math.pi * (day - SUMMER_SOLSTICE) / DAYS_PER_YEAR)

        # Base times are 6:00 and 18:00
        sunrise_base_minutes = 6 * 60
        sunset_base_minutes = 18 * 60

        sunrise_total_minutes = sunrise_base_minutes + deviation_minutes
        sunset_total_minutes = sunset_base_minutes - deviation_minutes

        # Convert total minutes back to hours and minutes
        sunrise_hour = int(sunrise_total_minutes // 60)
        sunrise_minute = int(sunrise_total_minutes % 60)
        sunset_hour = int(sunset_total_minutes // 60)
        sunset_minute = int(sunset_total_minutes % 60)

        return (sunrise_hour, sunrise_minute), (sunset_hour, sunset_minute)

    def at_repeat(self):
        """
        Called every in-game hour to update the time, weather, and day/night state.
        """
        time_info = gametime.get_gametime_info()
        current_hour = time_info["hour"]

        (sunrise_hour, _), (sunset_hour, _) = self.get_sunrise_sunset()

        # Determine if it should be day or night
        # We check a simple hour range for now
        was_day = self.db.is_day
        is_now_day = sunrise_hour <= current_hour < sunset_hour
        self.db.is_day = is_now_day

        if was_day and not is_now_day:
            self.announce_sunset()
        elif not was_day and is_now_day:
            self.announce_sunrise()

        self.update_weather()

    def update_weather(self):
        """
        Updates the weather every WEATHER_UPDATE_RATE hours.
        """
        current_time = gametime.gametime()
        if current_time - self.db.last_weather_change >= WEATHER_UPDATE_RATE * 3600:
            self.db.last_weather_change = current_time

            season = self.get_season()
            new_weather = random.choice(WEATHER_PATTERNS[season])

            # Only announce if the weather is different
            if new_weather != self.db.current_weather:
                self.db.current_weather = new_weather
                message = f"|cThe weather changes: {new_weather}.|n"
                for room in self.find_outdoor_rooms():
                    room.msg_contents(message)

    def find_outdoor_rooms(self):
        """Helper to find all rooms tagged as 'outdoors'."""
        from evennia.objects.models import ObjectDB
        return ObjectDB.objects.filter(db_tags__db_key="outdoors")

    def announce_sunrise(self):
        """Announces the sunrise to all outdoor rooms."""
        message = "|yThe sun rises, casting long shadows across the land.|n"
        for room in self.find_outdoor_rooms():
            room.msg_contents(message)

    def announce_sunset(self):
        """Announces the sunset to all outdoor rooms."""
        message = "|yThe sun dips below the horizon, and the sky darkens.|n"
        for room in self.find_outdoor_rooms():
            room.msg_contents(message)
