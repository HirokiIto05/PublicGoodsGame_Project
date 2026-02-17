from otree.api import *
from .models import C, Subsession, Group, Player


class Introduction(Page):
    template_name = C.INTRODUCTION_TEMPLATE

    def is_displayed(self):
        return self.round_number == 1


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        # Endowment is set in set_contributions, but we show the intended endowment now
        asym = self.session.config.get('asymmetry', 0)
        
        # asym = self.session.asymmetry
        if asym == 0:
            endowment = C.ENDOWMENT_SYM
        else:
            if self.player.id_in_group in [1, 2]:
                endowment = C.ENDOWMENT_ADV
            else:
                endowment = C.ENDOWMENT_DISADV

        return dict(
            endowment=endowment,
            multiplier=C.MULTIPLIER,
            group_size=C.PLAYERS_PER_GROUP,
            punishment_system=self.group.punishment_system,
        )

    def error_message(self, values):
        # Need to check against correct endowment
        asym = self.session.config.get('asymmetry', 0)
        if asym == 0:
            endowment = C.ENDOWMENT_SYM
        else:
            if self.player.id_in_group in [1, 2]:
                endowment = C.ENDOWMENT_ADV
            else:
                endowment = C.ENDOWMENT_DISADV

        c = values.get('contribution', 0)
        if c < 0 or c > endowment:
            return f'Your contribution must be between 0 and {endowment}.'


class ContributeWaitPage(WaitPage):
    after_all_players_arrive = 'set_contributions'


class Punish(Page):
    form_model = 'player'

    def is_displayed(self):
        # peer (1) または democratic (2) で表示
        return self.group.punishment_system in [1, 2]

    def get_form_fields(self):
        # Punish only others; fields depend on id_in_group
        others = self.player.get_others_in_group()
        return [f'punish_p{o.id_in_group}' for o in others]

    def error_message(self, values):
        # Enforce max total budget 9 MU
        total = 0
        for o in self.player.get_others_in_group():
            total += values.get(f'punish_p{o.id_in_group}', 0) or 0
        if total > C.MAX_PUNISHMENT_BUDGET:
            return f'You can invest at most {C.MAX_PUNISHMENT_BUDGET} monetary units in punishment.'

    def vars_for_template(self):
        others = self.player.get_others_in_group()
        data = []
        for o in others:
            data.append(dict(
                id_in_group=o.id_in_group,
                contribution=o.contribution,
                endowment=o.endowment,
                relative_contribution=round(o.contribution / o.endowment, 2)
                if o.endowment else 0,
                field_name=f'punish_p{o.id_in_group}',
            ))
        return dict(
            others=data,
            own_contribution=self.player.contribution,
            own_endowment=self.player.endowment,
            max_budget=C.MAX_PUNISHMENT_BUDGET,
            cost_per_mu=C.PUNISHMENT_COST_PER_MU,
            fine_per_mu=C.PUNISHMENT_FINE_PER_MU,
        )


class PunishWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # For peer punishment: compute payoffs after proposals
        if self.group.punishment_system == 1:
            self.group.set_payoffs()

class DemocraticVote(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.group.punishment_system == 2

    def get_form_fields(self):
        # vote for each other member (execute punishment on them or not)
        others = self.player.get_others_in_group()
        return [f'vote_exec_p{o.id_in_group}' for o in others]

    def vars_for_template(self):
        players = self.group.get_players()
        rows = []
        for target in self.player.get_others_in_group():
            # total proposed points against target (sum of the 3 others' proposals)
            total_proposed = 0
            for proposer in target.get_others_in_group():
                field = f'punish_p{target.id_in_group}'
                total_proposed += getattr(proposer, field, 0) or 0

            rows.append(dict(
                id_in_group=target.id_in_group,
                contribution=target.contribution,
                endowment=target.endowment,
                relative_contribution=round(target.contribution / target.endowment, 2)
                if target.endowment else 0,
                total_proposed_points=total_proposed,
                implied_fine=total_proposed * C.PUNISHMENT_FINE_PER_MU,
                vote_field=f'vote_exec_p{target.id_in_group}',
                votes_needed=2,  # out of 3
            ))
        return dict(targets=rows)


class DemocraticVoteWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # For democratic punishment: compute payoffs after votes
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return dict(
            endowment=self.player.endowment,
            contribution=self.player.contribution,
            private_account=self.player.private_account,
            total_contribution=self.group.total_contribution,
            individual_return=self.group.individual_return,
            payoff_before_punishment=self.player.payoff_before_punishment,
            punishment_system=self.group.punishment_system,
            punishment_received=self.player.punishment_received,
            punishment_cost=self.player.punishment_cost,
            payoff=self.player.payoff,
            status=self.player.status
            # asymmetry=self.session.asymmetry
        )


page_sequence = [
    Contribute,
    ContributeWaitPage,
    Punish,                 # proposals (peer + democratic)
    PunishWaitPage,         # computes payoffs only if peer
    DemocraticVote,         # voting (democratic only)
    DemocraticVoteWaitPage, # computes payoffs for democratic
    Results,
]

