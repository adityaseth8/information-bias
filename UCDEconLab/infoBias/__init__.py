from otree.api import *
import random
import json


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'infoBias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    TIMEOUT_SECONDS = 120
    SEARCH_COST = 0.10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sid = models.IntegerField(label="What is your student id?", min=0, max=999999999)
    searchBudget = models.FloatField(default=1.50)
    wallet = models.IntegerField(default=0)    
    numTasks = models.IntegerField(default=0)
    tuples = models.StringField()
    # num_rounds = models.IntegerField(initial=0)
    
    # decision = models

# hook method called during the session creating process.
# Set up initial state of the game (list of choices) for each subsession
def creating_session(subsession):
    if subsession.get_players():
        tuples = []
        for i in range(25):
            walletChoice = random.randint(0,25)
            taskChoice = random.randint(0,25)
            tuples.append((walletChoice, taskChoice))

         # Serialize tuples as a JSON string and store it in Player model
        for player in subsession.get_players():
            player.tuples = json.dumps(tuples)

# PAGES

class Instructions(Page):
    form_model = 'player'
    form_fields = ['sid']

    @staticmethod
    def is_displayed(player):
        return player.round_number <= C.NUM_ROUNDS

class ChoiceGame(Page):
    form_model = 'player'
    # form_fields = ['decision']

    @staticmethod
    def is_displayed(player):
        return player.round_number <= C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        playerTuples = json.loads(player.tuples)
        return {'tuples': playerTuples}
    
    # def get_timeout_seconds(self):
    #     return C.TIMEOUT_SECONDS

    # time out that auto submits page
    timeout_seconds = 60
    
    # def before_next_page(self, timeout_happened=False):
    #     if self.request.POST.get('reveal-tuples'):
    #         self.player.searchBudget -= 0.10
    #         self.player.save()


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass

class Tasks(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    pass

page_sequence = [Instructions, ChoiceGame, Results, Tasks]