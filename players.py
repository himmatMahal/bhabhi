from abc import ABC, abstractmethod
from cards import Hand
from random import randint, shuffle

class Player(ABC):

    def __init__(self, name, hand):
        ''' Given name, and hand (deck of cards), initializes player '''
        self.hand = Hand(hand)
        self.name = name
        self.rounds_played = 0

    def show_cards(self):
        print(str(self.name))
        self.hand.show_cards()

    def pick_up_cards(self, c):
        self.hand.pick_up_cards(c)

    def pick_up_card(self, c):
        self.hand.pick_up_card(c)

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
        selection = 0
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

class HumanLikeCPUI(Player):
    ''' human-like CPU I - Always selects highest possible card '''
    def bhabhi_move(self, table_cards):
        selection = 0
        if table_cards.get_card_count() > 0:
            table_suit = table_cards.get_bottom_suit()
            if self.hand.has_suit( table_suit ):
                # Case 1 - player has the live suit
                card_values = [ card[2] if card[0]==table_suit else -1
                                for card in self.hand.cards ]
                selection = card_values.index(max(card_values))+1
            else:
                # Case 2 - player does not have live suit
                card_values = [ card[2] for card in self.hand.cards ]
                selection = card_values.index(max(card_values))+1
        else:
            # Case 3 - player is starting a round
            card_values = [ card[2] for card in self.hand.cards ]
            selection = card_values.index(max(card_values))+1

        return self.hand.pop_card( selection )

class HumanLikeCPUII(Player):
    ''' human-like CPU II - uses more advanced human-like tactics:
        - plays highest if making someone pick up
        - when beginning a new round, plays high in early game, then in late
          game, cpu gets rid of suits by playing suit which cpu has lowest of
        - when playing the table suit, plays high cards in the early game. In
          late game, cpu tries to play lower than the table cards while
          getting rid of high cards
    '''
    def select_lowest_occuring_card(self):
        suits = [card[0] for card in self.hand.cards]
        # make list of possible suits
        possibilities = list(dict.fromkeys(suits))
        # make list of count of each suit, this list matches 1-1 with the
        # list of possible suits
        suit_counts = []
        for possible_suit in possibilities:
            suit_counts.append(suits.count(possible_suit))
        # index the suit with the lowest occurence
        suit_to_play = possibilities[ suit_counts.index(min(suit_counts)) ]
        # make a list of possible cards to play, then sort by value
        possible_cards = [ card for card in self.hand.cards
                           if card[0]==suit_to_play ]
        possible_cards.sort(key=lambda card:card[2])
        # .sort() sorts in ascending order, and we want the highest value card
        return self.hand.pop_card(possible_cards[-1])

    def select_highest_low_value_suited(self, table_suit, table_cards):
        # play highest possible card less than any table cards
        max_live = max([card[2] for card in table_cards.cards])
        # list of options: playable cards that have lower rand than max card
        options = [ card for card in self.hand.cards
                    if (card[2]<max_live and card[0]==table_suit) ]
        # if these options exist, sort them and play the highest
        if options:
            options.sort(key=lambda card:card[2])
            card_to_pick = options[-1]
            return self.hand.pop_card(card_to_pick)
        # if no options, default to playing highest
        else:
            card_values = [ card[2] if card[0]==table_suit else -1
                            for card in self.hand.cards ]
            return self.hand.pop_card(card_values.index(max(card_values))+1)

    def bhabhi_move(self, table_cards):
        selection = 0
        early_game = self.rounds_played <= 3
        card_to_play = None

        if table_cards.get_card_count() > 0:
            table_suit = table_cards.get_bottom_suit()
            if self.hand.has_suit( table_suit ):
                # Case 1 - player has the live suit
                if early_game:
                    card_values = [ card[2] if card[0]==table_suit else -1
                                    for card in self.hand.cards ]
                    card_to_play = self.hand.pop_card(
                        card_values.index(max(card_values))+1
                    )
                else: # late game
                    card_to_play = self.select_highest_low_value_suited(
                        table_suit, table_cards
                    )
            else:
                # Case 2 - does not have live suit (making someone pick up)
                card_to_play = self.select_lowest_occuring_card()
        else:
            # Case 3 - player is starting a round
            card_values = [ card[2] for card in self.hand.cards ]
            if early_game:
                card_to_play = self.hand.pop_card(
                    card_values.index(max(card_values))+1
                )
            else: # late game
                card_to_play = self.select_lowest_occuring_card()

        self.rounds_played += 1

        return card_to_play
