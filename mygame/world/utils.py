# mygame/world/utils.py

def get_proficiency_rating(value):
    """
    Converts a numerical proficiency value (1-100) into a string rating.
    """
    if value <= 0:
        return "not learned"
    elif value <= 10:
        return "awful"
    elif value <= 20:
        return "poor"
    elif value <= 30:
        return "bad"
    elif value <= 40:
        return "average"
    elif value <= 50:
        return "fair"
    elif value <= 60:
        return "good"
    elif value <= 70:
        return "very good"
    elif value <= 80:
        return "excellent"
    elif value <= 90:
        return "superb"
    else:
        return "perfect"
