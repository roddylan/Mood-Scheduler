from .mood import Mood
from . import engine_utils as engine_utils
from . import constants
from langchain.prompts import PromptTemplate
import numpy as np


# add functions/variables to customize routines

class DefaultRoutine:
    '''
    Class for default routine, custom routines built upon this
    '''
    # TODO: add meal_plan
    def __init__(self, bedtime: engine_utils.Time, spotify, schedule: engine_utils.Schedule, bus_schedule):
        self._bedtime = bedtime
        self._playlists = spotify
        self._schedule = schedule
        self.bus_schedule = bus_schedule
        # self.meal_plan = meal_plan

    def get_bedtime(self):
        return self._bedtime
    
    def get_playlists(self):
        return self._playlists
    
    def get_schedules(self):
        return self._schedule

# TODO: IMPROVE SEPARATION, SEPARATE ROUTINE INSTANCES 
class Routine:
    def __init__(self, mood: Mood, default: DefaultRoutine):
        self.mood = mood
        self.default = default

    def get_playlist(self):
        playlists = self.default.get_playlists()[self.mood.get_label()]
        idx = np.random.randint(0, len(playlists))
        return playlists[idx]

    def send_text(self, sched=None):
        # gm_template = PromptTemplate()
        prompt = f"I just woke up and feel {self.mood.get_awake()} and {self.mood.get_emotion()}, write me a short, 45 word long, encouraging message."
        llm = constants.llm
        gm_text = llm(prompt)
        playlist = self.get_playlist()
        engine_utils.send_text(text=gm_text, playlist=playlist, sched=sched, bedtime=self.get_bedtime())

    # def set_bedtime(self, offset: engine_utils.Time):
    #     if self.mood.is_awake():
    #         # return self.default.bedtime + utils.Time(1, 30)
    #         return self.default.get_bedtime()
    #     else:
    #         return self.default.get_bedtime() - offset
    
    def get_bedtime(self):
        if self.mood.is_awake():
            # return self.default.bedtime + utils.Time(1, 30)
            return self.default.get_bedtime()
        else:
            return self.default.get_bedtime() - engine_utils.Time(1, 30)

    def run(self):
        scheds = self.default.get_schedules()
        sched = scheds.get_schedule(self.mood)
        # TODO: google calendar/tasks interaction
        # TODO: clock interaction

        self.send_text(sched)

    def __str__(self):
        return f"< Routine: {self.mood.label} >"
    
    def __repr__(self):
        return f"< Routine: {self.mood.label} >"