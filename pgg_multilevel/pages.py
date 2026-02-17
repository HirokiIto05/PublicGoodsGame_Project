from otree.api import *
from .models import *

class Introduction(Page):
    template_name = C.INTRODUCTION_TEMPLATE

    def is_displayed(self):
        return self.player.round_number == 1

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribute_local', 'contribute_global']

    def error_message(self, values):
        total = values.get('contribute_local', 0) + values.get('contribute_global', 0)
        if total > C.ENDOWMENT:
            return 'The sum of your local and global contributions cannot exceed your endowment.'

    def vars_for_template(self):
        return dict(
            mpcr_local=self.group.mpcr_local,
            mpcr_global=self.group.mpcr_global,
            local_size=C.LOCAL_SIZE,
            global_size=C.GLOBAL_SIZE,
        )

class ContributeWaitPage(WaitPage):
    after_all_players_arrive = 'set_contributions'


class Punish(Page):
    form_model = 'player'
    
    def get_form_fields(self):
        """Dynamically generate punishment fields for other players only"""
        return [f'punish_p{p.id_in_group}' 
                for p in self.player.get_others_in_group()]
    
    def vars_for_template(self):
        """Show contributions of all group members"""
        other_players = self.player.get_others_in_group()
        players_data = []
        
        for p in other_players:
            players_data.append({
                'id_in_group': p.id_in_group,
                'contribute_local': p.contribute_local,
                'contribute_global': p.contribute_global,
                'total_contribution': p.contribute_local + p.contribute_global,
                'field_name': f'punish_p{p.id_in_group}',
            })
        
        return dict(
            players_data=players_data,
            own_contribution_local=self.player.contribute_local,
            own_contribution_global=self.player.contribute_global,
            own_total_contribution=self.player.contribute_local + self.player.contribute_global,
            max_punishment=C.MAX_PUNISHMENT_POINTS,
        )



class PunishWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs_after_punishment'

class Results(Page):
    def vars_for_template(self):
        return dict(
            contribute_local=self.player.contribute_local,
            contribute_global=self.player.contribute_global,
            contribute_private=self.player.contribute_private,
            local_return=self.group.individual_local_return,
            global_return=self.group.individual_global_return,
            payoff_before_punishment=self.player.payoff_before_punishment,
            punishment_received=self.player.punishment_received,
            punishment_cost=self.player.punishment_cost,
            payoff=self.player.payoff,
        )

page_sequence = [Contribute, ContributeWaitPage, Punish, PunishWaitPage, Results]
