from otree.api import *
import random
import ast
import numpy as np
import string

doc = """
Your app description
"""


class Constants(BaseConstants):
    num_rounds = 50
    name_in_url = 'generate_validate'
    players_per_group = None
    dimension = 5  # dimension of the zero-one matrix (dimension x dimension = length)
    length = dimension * dimension
    proportion = 0.5  # proportion of zeros in the matrix


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_vector = models.StringField()
    completion_code = models.StringField(initial=''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(9)))


def creating_session(subsession):
    for player in subsession.get_players():
        aux = np.random.rand(1, Constants.length)  # get random numbers between zero and 1
        zero_one = aux > (1 - Constants.proportion)  # transform to vector of booleans
        integer_vector = 1 * zero_one  # transform to vector of integers
        flat_vector = integer_vector.flatten().tolist()  # converts ndarray to flat list

        # method to indicate column breaks
        broken_vector = []
        for index in range(0, Constants.length):
            broken_vector.append(flat_vector[index])
            if index % Constants.dimension == Constants.dimension - 1:
                broken_vector.append(-1)

        string_vector = [str(int) for int in broken_vector]  # transform to vector of strings
        player.task_vector = ", ".join(string_vector)  # join into one string

        # method to generate random string (completion code)


# PAGES
class Tasks(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number <= player.participant.selectedNumTasks
        
    @staticmethod
    def vars_for_template(player: Player):
        task_vector = ast.literal_eval(player.task_vector)
        return {
            "task_vector": task_vector,
        }


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == player.participant.selectedNumTasks


page_sequence = [Tasks, Results]