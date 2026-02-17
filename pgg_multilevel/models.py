from otree.api import *
import random

doc = """
Public Goods Game with Multilevel structure and Punishment (Fehr & Gächter style)
"""

class C(BaseConstants):
    NAME_IN_URL = 'pgg_multilevel'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    MULTIPLIER_LOCAL = 0.7
    MULTIPLIER_GLOBAL_TREATMENTS = {
        0: 0.0,
        1: 0.2,
        2: 0.35}

    ENDOWMENT = 100

    LOCAL_SIZE = 2
    GLOBAL_SIZE = 4

    INTRODUCTION_TEMPLATE = 'pgg_base/Introduction.html'
    
    # Punishment parameters (following Fehr & Gächter)
    PUNISHMENT_EFFECTIVENESS = 0.1  # Each punishment point reduces payoff by 10%
    MAX_PUNISHMENT_POINTS = 10
    PUNISHMENT_COST = {
        0: 0, 1: 1, 2: 2, 3: 4, 4: 6, 
        5: 9, 6: 12, 7: 16, 8: 20, 9: 25, 10: 30
    }

class Subsession(BaseSubsession):

    def creating_session(self):
        treatment = self.session.config.get('treatment', 1)

        players = self.get_players()
        random.shuffle(players)
        global_groups = [players[i:i + C.GLOBAL_SIZE]
        for i in range(0, len(players), C.GLOBAL_SIZE)]

        for global_id, g_players in enumerate(global_groups, start=1):
            for local_id, p in enumerate(g_players, start=1):
                p.global_group_id = global_id
                p.local_group_id = 1 if local_id <= 2 else 2
        
        self.set_group_matrix([
            [p.id_in_subsession for p in g_players if p.local_group_id == 1] +
            [p.id_in_subsession for p in g_players if p.local_group_id == 2]
            for g_players in global_groups
        ])

        for g in self.get_groups():
            g.treatment = treatment
            g.mpcr_local = C.MULTIPLIER_LOCAL
            g.mpcr_global = C.MULTIPLIER_GLOBAL_TREATMENTS[treatment]

class Group(BaseGroup):
    treatment = models.IntegerField()
    mpcr_local = models.FloatField()
    mpcr_global = models.FloatField()

    total_local = models.CurrencyField()
    total_global = models.CurrencyField()
    individual_local_return = models.CurrencyField()
    individual_global_return = models.CurrencyField()

    def set_contributions(self):
        self.total_local = sum(p.contribute_local for p in self.get_players())

        all_players = self.subsession.get_players()
        same_global = [p for p in all_players
                       if p.global_group_id == self.get_players()[0].global_group_id]

        self.total_global = sum(p.contribute_global for p in same_global)

        self.individual_local_return = (
            self.total_local * self.mpcr_local / C.LOCAL_SIZE
        )
        self.individual_global_return = (
            self.total_global * self.mpcr_global / C.GLOBAL_SIZE)

        for p in self.get_players():
            p.set_private()
            p.payoff_before_punishment = (
                p.contribute_private +
                self.individual_local_return +
                self.individual_global_return
            )
    
    def set_payoffs_after_punishment(self):
        """Calculate final payoffs after punishment stage"""
        for p in self.get_players():
            # Calculate total punishment points received
            other_players = p.get_others_in_group()
            total_punishment_received = sum([
                getattr(other, f'punish_p{p.id_in_group}', 0) 
                for other in other_players
            ])
            
            # Cap punishment at 10 points (following Fehr & Gächter)
            effective_punishment = min(total_punishment_received, C.MAX_PUNISHMENT_POINTS)
            p.punishment_received = effective_punishment
            
            # Calculate punishment cost (cost of punishing others)
            punishment_cost = 0
            for other in other_players:
                points_given = getattr(p, f'punish_p{other.id_in_group}', 0)
                punishment_cost += C.PUNISHMENT_COST.get(points_given, 0)
            
            p.punishment_cost = punishment_cost
            
            # Final payoff = initial payoff * (1 - 0.1 * punishment_received) - punishment_cost
            payoff_after_receiving = p.payoff_before_punishment * (
                1 - C.PUNISHMENT_EFFECTIVENESS * effective_punishment
            )
            p.payoff = max(0, payoff_after_receiving - punishment_cost)

class Player(BasePlayer):
    
    global_group_id = models.IntegerField()
    local_group_id = models.IntegerField()
    
    # Contribution choices
    contribute_local = models.CurrencyField(min=0, max=C.ENDOWMENT)
    contribute_global = models.CurrencyField(min=0, max=C.ENDOWMENT)
    contribute_private = models.CurrencyField()

    # Punishment fields - 必要な数だけ定義（PLAYERS_PER_GROUPと同じ数）
    punish_p1 = models.IntegerField(
        min=0, max=C.MAX_PUNISHMENT_POINTS, 
        initial=0,
        blank=True,
        label="Punishment points for Player 1"
    )
    punish_p2 = models.IntegerField(
        min=0, max=C.MAX_PUNISHMENT_POINTS, 
        initial=0,
        blank=True,
        label="Punishment points for Player 2"
    )
    
    # Payoff tracking
    payoff_before_punishment = models.CurrencyField()
    punishment_received = models.IntegerField(initial=0)
    punishment_cost = models.CurrencyField(initial=0)

    def set_private(self):
        self.contribute_private = C.ENDOWMENT - self.contribute_local - self.contribute_global
