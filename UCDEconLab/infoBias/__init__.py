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

selectionHistory = []

def filter_by_round():
    data = []
    selected_round = random.randint(1, C.NUM_ROUNDS)
    print(selected_round)
    for x in selectionHistory:
        if x['round'] == selected_round:
            data.append(x)
    return data

class Player(BasePlayer):
    sid = models.IntegerField(label="What is your student id?", min=0, max=999999999)
    searchBudget = models.FloatField(default=1.50)
    wallet = models.IntegerField(default=0)    
    numTasks = models.IntegerField(default=0)
    tuples = models.StringField()
    decision = models.StringField(
        # multiple choice selection (bubble in)
        widget = widgets.RadioSelect
    )
    choiceHistory = models.StringField(blank=True, default="[]") # store returned dictionary as JSON-encoded string


    def store_choice(self, choice_data):
        if self.choiceHistory:
            # Retrieve existing choices and convert to a list
            existing_choices = json.loads(self.choiceHistory)
        else:
            existing_choices = []
        
        # Append the new choice data to the existing choices list
        existing_choices.append(choice_data)
        
        # Store the updated choices as a JSON-encoded string
        self.choiceHistory = json.dumps(existing_choices)

    def get_choices(self):
        return json.loads(self.choiceHistory)

def decision_choices(player):
    # hard set first choice always current wallet choice
    choices = ['0 dollars, 0 tasks']
    # random generate 25 tuples of int, int for dollar and task amount
    for i in range(25):
        walletChoice = random.randint(0, 25)
        taskChoice = random.randint(0, 25)
        # convert to string format
        choice_str = f'{walletChoice} dollars, {taskChoice} tasks'
        # add to the choices array (array of strings)
        choices.append(choice_str)
    # shuffle order of everything excluding hard set first choice
    random.shuffle(choices[1:])
    #store choices list as a JSON-encoded string in choices attribute of player object
    player.choices = json.dumps(choices)
    return choices

# PAGES

class Instructions(Page):
    form_model = 'player'
    form_fields = ['sid']

    @staticmethod
    def is_displayed(player):
        return player.round_number <= C.NUM_ROUNDS

class ChoiceGame(Page):
    form_model = 'player'
    form_fields = ['decision']

    @staticmethod
    def is_displayed(player):
        return player.round_number <= C.NUM_ROUNDS

    # time out that auto submits page
    timeout_seconds = 15

    @staticmethod
    def live_method(player, data):
        print('New Selection!:', data)
        print('STORING!')
        selectionHistory.append(data)
        print(selectionHistory)

        # player.store_choice(data)
        # stored_data_list = player.get_choices()
        # print(stored_data_list)
        # random_entry = random.choice(stored_data_list)
        # Print the randomly selected entry
        # print("Randomly selected entry:", random_entry)



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        filtered_data = []
        filtered_data = filter_by_round()
        print(filtered_data)

    
    pass

class Tasks(Page):
    # display task page once game is over
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    
    # @staticmethod
    # def before_next_page(self):
    #     filter_by_round()
    #     print(filtered_data)

    pass

class Survey(Page):
    # display task page once game is over
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    pass


page_sequence = [Instructions, ChoiceGame, Results, Tasks, Survey]