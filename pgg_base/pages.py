from otree.api import *
from .models import *


class Introduction(Page):
    template_name = C.INTRODUCTION_TEMPLATE

    def is_displayed(self):
        return self.player.round_number == 1

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass


page_sequence = [Introduction, Contribute, ResultsWaitPage, Results]