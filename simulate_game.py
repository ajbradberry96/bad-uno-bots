from players import Player
from game import Game

def simulate_game(players: list[Player]):
    g = Game(len(players))
    game_over = False
    player = g.active_player

    while not game_over:
        player, game_over = players[player].move(g)

        for p in players:
            p.update(g)

    return player