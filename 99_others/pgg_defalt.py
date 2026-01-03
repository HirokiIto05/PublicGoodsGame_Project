from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg'
    # for testing up to 3 people can fit into split screen mode which is highly useful because otherwise would have to juggle multiple tabs
    PLAYERS_PER_GROUP = 3
    # since we made the end of the experiment dynamic we have to put a large number for rounds that participants can never ever reach
    # it is a huge mess if they reach that so it has to be avoided, but dont but too large a number either because that can stress the database
    NUM_ROUNDS = 20
    BUDGET = 10
    # contributions get multiplied by this
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # we use group variables as they are relevant for and only have a single value for the whole group
    sum_contributions = models.IntegerField(initial=0)
    end = models.BooleanField()


class Player(BasePlayer):
    # players can contribute each different amounts so its a player variable
    contribution = models.IntegerField(label='Contribution', min=0, max=C.BUDGET)


# PAGES
class Instructions(Page):
    pass

    @staticmethod
    def is_displayed(player):
        # only show the instructions in the first round
        return player.round_number == 1

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == 1:
            # demonstration for how we can put data into participant variables that are defined in the settings.py
            player.participant.whatever = player.contribution

class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        # loop through all the players in the group and sum up their contributions
        for p in group.get_players():
            group.sum_contributions += p.contribution

        # loop through the players again and calculate their payoffs
        # what they kept + share of the public funds
        for p in group.get_players():
            p.payoff = C.BUDGET - p.contribution + (group.sum_contributions*C.MULTIPLIER)/C.PLAYERS_PER_GROUP

        # dynamically determine the end of the experiment
        # after 5 rounds it has 50% chance to end
        if group.round_number > 5:
            group.end = random.choice([True, False])
        else:
            group.end = False

class Results(Page):
    pass

class FinalResults(Page):
    pass

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [Instructions, Contribute, ResultsWaitPage, Results]
