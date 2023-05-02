from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'infoBias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20 #random.randint(1,5)
    # TIMEOUT_SECONDS = 120


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sid = models.IntegerField(
        label="What is your student id?", min=0, max=999999999
    )

    decision = models.BooleanField(
        label="Please choose if you want to keep your current choice, pick the alternative choice, or pay 10 cents to generate a new option",
        choices=[        
            [True, "Keep Current Choice and generate new choice"],
            [False, "Pick alternative Choice"],
        ]
    )
    
    roundsPlayed = models.IntegerField(initial=0)

    wallet = models.IntegerField(default=0)    
    task = models.StringField(default="")
    altChoice = models.IntegerField(default=random.randint(0,20))
    altTask = models.StringField(default=random.choice(['matrix', 'typing']))

    def genChoice(player):
        player.altChoice = random.randint(0,20)
        player.altTask = random.choice(['matrix', 'typing'])



# PAGES

class Instructions(Page):
    form_model = 'player'
    form_fields = ['sid']

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
    # wait_for_all_groups = True

    # def after_all_players_arrive(self):
    #     # Define logic for transitioning back to the gameplay page
    #     # e.g. to transition to the next round, use:
    #     self.group.next_round()
        
    #     #store player's choice
    #     self.player.participant.vars['wallet'] = self.player.wallet
    #     self.player.participant.vars['task'] = self.player.task
        
    #     # to transition to a specific page
    #     return self.player.redirect_to_page('ChoiceGame')
class Results(Page):
    pass


page_sequence = [Instructions, ChoiceGame]
