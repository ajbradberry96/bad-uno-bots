import random
from game import Game
from card import CardColors
from pprint import pprint

class Player:
    def move(self, g: Game) -> tuple[int, bool]:
        raise(Exception('Abstract class, method not implemented'))

    def update(self, g: Game):
        pass

class RandomPlayer(Player):
    def __init__(self, seed=None) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)

    def move(self, g: Game):
        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = CardColors(self.r.randint(0, 3))
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            card = self.r.choice(g.legal_moves())
            if card.color == CardColors.BLACK:
                color = CardColors(self.r.randint(0, 3))
            else:
                color = None
            return g.make_move(card, color)

class HumanPlayer(Player):
    def move(self, g: Game):
        print("It's your turn, Player", g.active_player)
        print("Active Card:", g.active_card)
        if g.active_card.color == CardColors.BLACK:
            print("Active Color:", g.active_color)
        print("Your hand:")
        pprint(g.player_hands[g.active_player])

        if len(g.legal_moves()) == 0:
            print("Oh no! No legal moves.")

            new_card = g.draw()
            
            print("You drew a", new_card)

            if len(g.legal_moves()) == 1:
                play = input("Do you want to play it? y/n") == 'y'

                if play:
                    if new_card.color == CardColors.BLACK:
                        print("What color do you want to change the board to?")
                        for c in CardColors:
                            print(c)
                        color = CardColors(int(input()))
                    else:
                        color = None
                    return g.make_move(new_card, color)
                else:
                    return g.pass_turn()
            else:
                print("Passing turn...")
                return g.pass_turn()
        else:
            card_index = int(input("Which card do you want to play?"))

            if g.player_hands[g.active_player][card_index].color == CardColors.BLACK:
                print("What color do you want to change the board to?")
                for c in CardColors:
                    print(c)
                color = CardColors(int(input()))
            else:
                color = None
            
            return g.make_move(g.player_hands[g.active_player][card_index], color)

class SaveBlackPlayer(Player):
    def __init__(self, seed=None) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)

    def move(self, g: Game):
        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = CardColors(self.r.randint(0, 3))
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            filtered = [card for card in movepool if card.color != CardColors.BLACK]

            card = self.r.choice(movepool) if len(filtered) == 0 else self.r.choice(filtered)
            if card.color == CardColors.BLACK:
                color = CardColors(self.r.randint(0, 3))
            else:
                color = None
            return g.make_move(card, color)

'''
Least recently seen
'''
class LRSPlayer(Player):
    def __init__(self) -> None:
        self.last_seen_colors: list[CardColors] = [color for color in CardColors][:-1]
        self.last_seen_values: list[str] = [str(i) for i in range(10)]
        self.last_seen_values.extend(['w', 't', 'f', 's', 'r'])

    def move(self, g: Game):
        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = self.last_seen_colors[0]
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            for color in self.last_seen_colors:
                filtered_color = [card for card in movepool if card.color == color]
                if len(filtered_color) > 0:
                    for value in self.last_seen_values:
                        filtered_value = [card for card in filtered_color if card.value == value]
                        if len(filtered_value) > 0:
                            card = filtered_value[0]

                            if card.color == CardColors.BLACK:
                                color = self.last_seen_colors[0]
                            else:
                                color = None
                            
                            return g.make_move(card, color)
            card = movepool[0]
            if card.color == CardColors.BLACK:
                color = self.last_seen_colors[0]
            else:
                color = None

            if card.color != CardColors.BLACK:
                raise Exception("Couldn't find card")

            return g.make_move(card, color)

    def update(self, g: Game):
        self.last_seen_colors.append(self.last_seen_colors.pop(self.last_seen_colors.index(g.active_color)))
        self.last_seen_values.append(self.last_seen_values.pop(self.last_seen_values.index(g.active_card.value)))

class AlwaysChangeColorPlayer(Player):
    def __init__(self, seed=None) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)

    def move(self, g: Game):
        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = CardColors(self.r.randint(0, 3))
                    while color == g.active_color:
                        color = CardColors(self.r.randint(0, 3))
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            filtered = [card for card in movepool if card.color != g.active_color]

            card = self.r.choice(movepool) if len(filtered) == 0 else self.r.choice(filtered)
            if card.color == CardColors.BLACK:
                color = CardColors(self.r.randint(0, 3))
            else:
                color = None
            return g.make_move(card, color)

'''
Changes color to that which matches the most cards in hand whenever possible. 
Will save black cards until necessary.
TODO: Prioritize number in optimal set too
'''
class SurvivalistPlayer(Player):
    def __init__(self, seed=None) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)

    def move(self, g: Game):
        color_counts = {CardColors.BLUE: 0, CardColors.YELLOW: 0, CardColors.RED: 0, CardColors.GREEN: 0}
        for card in g.player_hands[g.active_player]:
            if card.color != CardColors.BLACK:
                color_counts[card.color] += 1
        
        color_counts = [(k, v) for k, v in color_counts.items()]
        color_priorities = sorted(color_counts, key=lambda tup: tup[1], reverse=True)

        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = color_priorities[0][0]
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            for color, _ in color_priorities:
                filtered = [card for card in movepool if card.color == color]

                if len(filtered) > 0:
                    card = self.r.choice(filtered)

                    return g.make_move(card)
            
            card = self.r.choice(movepool)
            if card.color == CardColors.BLACK:
                    color = color_priorities[0][0]
            else:
                color = None
            
            return g.make_move(card, color)

'''
Changes color to that which matches the least cards in hand whenever possible.
Will NOT save black cards, will play ASAP.
TODO: Prioritize number player doesn't have.
'''
class AntiSurvivalistPlayer(Player):
    def __init__(self, seed=None) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)

    def move(self, g: Game):
        color_counts = {CardColors.BLUE: 0, CardColors.YELLOW: 0, CardColors.RED: 0, CardColors.GREEN: 0}
        for card in g.player_hands[g.active_player]:
            if card.color != CardColors.BLACK:
                color_counts[card.color] += 1
        
        color_counts = [(k, v) for k, v in color_counts.items()]
        color_priorities = sorted(color_counts, key=lambda tup: tup[1])

        for card in g.legal_moves():
            if card.color == CardColors.BLACK:
                if card.color == CardColors.BLACK:
                    color = color_priorities[0][0]
                else:
                    color = None
            
                return g.make_move(card, color)

        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = color_priorities[0][0]
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            for color, _ in color_priorities:
                filtered = [card for card in movepool if card.color == color]

                if len(filtered) > 0:
                    card = self.r.choice(filtered)

                    return g.make_move(card)

        raise Exception('Should never be here')

'''
Chooses the legal move that changes the card in play to the one with most often seen features,
prioritizing color.
'''
class MostOftenSeenPlayer(Player):
    def move(self, g: Game):
        raise NotImplementedError

'''
Chooses the legal move that changes the card in play to the one with least often seen features,
prioritizing color.
'''
class LeastOftenSeenPlayer(Player):
    def move(self, g: Game):
        raise NotImplementedError
        
class LastDrawSeenByBestPlayer(Player):
    def __init__(self, seed=None, aggro=False) -> None:
        self.r = random.Random() if seed == None else random.Random(seed)
        self.surv_player = SurvivalistPlayer(seed)
        self.last_seen_drawn = None
        self.aggro = aggro
    
    def update(self, g: Game):
        self.surv_player.update(g)

        if self.last_seen_drawn == None:
            self.last_seen_drawn = [None for _ in range(len(g.player_hands))]
        
        if g.just_passed:
            self.last_seen_drawn[g.passing_player] = g.active_color
    
    def move(self, g: Game):
        if min(len(h) for h in g.player_hands) == len(g.player_hands[g.active_player]):
            return self.surv_player.move(g)
        
        winning_player = (0, 100)

        for i, hand in enumerate(g.player_hands):
            if len(hand) < winning_player[1]:
                winning_player = (i, len(hand))

        if self.last_seen_drawn[winning_player[0]] != None:
            color_priorities = [self.last_seen_drawn[winning_player[0]]]
        else:
            return self.surv_player.move(g)

        if len(g.legal_moves()) == 0:
            new_card = g.draw()

            if len(g.legal_moves()) == 1:
                if new_card.color == CardColors.BLACK:
                    color = color_priorities[0]
                else:
                    color = None
                return g.make_move(new_card, color)
            else:
                return g.pass_turn()
        
        else:
            movepool = g.legal_moves()
            for color in color_priorities:
                filtered = [card for card in movepool if card.color == color]

                if len(filtered) > 0:
                    card = self.r.choice(filtered)

                    return g.make_move(card)
            
            if self.aggro:
                for card in movepool:
                    if card.color == CardColors.BLACK:
                        return g.make_move(card, color_priorities[0])

            return self.surv_player.move(g)
        
