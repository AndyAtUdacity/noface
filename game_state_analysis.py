from __future__ import division
from math import *

REP_AVG = list()
REP_STD = list()
REP_CHG = list()
NUM_OPPS = list()

def std_dev(numbers):
	mean = sum(numbers) / len(numbers)
	abs_devs = [abs(num-mean) for num in numbers]
	std_dev = sum(abs_devs) / len(abs_devs)
	return std_dev

def update_game_stats(player_reputations):
	NUM_OPPS.append(len(player_reputations))
	if len(player_reputations) > 0: 
		REP_AVG.append(sum(player_reputations)/len(player_reputations))	
		REP_STD.append(std_dev(player_reputations))
	if len(REP_AVG) > 1:
		REP_CHG.append(REP_AVG[-1]-REP_AVG[-2])
	pass

def compare_reputation(current_reputation, current_avg_rep, current_rep_std):
	"""Classifies my player on a scale of very lazy (negative numbers) to very hardworking,
	based on current state of game."""
	return max(min(((current_reputation - current_reputation_avg_rep) / (current_rep_std + 0.0001)), 3), -3)

def predict_rep_in_10_rounds(current_avg_rep, current_rep_chg_rate = 0):
	return current_avg_rep + 10 * current_rep_chg_rate

def predict_rounds_left(food_per_player, num_rounds, current_food_chg_rate = 0, reward = False):
	if reward:
		current_food_chg_rate = (food_per_player - 300) / num_rounds
	return food_per_player / current_food_chg_rate