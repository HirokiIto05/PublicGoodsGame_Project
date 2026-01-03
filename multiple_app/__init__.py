from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'multiple_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    PAYMENT_AMOUNT = cu(1)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_entered = models.IntegerField()
    sum_of_numbers = models.IntegerField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['number_entered']
    @staticmethod
    def vars_for_template(player):
        number_1 = random.randint(1, 100)
        number_2 = random.randint(1, 100)
        player.sum_of_numbers = number_1 + number_2
        return {
            'number_1': number_1,
            'number_2': number_2,
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.sum_of_numbers == player.number_entered:
            player.payoff = C.PAYMENT_AMOUNT
    


class Results(Page):
    pass

class Combined_Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        combined_payoff = 0
        for p in all_players:
            combined_payoff += p.payoff
        return {
            "combined_payoff": combined_payoff
        }


page_sequence = [MyPage, Results, Combined_Results]