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
    # form_fields = ['decision']

    # def gameProcessing(player: Player):
    #     # if player stuck with current choice
    #     if player.decision == True:
    #         player.roundsPlayed += 1
    #         # store player's wallet and task value somewhere
    #         # generate new alteranative choice and task, display it on the ChoiceGame page
    #         player.genChoice()

    #         if player.roundsPlayed == C.NUM_ROUNDS:
    #             # terminate game by going to the results page
    #             return player.redirect('Results')
            
    #     # Pick alternative Choice
    #     elif player.decision == False:
    #         player.roundsPlayed += 1
    #         #store altChoice and altTask variable values as wallet and task
    #         player.wallet = player.altChoice
    #         player.task = player.altTask
    #         if player.roundsPlayed == C.NUM_ROUNDS:
    #             # terminate game by going to the results page
    #             return player.redirect('Results')

    # def before_next_page(self):
    #     if self.player.decision is not None:
    #         self.gameProcessing(self.player)
    #         print("works4")
        # Define the timeout function
        # @staticmethod
        # def timeout_player(player: Player):
        #     player.genChoice()
        #     player.participant.vars['choice'] = player.currChoice



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, ChoiceGame, Results]
