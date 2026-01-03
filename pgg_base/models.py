from tokenize import group
from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg_base'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    MULTIPLIER = 0.5
    ENDOWMENT = 100
    INTRODUCTION_TEMPLATE = 'pgg_base/Introduction.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum(p.contribution for p in self.get_players())
        self.individual_share = (self.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP
        for p in self.get_players():
            p.payoff = C.ENDOWMENT - p.contribution + self.individual_share

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="How much will you contribute?"
    )

