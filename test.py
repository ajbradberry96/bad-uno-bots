from simulate_game import simulate_game
from players import AntiSurvivalistPlayer, LastDrawSeenByBestPlayer, RandomPlayer, SaveBlackPlayer, LRSPlayer, AlwaysChangeColorPlayer, SurvivalistPlayer, LastDrawSeenByBestPlayer
import numpy as np

# Type, games, wins
player_scores = {'ACC': [AlwaysChangeColorPlayer, 0, 0], 
                 'Rand': [RandomPlayer, 0, 0], 
                 'Save': [SaveBlackPlayer, 0, 0], 
                 'LRS': [LRSPlayer, 0, 0], 
                 'Surv': [SurvivalistPlayer, 0, 0],
                 'ASurv': [AntiSurvivalistPlayer, 0, 0],
                 'LDSB': [LastDrawSeenByBestPlayer, 0, 0]}

n = 100000

for _ in range(n):
    player_types = list(np.random.choice(list(player_scores.keys()), 4, False))

    players = [player_scores[t][0]() for t in player_types]

    result = simulate_game(players)

    for p in range(4):
        player_scores[player_types[p]][1] += 1
        if p == result:
            player_scores[player_types[p]][2] += 1

for key in player_scores.keys():
    print(key, '%0.3f' % (player_scores[key][2]/player_scores[key][1]))


