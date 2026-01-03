from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    amount_offered = models.IntegerField(initial=0)

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['amount_offered']


# class ResultsWaitPage(WaitPage):
#     pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'amount_offered': player.amount_offered
            # 'amount_kept': 100 - player.amount_offered,
        }

page_sequence = [MyPage, Results]
