from abc import ABC, abstractmethod
from cards import Hand
from random import randint, shuffle

class Player(ABC):

    def __init__(self, name, hand):
        ''' Given name, and hand (deck of cards), initializes player '''
        self.hand = Hand(hand)
        self.name = name

    def show_cards(self):
        print(str(self.name))
        self.hand.show_cards()

    def bhabhi_move(self, table_cards):
        ''' abstract method. table_cards is a Hand
            containing cards on the table,

            * function should return the card played by the player
            * it should be a valid move depending on the table cards.
        '''

        pass

class HumanPlayer(Player):
    ''' human player which interacts with game through command line '''
    def bhabhi_move(self, table_cards):
        selection = 0

        print("Would you like to see your cards? (y/n)")
        show_player_cards = input()
        if ( show_player_cards.lower() == 'y' ):
            self.hand.show_cards()

        if table_cards.get_card_count() > 0:
            table_suit = table_cards.get_bottom_suit()
            if self.hand.has_suit( table_suit ):
                # Case 1 - player has the live suit
                valid_move = False
                while not valid_move:
                    print("(Suited) Enter the index of the"
                    + " card you would like to play: ")
                    selection = int(input())
                    valid_move = self.hand.get_card_suit(selection)==table_suit
            else:
                # Case 2 - player does not have live suit
                valid_moves = list(range(1, (self.hand.get_card_count()+1)))
                while not (selection in valid_moves):
                    print("(Any) Enter the index of the"
                    + " card you would like to play: ")
                    selection = int(input())
        else:
            # Case 3 - player is starting round
            valid_moves = list(range(1, (self.hand.get_card_count()+1)))
            while not (selection in valid_moves):
                print("(Start of Round) Enter the index of the"
                + " card you would like to play: ")
                selection = int(input())

        return self.hand.pop_card(selection)

class MonkeyCPU(Player):
    ''' CPU player which selects cards at random to play '''
    def bhabhi_move(self, table_cards):

        # note: randint includes end points, range() does not
        if table_cards.get_card_count() > 0:
            table_suit = table_cards.get_bottom_suit()

            if self.hand.has_suit( table_suit ):
                # Case 1 - player has the live suit
                self.hand.shuffle_cards()
                end = self.hand.get_card_count()+1
                for i in range(1,  end):
                    if self.hand.get_card_suit(i) == table_suit:
                        selection = i
                        i = end
            else:
                # Case 2 - player does not have live suit
                selection = randint(1, self.hand.get_card_count())
        else:
            # Case 3 - player is starting round (any)
            selection = randint(1, self.hand.get_card_count())

        return self.hand.pop_card( selection )
