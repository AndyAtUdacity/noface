from Player import BasePlayer
import random

class Pushover(BasePlayer):
    '''Player that always hunts.'''
    def __init__(self):
        self.name = "Pushover"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h']*len(player_reputations)

class Dignified(BasePlayer):
    """Player that hunts with people who have higher reputation"""
    def __init__(self):
        self.name = "Dignified"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        hunt_decisions = list()
        for reputation in player_reputations:
            if reputation > current_reputation:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

class Hungry(BasePlayer):
    """Player who maximizes expected food, based on assumption that opponent's
    reputation is equal to his probability of hunting."""
    def __init__(self):
        self.name = "Hungry"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
       
        def hunt_EV_decider(p_hunt):
            p_slack = 1.0 - p_hunt
            hunt_EV = -3.0*p_slack
            slack_EV = 1.0*p_hunt - 2.0*p_slack
            if hunt_EV > slack_EV:
                return 'h'
            else:
                return 's'
        hunt_decisions = list()
        for reputation in player_reputations:
            hunt_decisions.append(hunt_EV_decider(reputation))
        return hunt_decisions

class Vain(BasePlayer):
    """Player that plays like Hungry, but with some value towards reputation"""
    def __init__(self):
        self.name = "Vain"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        def hunt_EV_decider(p_hunt, round_number = round_number, vanity=100):
            p_slack = 1.0 - p_hunt
            hunt_EV = -3.0*p_slack + vanity / round_number
            slack_EV = 1.0*p_hunt - 2.0*p_slack
            if hunt_EV > slack_EV:
                return 'h'
            else:
                return 's'
        hunt_decisions = list()
        for reputation in player_reputations:
            hunt_decisions.append(hunt_EV_decider(reputation))
        return hunt_decisions

class BecomesCorrupt(BasePlayer):
    """Player that starts by always hunting, then gradually becomes more
    likely to slack"""

    def __init__(self):
        self.name = "BecomesCorrupt"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        p_hunt = max((1.0 - round_number / 120),0.0)
        hunt_decisions = list()
        for reputation in player_reputations:
            if random.random() < p_hunt:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

class BecomesCorruptSlow(BasePlayer):
    """Player that starts by always hunting, then gradually becomes more
    likely to slack"""

    def __init__(self):
        self.name = "BecomesCorruptSlow"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        p_hunt = max((1.0 - round_number / 200),0.0)
        hunt_decisions = list()
        for reputation in player_reputations:
            if random.random() < p_hunt:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

class BecomesCorruptFast(BasePlayer):
    """Player that starts by always hunting, then gradually becomes more
    likely to slack"""

    def __init__(self):
        self.name = "BecomesCorruptFast"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        p_hunt = max((1.0 - round_number / 60),0.0)
        hunt_decisions = list()
        for reputation in player_reputations:
            if random.random() < p_hunt:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions
  

class Freeloader(BasePlayer):
    '''Player that always slacks.'''
    
    def __init__(self):
        self.name = "Freeloader"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['s']*len(player_reputations)
        

class Alternator(BasePlayer):
    '''Player that alternates between hunting and slacking.'''
    def __init__(self):
        self.name = "Alternator"
        self.last_played = 's'
        
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        hunt_decisions = []
        for i in range(len(player_reputations)):
            self.last_played = 'h' if self.last_played == 's' else 's'
            hunt_decisions.append(self.last_played)

        return hunt_decisions

class MaxRepHunter(BasePlayer):
    '''Player that hunts only with people with max reputation.'''
    def __init__(self):
        self.name = "MaxRepHunter"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        threshold = max(player_reputations)
        return ['h' if rep == threshold else 's' for rep in player_reputations]


class Random(BasePlayer):
    '''
    Player that hunts with probability p_hunt and
    slacks with probability 1-p_hunt
    '''
    
    def __init__(self, p_hunt):
        self.name = "Random" + str(p_hunt)
        self.p_hunt = p_hunt

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h' if random.random() < self.p_hunt else 's' for p in player_reputations]

class FairHunter(BasePlayer):
    '''Player that tries to be fair by hunting with same probability as each opponent'''
    def __init__(self):
        self.name = "FairHunter"

    def hunt_choices(
                self,
                round_number,
                current_food,
                current_reputation,
                m,
                player_reputations,
                ):
        return ['h' if random.random() < rep else 's' for rep in player_reputations]
        
