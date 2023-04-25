from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'infoBias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20 #random.randint(1,5)
    TIMEOUT_SECONDS = 120


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sid = models.IntegerField(label="What is your student id?", min=0, max=999999999)

    # initially playing around, new thought: what if this question acts as a control to eliminate "invalid data"
    controlQ = models.StringField(
        label='''
        Type "Sally sells seashells by the seashore"'''
    ) 

    wallet = models.IntegerField(default=0)    
    task = models.StringField(default=0)
    altChoice = models.IntegerField(default=random.randint(0,20))
    altTask = models.StringField(default=random.choice(['matrix', 'typing']))

    def genChoice(player):
        player.altChoice = random.randint(0,20)
        player.altTask = random.choice(['matrix', 'typing'])



# PAGES

class Instructions(Page):
    form_model = 'player'
    form_fields = ['sid', 'controlQ']

class ChoiceGame(Page):
        form_model = 'player'
        
        # Define the timeout function
        # @staticmethod
        # def timeout_player(player: Player):
        #     player.genChoice()
        #     player.participant.vars['choice'] = player.currChoice



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, ChoiceGame, ResultsWaitPage, Results]
