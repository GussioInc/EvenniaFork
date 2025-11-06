from evennia import DefaultScript
import random

# Define the different weather patterns
WEATHER_PATTERNS = {
    "clear": {
        "desc": "The sky is clear and the sun is shining brightly.",
        "transitions": {"clear": 0.7, "cloudy": 0.3},
    },
    "cloudy": {
        "desc": "The sky is overcast with grey clouds.",
        "transitions": {"clear": 0.4, "rainy": 0.6},
    },
    "rainy": {
        "desc": "A steady, cool rain falls from the sky.",
        "transitions": {"cloudy": 0.8, "stormy": 0.2},
    },
    "stormy": {
        "desc": "Thunder rumbles in the distance as lightning flashes.",
        "transitions": {"rainy": 1.0},
    },
}

class WeatherScript(DefaultScript):
    """
    This script manages the global weather.
    """
    def at_script_creation(self):
        """Called when the script is first created."""
        self.key = "weather_script"
        self.desc = "Manages the weather."
        self.interval = 60 * 10  # Change weather every 10 minutes
        self.persistent = True
        self.db.current_weather = "clear"

    def at_repeat(self):
        """Called every self.interval seconds."""
        current_state_key = self.db.current_weather
        current_state = WEATHER_PATTERNS.get(current_state_key, WEATHER_PATTERNS["clear"])

        # Get possible next states and their probabilities
        transitions = current_state["transitions"]
        new_state = random.choices(list(transitions.keys()), list(transitions.values()))[0]

        self.db.current_weather = new_state
        # Announce the change to all outdoor rooms (optional)
        # self.announce_weather_change()

    def get_weather_desc(self):
        """Returns the description for the current weather."""
        return WEATHER_PATTERNS[self.db.current_weather]["desc"]
