from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'infoBias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pid = models.IntegerField(label="What is your student id?", min=0, max=999999999)

    # initially playing around, new thought: what if this question acts as a control to eliminate "invalid data"
    controlQ = models.IntegerField(
        label='''
        Type "Sally sells seashells by the seashore"'''
    ) 

# PAGES

class Instructions(Page):
    form_model = 'player'
    form_fields = ['pid', 'controlQ']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, ResultsWaitPage, Results]
