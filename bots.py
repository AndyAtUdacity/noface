from Player import BasePlayer
import random

##########################################################################################
##                                STATIC BOTS                                           ##
##########################################################################################

class Hunter(BasePlayer):
    '''Player that always hunts.'''
    def __init__(self):
        self.name = "Hunter"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h']*len(player_reputations)

class Slacker(BasePlayer):
    '''Player that always slacks.'''
    
    def __init__(self):
        self.name = "Slacker"
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['s']*len(player_reputations)

class AlternateHunter(BasePlayer):
    '''Player that alternates between hunting and slacking.'''
    def __init__(self):
        self.name = "AlternateHunter"
        
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
            if i % 2 == 0:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

class AlternateSlacker(BasePlayer):
    '''Player that alternates between hunting and slacking.'''
    def __init__(self):
        self.name = "AlternateSlacker"
        
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
            if i % 2 == 0:
                hunt_decisions.append('s')
            else:
                hunt_decisions.append('h')
        return hunt_decisions

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




##########################################################################################
##                                UTILITY(ref) BOTS                                     ##
##########################################################################################

class BalancedHunter(BasePlayer):
    '''Player that hunts with 1 - m of the player for each hunt'''
    def __init__(self):
        self.name = "BalancedHunter"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h' if random.random() < 1 - rep else 's' for rep in player_reputations]


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
        
class BoundedHunter(BasePlayer):
    '''Player that hunts whenever people whose reputation is within some range.'''
    def __init__(self,lower,upper):
        self.name = "BoundedHunter" + str(lower)+'-'+str(upper)
        self.low = lower
        self.up = upper

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h' if self.low <= rep <= self.up else 's' for rep in player_reputations]
        
class AverageHunter(BasePlayer):
    '''Player that tries to maintain the average reputation, but spreads its hunts randomly.'''
    
    def __init__(self):
        self.name = "AverageHunter"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        avg_rep = sum(player_reputations) / float(len(player_reputations))
        return ['h' if random.random() < avg_rep else 's' for rep in player_reputations]

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



##########################################################################################
##                                UTILITY(food, rep) BOTS                               ##
##########################################################################################

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

##########################################################################################
##                          UTILITY(food, rep, time) BOTS                               ##
##########################################################################################

class BecomesCorrupt(BasePlayer):
    """Player that starts by always hunting, then becomes more likely to slack"""

    def __init__(self, corruptionRound):
        self.name = "BecomesCorrupt" + str(corruptionRound)
        self.corrupt = corruptionRound
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        p_hunt = max((1.0 - round_number / self.corrupt),0.0)
        hunt_decisions = list()
        for reputation in player_reputations:
            if random.random() < p_hunt:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions

class MoreCorrupt(BasePlayer):
    """Players that starts some probability of hunting, then becomes more likely to slack"""

    def __init__(self, pHunt, corruptionRound):
        self.name = "MoreCorrupt" + str(pHunt) + "-" +  str(corruptionRound)
        self.corrupt = corruptionRound
        self.pHunt = pHunt

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations
                    ):
        p_hunt = max((self.pHunt - round_number / self.corrupt),0.0)
        hunt_decisions = list()
        for reputation in player_reputations:
            if random.random() < p_hunt:
                hunt_decisions.append('h')
            else:
                hunt_decisions.append('s')
        return hunt_decisions
