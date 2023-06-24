from otree.api import *
import random
import json
import numpy as np
import string
import ast


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'infoBias'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    TIMEOUT_SECONDS = 120
    SEARCH_COST = 0.10

    dimension = 5  # dimension of the zero-one matrix (dimension x dimension = length)
    length = dimension * dimension
    proportion = 0.5  # proportion of zeros in the matrix


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

# in the future, remove global variables
selectionHistory = []
selectedChoice = []
# numTasks = 0

def selectChoice(player):
    selected_round = random.randint(1, C.NUM_ROUNDS)
    filtered_data = filter_by_round(selected_round)
    selectedChoice = filter_by_time(filtered_data, selected_round)
    print("selected choice")
    print(selectedChoice)
    choice_parts = selectedChoice['choice'].split(',')
    player.selectedMoney = int(choice_parts[0].strip().split()[0])
    player.selectedNumTasks = int(choice_parts[1].strip().split()[0])
    player.session.vars['selectedNumTasks'] = player.selectedNumTasks
    player.participant.selectedNumTasks  = player.selectedNumTasks
    # numTasks = player.selectedNumTasks
    # print(numTasks)

def filter_by_round(selected_round):
    data = []
    for x in selectionHistory:
        if x['round'] == selected_round:
            data.append(x)
    return data

def filter_by_time(filtered_data, selected_round):
    # Generate a random timestamp between 0:59 and 0:00
    seconds = random.randint(0, 5)
    rand_time = "0:" + str(seconds).zfill(2)

    chosen_choice = None
    # Iterate through the list and find the choice at the given timestamp
    for item_index, item in enumerate(filtered_data):
        item_time = item['time']
        # print(item_time)
        # print(item)
        if (rand_time > filtered_data[item_index]['time']):
            selected_row = {'round': selected_round, 'time': '1:00', 'choice': '0 dollars, 0 tasks'}
            break
        if item_index + 1 < len(filtered_data):
            next_item_time = filtered_data[item_index + 1]['time']
            if rand_time >= next_item_time and item_time >= rand_time:
                selected_row = item
                break
            else:
                continue
        else:
            selected_row = item
    return selected_row

class Player(BasePlayer):
    sid = models.IntegerField(label="What is your student id?", min=0, max=999999999)
    searchBudget = models.FloatField(default=4.00)
    wallet = models.IntegerField(default=0)
    numTasks = models.IntegerField(default=0)
    tuples = models.StringField()
    decision = models.StringField(
        # multiple choice selection (bubble in)
        widget = widgets.RadioSelect
    )
    choiceHistory = models.StringField(blank=True, default="[]") # store returned dictionary as JSON-encoded string
    selectedMoney = models.IntegerField()
    selectedNumTasks = models.IntegerField()

    task_vector = models.StringField()
    completion_code = models.StringField(initial=''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(9)))


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
    for i in range(40):
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

class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    
    form_model = 'player'
    form_fields = ['sid']
    pass

class Instructions(Page):
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
    timeout_seconds = 5

    @staticmethod
    def live_method(player, data):
        print('New Selection!:', data)
        print('STORING!')
        selectionHistory.append(data)
        print(selectionHistory)

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:
            selectChoice(player)

            
class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
       
    pass

page_sequence = [Intro, Instructions, ChoiceGame, Results]