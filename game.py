from card import Card, CardColors
import random

class Game:
    def __init__(self, num_players: int) -> None:
        self.num_players = num_players

        self.deck = [Card(CardColors(c), str(v)) for c in range(4) for v in range(10)]
        self.deck.extend(Card(CardColors(c), str(v)) for c in range(4) for v in range(1, 10))
        self.deck.extend(Card(CardColors(c), 's') for c in range(4))
        self.deck.extend(Card(CardColors(c), 'r') for c in range(4))
        self.deck.extend(Card(CardColors(c), 't') for c in range(4))
        self.deck.extend(Card(CardColors.BLACK, 'w') for _ in range(4))
        self.deck.extend(Card(CardColors.BLACK, 'f') for _ in range(4))

        self.order = 1
        
        self.just_passed = False
        self.passing_player = None
        random.shuffle(self.deck)

        self.active_card = self.deck.pop()
        self.active_color = self.active_card.color
        self.active_player = 0
        self.player_hands = [[self.deck.pop() for _ in range(7)] for _2 in range(num_players)]
        self.discard = []

    def legal_moves(self) -> list[Card]:
        ret = []
        hand = self.player_hands[self.active_player]
        for card in hand:
            if (self.active_color == CardColors.BLACK or 
                card.color == CardColors.BLACK or 
                card.color == self.active_color or 
                card.value == self.active_card.value):
                ret.append(card)
        
        return ret 

    def draw(self) -> Card:
        if len(self.deck) == 0:
            self.deck.extend(self.discard)
            random.shuffle(self.deck)
        
        self.player_hands[self.active_player].append(self.deck.pop())

        return self.player_hands[self.active_player][-1]

    def pass_turn(self) -> tuple[int, bool]:
        self.just_passed = True
        self.passing_player = self.active_player
        self.active_player = (self.active_player + self.order) % self.num_players

        game_over = 0 in [len(hand) for hand in self.player_hands]

        return self.active_player, game_over

    def make_move(self, card: Card, color: CardColors=None) -> tuple[int, bool]:
        self.just_passed = False
        moving_player = self.active_player
        self.player_hands[self.active_player].pop(self.player_hands[self.active_player].index(card))
        self.discard.append(self.active_card)
        self.active_card = card
        self.active_color = color if color != None else self.active_card.color

        if card.value == 'r':
            self.reverse_order()
        elif card.value == 's':
            self.active_player = (self.active_player + self.order) % self.num_players
        
        self.active_player = (self.active_player + self.order) % self.num_players

        if card.value == 't':
            self.draw()
            self.draw()
            self.active_player = (self.active_player + self.order) % self.num_players
        elif card.value == 'f':
            for _ in range(4):
                self.draw()
            self.active_player = (self.active_player + self.order) % self.num_players

        game_over = 0 in [len(hand) for hand in self.player_hands]

        return moving_player if game_over else self.active_player, game_over

    def reverse_order(self) -> None:
        self.order *= -1