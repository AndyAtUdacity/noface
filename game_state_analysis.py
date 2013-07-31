from __future__ import division
from math import *

# Definition of Terms
# -------------------
#
# History: 		All HISTORY variables are lists. Each entry corresponds to a round. 
#
# Hunt Outcome: A hunt outcome is a list of values. Each value represents the amount of food 
# 				earned in a particular hunt. 
#
# Hunt w/ Me:   This ratio is calculated at the end of each round. It is equal to the number
#				of times my opponents hunted with me / number of hunt opportunities.
#
# True Avg Rep: Assuming that players will become more likely to slack as the game goes
#				on, average reputation won't be a good indicator of the state of the game.
# 				"True Average Reputation" is simply the # of hunts / # of hunt opportunities.
#				It is calculated at the end of every round. 
#
# Persuasion:	It's important that other people hunt with me. Persuasion is calculated at the end
#				of each round and is defined as the number of people who hunted with you divided
#				by the expected number (as calculated from that round's True Avg Rep) If this number
#				is greater than 1, it means that opponents are more likely to hunt with me than with
# 				a generic "other"

OPPONENT_REPUTATION_HISTORY = list() #should be list of lists, each list is one round of repuations
HUNT_OUTCOME_HISTORY = list() #should be list of lists, each list is one round of hunt_outcomes
MY_FOOD_HISTORY = list()
NUM_OPPS_HISTORY = list()
OPP_REP_AVG_HISTORY = list()
OPP_REP_AVG_DEV_HISTORY = list()
OPP_REP_CHG_HISTORY = list() #this list will have a len that is one less than the others.
CURRENT_PERSUASION = 0
PERSUASION_HISTORY = list()
TRUE_AVG_REPUTATION_HISTORY = list()
TRUE_CURRENT_AVG_REPUTATION = 0
CURRENT_NUM_OPPS = 0
CURRENT_NUM_PLAYERS = CURRENT_NUM_OPPS + 1
CURRENT_ROUND_NUMBER = 0
MY_CURRENT_FOOD = 0
MY_CURRENT_REPUTATION = 0
CURRENT_m = 0
CURRENT_PLAYER_REPUTATIONS = list()
CURRENT_HUNT_WITH_ME_RATIO = 0
HUNT_WITH_ME_RATIO_HISTORY = list()
ROUND_END_CALLED = False #this is a flag that lets me know if round_end() has been called yet
HUNT_OUTCOMES_CALLED = False #another flag
IS_FIRST_ROUND = True #Flag for the first round (since some of the numbers are weird in round 1)


def avg_dev(numbers):
	"""Calculates average deviation of a list of numbers"""
	mean = sum(numbers) / len(numbers)
	abs_devs = [abs(num-mean) for num in numbers]
	std_dev = sum(abs_devs) / len(abs_devs)
	return std_dev

def update_hunt_with_me_ratio(food_earnings):
	"""Updates CURRENT_HUNT_WITH_ME_RATIO and HUNT_WITH_ME_RATIO_HISTORY. 
	food_earnings is a list of earnings that is passed to the hunt_outcomes() 
	function at the end of each round"""
	num_hunts = 0
	num_slacks = 0
	for payout in food_earnings:
		if payout == 1 or payout == 0:
			num_hunts += 1
		elif payout == -2 or payout == -3:
			num_slacks += 1
		else:
			raise ValueError
	CURRENT_HUNT_WITH_ME_RATIO = num_hunts / (num_hunts + num_slacks)
	HUNT_WITH_ME_RATIO_HISTORY.append(CURRENT_HUNT_WITH_ME_RATIO)

def update_persuasion():
	"""Updates current persuasion and history"""
	global CURRENT_PERSUASION = CURRENT_HUNT_WITH_ME_RATIO / TRUE_CURRENT_AVG_REPUTATION
	global PERSUASION_HISTORY.append(CURRENT_PERSUASION)
	pass

def update_globals_beginning_of_round(round_number,
	current_food, current_reputation, m,  player_reputations):
	"""Updates all the global variables that can be updated at the beginning of the round.
	Should be called when hunt_choices is called."""
	global CURRENT_ROUND_NUMBER = round_number
	global MY_CURRENT_FOOD = current_food
	global MY_CURRENT_REPUTATION = current_reputation
	global CURRENT_PLAYER_REPUTATIONS = player_reputations
	global CURRENT_m = m
	global MY_FOOD_HISTORY.append(current_food)
	global OPPONENT_REPUTATION_HISTORY.append(player_reputations)
	global CURRENT_NUM_OPPS = len(player_reputations)
	global NUM_OPPS_HISTORY.append(CURRENT_NUM_OPPS)
	global OPP_REP_AVG_HISTORY.append((sum(player_reputations)/len(player_reputations)))
	global OPP_REP_AVG_DEV_HISTORY.append(avg_dev(player_reputations))
	if len(OPP_REP_AVG_HISTORY) > 1:
		global OPP_REP_CHG_HISTORY.append(OPP_REP_AVG_HISTORY[-1] - OPP_REP_AVG_HISTORY[-2])
	pass

def update_globals_round_end(award, m, number_hunters):
	"""Updates the global variables that depend on the information passed to round_end()"""
	hunt_opportunities = CURRENT_NUM_PLAYERS * (CURRENT_NUM_PLAYERS - 1)
	TRUE_CURRENT_AVG_REPUTATION = number_hunters / hunt_opportunities
	TRUE_AVG_REPUTATION_HISTORY.append(TRUE_CURRENT_AVG_REPUTATION)
	if HUNT_OUTCOMES_CALLED: 
		update_persuasion()
		IS_FIRST_ROUND = False #this would be the last thing called in this round
	pass

def hunt_outcomes(food_earnings):
	HUNT_OUTCOMES_CALLED = True
	update_globals_hunt_outcomes(food_earnings)
	pass

def round_end(award, m, number_hunters):
	ROUND_END_CALLED = True
	update_globals_round_end(award, m, number_hunters)
	pass











def update_globals_hunt_outcomes(food_earnings):
	"""Updates the global variables that depend on the information passed to hunt_outcomes()"""
	HUNT_OUTCOME_HISTORY.append(food_earnings)
	update_hunt_with_me_ratio(food_earnings)
	if ROUND_END_CALLED:
		update_persuasion()
		IS_FIRST_ROUND = False #this would be the last thing called in this round
	pass

def compare_reputation(current_reputation, current_avg_rep, current_rep_std):
	"""Classifies my player on a scale of very lazy (negative numbers) to very hardworking,
	based on current state of game."""
	return max(min(((current_reputation - current_reputation_avg_rep) / (current_rep_std + 0.0001)), 3), -3)



