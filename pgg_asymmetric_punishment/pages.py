from otree.api import *
from .models import C, Subsession, Group, Player


class Introduction(Page):
    template_name = 'pgg_asymmetric_punishment/Introduction.html'

    def is_displayed(self):
        # Show only once at the very beginning
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            punishment_system=self.group.punishment_system,
        )


class InstructionPeer(Page):
    template_name = 'pgg_asymmetric_punishment/Instruction_peer.html'

    def is_displayed(self):
        # Show at the start of the peer block (round 1)
        return self.round_number == 1


class InstructionDemocratic(Page):
    template_name = 'pgg_asymmetric_punishment/Instruction_democratic.html'

    def is_displayed(self):
        # Show when the democratic block starts (e.g., round 7)
        return self.round_number == C.SWITCH_AFTER_ROUNDS + 1
    
    

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    # def vars_for_template(self):
    #     return dict(
    #         endowment=self.player.endowment,
    #         multiplier=C.MULTIPLIER,
    #         group_size=C.PLAYERS_PER_GROUP,
    #         punishment_system=self.group.punishment_system,
    #     )
    
    def vars_for_template(self):
        return dict(
            endowment=int(self.player.endowment),   # ← ここ重要
            multiplier=float(C.MULTIPLIER),
            group_size=int(C.PLAYERS_PER_GROUP),
            punishment_system=self.group.punishment_system,
        )


    def error_message(self, values):
        endowment = self.player.endowment
        c = values.get('contribution', 0)
        if c < 0 or c > endowment:
            return f'Your contribution must be between 0 and {endowment}.'


class ContributeWaitPage(WaitPage):
    after_all_players_arrive = 'set_contributions'


class Punish(Page):
    form_model = 'player'

    def is_displayed(self):
        # Display for peer or democratic punishment systems
        return self.group.punishment_system in [1, 2]

    def get_form_fields(self):
        # Allow punishment only toward other group members
        others = self.player.get_others_in_group()
        return [f'punish_p{o.id_in_group}' for o in others]

    def error_message(self, values):
        # Enforce total punishment budget constraint
        total = 0
        for o in self.player.get_others_in_group():
            total += values.get(f'punish_p{o.id_in_group}', 0) or 0
        if total > C.MAX_PUNISHMENT_BUDGET:
            return f'You can invest at most {C.MAX_PUNISHMENT_BUDGET} monetary units in punishment.'

    def vars_for_template(self):
        # Retrieve information visibility mode (default = full)
        info_mode = self.session.config.get('punishment_info_mode', 'full')
        hide_others_endowment = (info_mode == 'incomplete')

        others = self.player.get_others_in_group()
        data = []

        for o in others:
            # If information mode is "incomplete", hide others' endowment
            shown_endowment = None if hide_others_endowment else o.endowment

            data.append(dict(
                id_in_group=o.id_in_group,
                contribution=o.contribution,
                endowment=shown_endowment,
                field_name=f'punish_p{o.id_in_group}',
            ))

        return dict(
            others=data,

            # Own information is always visible
            own_contribution=self.player.contribution,
            own_endowment=self.player.endowment,

            max_budget=C.MAX_PUNISHMENT_BUDGET,
            cost_per_mu=C.PUNISHMENT_COST_PER_MU,
            fine_per_mu=C.PUNISHMENT_FINE_PER_MU,

            punishment_info_mode=info_mode,
            hide_others_endowment=hide_others_endowment,
        )


class PunishWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # For peer punishment: compute payoffs after proposals
        if self.group.punishment_system == 1:
            self.group.set_payoffs()

class DemocraticVote(Page):
    form_model = 'player'

    def is_displayed(self):
        # Display only under democratic punishment system
        return self.group.punishment_system == 2

    def get_form_fields(self):
        # Vote on execution of punishment for each other member
        others = self.player.get_others_in_group()
        return [f'vote_exec_p{o.id_in_group}' for o in others]

    def vars_for_template(self):
        # Retrieve information visibility mode (default = full)
        info_mode = self.session.config.get('punishment_info_mode', 'full')
        hide_others_endowment = (info_mode == 'incomplete')

        rows = []

        for target in self.player.get_others_in_group():

            # Calculate total proposed punishment points against this target
            total_proposed = 0
            for proposer in target.get_others_in_group():
                field = f'punish_p{target.id_in_group}'
                total_proposed += getattr(proposer, field, 0) or 0

            # Hide endowment if information mode requires it
            shown_endowment = None if hide_others_endowment else target.endowment

            rows.append(dict(
                id_in_group=target.id_in_group,
                contribution=target.contribution,
                endowment=shown_endowment,
                total_proposed_points=total_proposed,
                implied_fine=total_proposed * C.PUNISHMENT_FINE_PER_MU,
                vote_field=f'vote_exec_p{target.id_in_group}',
                votes_needed=2,  # Majority among 3 voters
            ))

        return dict(
            targets=rows,
            punishment_info_mode=info_mode,
            hide_others_endowment=hide_others_endowment,
        )
    
    def error_message(self, values):
        # Check if any vote field is missing
        for field in self.get_form_fields():
            if values.get(field) is None:
                return "Please select an option for all players."


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

class Demographics(Page):
    form_model = "player"
    form_fields = ["age", "gender", "nationality"]

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict()
    
class End(Page):
    def is_displayed(self):
        # Display only in the final round
        return self.round_number == C.NUM_ROUNDS


page_sequence = [
    Introduction,          # General instructions (shown at the beginning)
    InstructionPeer,       # Shown at the start of the peer punishment block
    InstructionDemocratic, # Shown at the start of the democratic punishment block
    # Demographics,
    Contribute,
    ContributeWaitPage,
    Punish,                 # proposals (peer + democratic)
    PunishWaitPage,         # computes payoffs only if peer
    DemocraticVote,         # voting (democratic only)
    DemocraticVoteWaitPage, # computes payoffs for democratic
    Results,
    End,
]
