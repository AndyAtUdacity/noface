
from __future__ import division, print_function
from Game import Game
from bots import *
from Player import Player

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
	randomHunters = [Random(i/10) for i in range(1, 10)]
	corrupters = [BecomesCorrupt(i) for i in range(1, 300)]
	moreCorrupters = [MoreCorrupt(p/10, day) for p in range(1,10) for day in range (1, 300)]
	boundedHunters =[BoundedHunter(i/10, j/10) for i in range(1,10) for j in range(1,10) if i < j]
	players = [Hunter(), Slacker(), AlternateHunter(), AlternateSlacker(), MaxRepHunter(), AverageHunter(), Dignified(), Hungry(), FairHunter(), Vain()]
	players = players + randomHunters + corrupters + boundedHunters + moreCorrupters
	game = Game(players)
	game.play_game()