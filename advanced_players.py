from cards import Hand
from random import randint, shuffle
import numpy as np
from qlearn import QLearner

class QLearnAI(QLearner):
    ''' fully trained q learning ai '''
    def bhabhi_move(self, table_cards):
        state = self.compute_state(table_cards)
        turn_case = state % 3
        card_returned = None

        if (self.qtable[state, 0] > self.qtable[state, 1]):
            card_returned = self.low_card_move(turn_case, table_cards)
        else:
            card_returned = self.high_card_move(turn_case, table_cards)

        return card_returned
