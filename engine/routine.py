from mood import Mood


# add functions/variables to customize routines

class DefaultRoutine:
    '''
    Class for default routine, custom routines built upon this
    '''

    def __init__(self, bedtime):
        self.bedtime = bedtime


class Routine():
    def __init__(self, mood: Mood, default: DefaultRoutine):
        self.mood = mood
        self.default = default

    def __str__(self):
        return f"< Routine: {self.mood.label} >"
    
    def __repr__(self):
        return f"< Routine: {self.mood.label} >"