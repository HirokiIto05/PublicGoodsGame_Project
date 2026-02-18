from otree.api import *
import random

doc = """
Public goods game with asymmetric vs symmetric endowments,
and different punishment systems (peer vs central; easily extendable).
Based on Nockur, Pfattheicher & Keller (2021, JESP).
"""


class C(BaseConstants):
    NAME_IN_URL = 'pgg_diff_punishment'
    PLAYERS_PER_GROUP = 4

    # In the original paper: 24 periods, 6 per punishment system.
    NUM_ROUNDS = 3
    # Here we keep it small for testing; adjust in session config.

    # Endowment profiles (by id_in_group order 1..4)
    ENDOWMENT_PROFILES = {
        'sym_30': [30, 30, 30, 30],
        'asym_40_40_20_20': [40, 40, 20, 20],
        'asym_80_40_20_20': [80, 40, 20, 20],
    }

    # MPCR of the public good: contributions * 1.6 / 4
    MULTIPLIER = 1.6

    # Punishment systems:
    # 0 = no punishment
    # 1 = peer punishment (costly, 1 MU cost -> 2 MU fine)
    # 2 = democratic punishment (not coded here)
    PUNISHMENT_SYSTEMS = [0, 1, 2]

    # Max MUs that can be invested in punishment in total (per punisher)
    MAX_PUNISHMENT_BUDGET = 9

    # Cost-to-fine ratio 1:2 (Fehr & Gächter; paper uses same ratio)
    PUNISHMENT_COST_PER_MU = 1
    PUNISHMENT_FINE_PER_MU = 2

    INTRODUCTION_TEMPLATE = 'pgg_diff_punishment/Introduction.html'


class Subsession(BaseSubsession):

    def creating_session(self):
        # punishment system from config
        ps = self.session.config.get('punishment_system', 1)
        for g in self.get_groups():
            g.punishment_system = ps

        # --- NEW: fixed endowment assignment ---
        # Choose which profile to use (default: old asym 40-40-20-20 style)
        profile_key = self.session.config.get('endowment_profile', 'asym_40_40_20_20')
        profile = C.ENDOWMENT_PROFILES.get(profile_key)
        if profile is None:
            raise ValueError(f"Unknown endowment_profile: {profile_key}")

        # Assign once in round 1, store in participant.vars, reuse in later rounds
        for p in self.get_players():
            if self.round_number == 1:
                e = profile[p.id_in_group - 1]
                p.participant.vars['fixed_endowment'] = e

                # optional: store a status label too (useful for analysis)
                if profile_key.startswith('sym'):
                    p.participant.vars['status'] = 'symmetric'
                else:
                    # you can customize labels; here’s a simple one:
                    if profile_key == 'asym_40_40_20_20':
                        p.participant.vars['status'] = 'advantaged' if p.id_in_group in [1, 2] else 'disadvantaged'
                    elif profile_key == 'asym_80_40_20_20':
                        # three-tier labels
                        if p.id_in_group == 1:
                            p.participant.vars['status'] = 'top'
                        elif p.id_in_group == 2:
                            p.participant.vars['status'] = 'middle'
                        else:
                            p.participant.vars['status'] = 'bottom'

            # every round: copy fixed values into Player fields
            p.endowment = p.participant.vars['fixed_endowment']
            p.status = p.participant.vars.get('status', '')



class Group(BaseGroup):
    punishment_system = models.IntegerField()

    # total group contribution and individual return from public good
    total_contribution = models.CurrencyField()
    individual_return = models.CurrencyField()

    def set_contributions(self):
        players = self.get_players()
    
        # DO NOT set endowment here anymore.
        # It's already fixed per participant in Subsession.creating_session()
    
        self.total_contribution = sum(p.contribution for p in players)
        self.individual_return = self.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    
        for p in players:
            p.private_account = p.endowment - p.contribution
            p.payoff_before_punishment = p.private_account + self.individual_return


    def apply_peer_punishment(self):
        """Costly peer punishment: 1 MU cost -> 2 MU fine, max 9 MU invested."""
        players = self.get_players()

        # First compute punishment cost for each punisher, and total punishment received.
        for p in players:
            others = p.get_others_in_group()
            used_budget = 0
            cost = 0
            for other_i in others:
                field = f'punish_p{other_i.id_in_group}'
                points = getattr(p, field, 0) or 0
                used_budget += points
                # Enforce budget cap at server side
                points = min(points, C.MAX_PUNISHMENT_BUDGET - used_budget)
                setattr(p, field, points)
                cost += points * C.PUNISHMENT_COST_PER_MU
            p.punishment_cost = cost

        # Now sum punishment received and apply fines
        for p in players:
            others = p.get_others_in_group()
            total_received = 0
            for other_i in others:
                field = f'punish_p{p.id_in_group}'
                total_received += getattr(other_i, field, 0) or 0
            p.punishment_received = total_received
            fine = total_received * C.PUNISHMENT_FINE_PER_MU
            p.payoff = p.payoff_before_punishment - fine - p.punishment_cost

    def apply_democratic_punishment(self):
        """
        Democratic punishment (per Nockur et al., 2021):
        1) Each player proposes punishment points for others (same as peer).
        2) For each target player T, the other 3 players vote whether to execute
            the *suggested* (summed) punishment on T.
        3) If at least 2 of 3 vote YES, punishment is executed:
                - T receives fine = (sum proposed points) * 2
                - proposers pay costs = (their proposed points) * 1
            If <2 vote YES, no punishment is executed on T and no one pays costs for T.
        """
        players = self.get_players()
    
        # Ensure clean initialization each round
        for p in players:
            p.punishment_cost = 0
            p.punishment_received = 0
            p.payoff = p.payoff_before_punishment
    
        # Server-side enforce proposal budget (same style as peer)
        for proposer in players:
            others = proposer.get_others_in_group()
            used_budget = 0
            for other_i in others:
                field = f'punish_p{other_i.id_in_group}'
                points = getattr(proposer, field, 0) or 0
    
                # cap remaining budget
                remaining = C.MAX_PUNISHMENT_BUDGET - used_budget
                points = max(0, min(points, remaining))
    
                setattr(proposer, field, points)
                used_budget += points
    
        # For each target, check votes and execute if majority approves
        for target in players:
            voters = [p for p in players if p.id_in_group != target.id_in_group]
    
            # how many voted to execute punishment on this target?
            yes_votes = 0
            for v in voters:
                vote_field = f'vote_exec_p{target.id_in_group}'
                if (getattr(v, vote_field, 0) or 0) == 1:
                    yes_votes += 1
    
            # majority rule among the 3 others: at least 2 yes votes
            execute = yes_votes >= 2
    
            if not execute:
                continue
    
            # total proposed points against target by the 3 others
            total_points = 0
            for proposer in voters:
                prop_field = f'punish_p{target.id_in_group}'
                total_points += getattr(proposer, prop_field, 0) or 0
    
            fine = total_points * C.PUNISHMENT_FINE_PER_MU
            target.punishment_received = total_points
            target.payoff -= fine
    
            # proposers bear costs for the points they proposed (only if executed)
            for proposer in voters:
                prop_field = f'punish_p{target.id_in_group}'
                pts = getattr(proposer, prop_field, 0) or 0
                proposer.punishment_cost += pts * C.PUNISHMENT_COST_PER_MU
    
        # subtract punishment costs from proposers
        for p in players:
            p.payoff -= p.punishment_cost

    def set_payoffs(self):
        if self.punishment_system == 0:
            # no punishment
            for p in self.get_players():
                p.punishment_cost = 0
                p.punishment_received = 0
                p.payoff = p.payoff_before_punishment
        elif self.punishment_system == 1:
            self.apply_peer_punishment()
        elif self.punishment_system == 2:
            self.apply_democratic_punishment()
        else:
            # Placeholder for democratic punishment or other systems
            for p in self.get_players():
                p.punishment_cost = 0
                p.punishment_received = 0
                p.payoff = p.payoff_before_punishment


class Player(BasePlayer):

    endowment = models.CurrencyField()
    status = models.StringField()  # 'advantaged' / 'disadvantaged' (asymmetric only)

    # Contribution
    contribution = models.CurrencyField(min=0)

    private_account = models.CurrencyField()

    payoff_before_punishment = models.CurrencyField()
    punishment_received = models.CurrencyField(initial=0)
    punishment_cost = models.CurrencyField(initial=0)


    # Peer punishment fields (for 4 players)
    punish_p1 = models.IntegerField(min=0, max=C.MAX_PUNISHMENT_BUDGET, initial=0)
    punish_p2 = models.IntegerField(min=0, max=C.MAX_PUNISHMENT_BUDGET, initial=0)
    punish_p3 = models.IntegerField(min=0, max=C.MAX_PUNISHMENT_BUDGET, initial=0)
    punish_p4 = models.IntegerField(min=0, max=C.MAX_PUNISHMENT_BUDGET, initial=0)
    
    # Democratic punishment voting (vote whether to execute punishment on each target)
    vote_exec_p1 = models.IntegerField(choices=[[0, 'No'], [1, 'Yes']], widget=widgets.RadioSelect())
    vote_exec_p2 = models.IntegerField(choices=[[0, 'No'], [1, 'Yes']], widget=widgets.RadioSelect())
    vote_exec_p3 = models.IntegerField(choices=[[0, 'No'], [1, 'Yes']], widget=widgets.RadioSelect())
    vote_exec_p4 = models.IntegerField(choices=[[0, 'No'], [1, 'Yes']], widget=widgets.RadioSelect())


    def available_punishment_budget(self):
        """Helper: total budget used (for form-side checks if desired)."""
        total = 0
        for i in range(1, C.PLAYERS_PER_GROUP + 1):
            if i == self.id_in_group:
                continue
            total += getattr(self, f'punish_p{i}', 0) or 0
        return total