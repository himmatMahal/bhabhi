import numpy as np
import random as rnd

from players import Player
from cards import Hand

class QLearner(Player):
    ''' q learning agent '''
    STATE_COUNT = 81
    ACTION_COUNT = 2 # 0- play low card...  1- play high card
    QTABLE_FILE = "qtable.csv"
    gamma = 0.81

    def __init__(self, name, hand=[], epsilon=0.75, lr=0.1, gamma=0.81):
        ''' extends Player with attributes below which help update qtable
            with rewards. explore_fraction determines how frequently
            a random move is made '''
        super().__init__(name, hand)

        self.qtable = np.loadtxt(self.QTABLE_FILE, delimiter=",")

        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        # update these variables after every single bhabhi_move()
        self.previous_action = 0
        self.previous_state = 0
        self.previous_card_rank_sum = self.sum_card_ranks()

    def sum_card_ranks(self):
        return np.sum([card[2] for card in self.hand.cards])

    def update_qtable(self):
        ''' when training, use this function at the end of every round '''
        reward = self.previous_card_rank_sum - self.sum_card_ranks()
        state = self.previous_state
        action = self.previous_action

        # getting possible future states for all turn cases
        possible_future_states = []
        i = self.compute_state(Hand([]))
        for j in range(2):
            if (i+j < self.STATE_COUNT):
                possible_future_states.extend( self.qtable[i+j] )
        # updating qtable array
        self.qtable[state, action] = self.qtable[state, action] + self.lr \
                                * (reward + (self.gamma) \
                                * (np.max(possible_future_states)) \
                                - self.qtable[state, action] )

    def compute_state(self, table_cards):
        ''' gets current state, and converts it into an index 0-80.
            can be thought of as base 3 number, 3^0 place contains
            the current turn case for the player
            (0- suited, 1- any (pick up), 2- any (start round)) '''

        case = 0
        if table_cards.get_card_count() > 0:
            table_suit = table_cards.get_bottom_suit()
            if self.hand.has_suit( table_suit ):
                # Case 1 - player has the live suit
                case = 0
            else:
                # Case 2 - player does not have live suit
                case = 1
        else:
            # Case 3 - player is starting round
            case = 2

        rank = 0
        sum = self.sum_card_ranks()
        if sum > 80:
            rank = 2
        elif sum > 20:
            rank = 1

        round = 0
        current_round = self.rounds_played
        if current_round>13:
            round = 2
        elif current_round>5:
            round = 1

        count = 0
        num_cards = self.hand.get_card_count()
        if num_cards>12:
            count = 2
        elif num_cards>5:
            count = 1

        return (3**3)*count + (3**2)*round + (3)*rank + case

    def high_card_move(self, turn_case, table_cards):
        card_selected = None

        if turn_case==0: #
            table_suit = table_cards.get_bottom_suit()
            # player has the live suit
            card_vals = [ card[2] if card[0]==table_suit else -1
                            for card in self.hand.cards ]
            card_selected = self.hand.pop_card(
                card_vals.index(max(card_vals))+1
            )
        else:
            # player is starting round
            # OR player does not have live suit
            card_vals = [ card[2] for card in self.hand.cards ]
            card_selected = self.hand.pop_card(
                card_vals.index(max(card_vals))+1
            )

        return card_selected

    def low_card_move(self, turn_case, table_cards):
        card_selected = None

        if turn_case==0:
            table_suit = table_cards.get_bottom_suit()
            # player has the live suit
            card_vals = [ card[2] if card[0]==table_suit else -1
                            for card in self.hand.cards ]
            card_selected = self.hand.pop_card(
                card_vals.index(min(card_vals))+1
            )
        elif turn_case==1:
            # player does not have live suit
            card_vals = [ card[2] for card in self.hand.cards ]
            card_selected = self.hand.pop_card(
                card_vals.index(min(card_vals))+1
            )
        else:
            # player is starting round
            suits = [card[0] for card in self.hand.cards]
            possibilities = list(dict.fromkeys(suits))
            suit_counts = []
            for possible_suit in possibilities:
                suit_counts.append(suits.count(possible_suit))
            suit_to_play = possibilities[ suit_counts.index(min(suit_counts)) ]
            possible_cards = [ card for card in self.hand.cards
                               if card[0]==suit_to_play ]
            possible_cards.sort(key=lambda card:card[2])
            card_selected = self.hand.pop_card(possible_cards[-1])

        return card_selected

    def bhabhi_move(self, table_cards):
        state = self.compute_state(table_cards)
        action = -1
        turn_case = state % 3
        card_returned = None

        self.previous_card_rank_sum = self.sum_card_ranks()

        if rnd.uniform(0,1) < self.epsilon:
            # make random move
            action = rnd.randint(0,1)
            if (action==1): # high card
                card_returned = self.high_card_move(turn_case, table_cards)
            else: # low card
                card_returned = self.low_card_move(turn_case, table_cards)
        else:
            # make calculated move: if value for playing a low card is higher,
            # play low, otherwise play high
            action = 0
            if (self.qtable[state, 0] > self.qtable[state, 1]):
                card_returned = self.low_card_move(turn_case, table_cards)
            else:
                card_returned = self.high_card_move(turn_case, table_cards)
                action = 1

        self.previous_state = state
        self.previous_action = action
        self.rounds_played += 1
        return card_returned

    def save_qtable(self):
        ''' after training, call this method to save the qtable file with
            updated value '''
        ## DEBUG:
        np.savetxt(self.QTABLE_FILE, self.qtable, delimiter=",")
