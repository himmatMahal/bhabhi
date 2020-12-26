from random import shuffle
# import pygame

CARD_SUITS = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
CARD_NUMS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
CARD_PNG_NUMS = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']

class Deck:
    ''' Deck
        After Deal is used, the deck is empty, all cards have been pop()'ed
        attributes: full_deck
        functions: deal
    '''

    def __init__(self):
        self.full_deck = []
        ''' full_deck is a list of tuples, each tuple represents a card:
            (suit, rank, value) '''
        for i in range(len(CARD_SUITS)):
            card_val = 0
            for j in range(len(CARD_NUMS)):
                self.full_deck.append((CARD_SUITS[i], CARD_NUMS[j], card_val))
                j=j+1
                card_val=card_val+1
            i=i+1

    def deal(self, player_count):
        ''' returns list with player_count indices, each index contains
            a list of cards '''
        shuffle(self.full_deck)
        dealt_cards = [ [] for player in range(player_count)]
        j=0
        while j<52:
            if len(self.full_deck) > 0:
                i = j%player_count
                dealt_cards[i].append(self.full_deck.pop())
            j=j+1
        return dealt_cards

    def __str__(self):
        return str(self.full_deck)


class Hand:
    ''' Hand
        attributes: cards
        functions: pop_card, pop_all_cards, show_cards
                   pick_up_cards, pick_up_card
                   get_card_count, has_suit, has_specific_card,
                   get_bottom_suit, shuffle_cards, top_card_is_highest
    '''
    def __init__(self, cards):
        ''' cards should be a list of card tuples '''
        self.cards = cards

    def __str__(self):
        return str(self.cards)

    def pop_all_cards(self):
        ''' returns and removes all cards from hand '''
        tmp = self.cards.copy()
        self.cards.clear()
        return tmp

    def pop_card(self, card):
        ''' pops given card from hand.
            card may be an index (STARTING at 1), or card tuple '''
        if ( isinstance(card, tuple) ):
            return self.cards.pop( self.cards.index(card) )

        elif ( isinstance(card, int) ):
            return self.cards.pop(card-1)

        else:
            raise TypeError("Error: invalid type. Expected int or tuple, got "
                            + str(type(card)) )

    def pick_up_cards(self, cards_picked):
        ''' takes a list of card tuples and extends it to the Hand.
            does not check if list contains valid cards so use carefully,
            also doesn't check for duplicates in deck
        '''
        if ( isinstance(cards_picked, list) ):
            self.cards.extend(cards_picked)

        else:
            raise TypeError("Error: invalid type, expected list of cards")

    def pick_up_card(self, card_picked):
        ''' add a single card to the hand '''
        self.cards.append( card_picked )

    def show_cards(self):
        ''' prints cards with clean formatting '''
        i=1
        for card in self.cards:
            print('[#{}: {} of {}]'.format(i, card[1], card[0]), end = '\t\t')
            if i%3==0:
                print('')
            i=i+1
        print('\n')

    def get_card_count(self):
        return len(self.cards)

    def has_suit(self, suit):
        ''' checks if hand contains suit '''
        for card in self.cards:
            if (card[0] == suit):
                return True
        return False

    def has_specific_card(self, specific_card):
        ''' check if hand contains card '''
        return specific_card in self.cards

    def get_bottom_suit(self):
        ''' returns suit of bottom card in hand, useful for determining
            suit of table cards in bhabhi '''
        return self.cards[0][0]

    def get_card_suit(self, card_idx):
        ''' given index of card (STARTING at 1), returns its suit '''
        return self.cards[ card_idx - 1 ][0]

    def shuffle_cards(self):
        ''' shuffles cards in place '''
        shuffle(self.cards)

    def top_card_is_highest(self):
        ''' checks if card on top of "stack" is higher than the others '''
        highest = True
        for i in range(self.get_card_count() - 1):
            # index 2 of card tuple represents rank
            if self.cards[-1][2] < self.cards[i][2]:
                highest = False
        return highest

    def top_card_is_diffsuit(self):
        return (not (self.get_bottom_suit() == self.cards[-1][0]))


class GUIDeck:
    ''' same as Deck, with images on each card tuple for GUI '''
    def __init__(self):
        import pygame

        self.full_deck = []
        ''' full_deck is a list of tuples, each tuple represents a card:
            (suit, rank, value, image) '''
        for i in range(len(CARD_SUITS)):

            card_val = 0
            for j in range(len(CARD_NUMS)):
                file_name = 'card_pics/{}_of_{}.jpg'.format(
                    CARD_PNG_NUMS[j], CARD_SUITS[i].lower()
                )
                img = pygame.image.load(file_name)
                img = pygame.transform.smoothscale(img,(50,72))
                self.full_deck.append(
                    (CARD_SUITS[i], CARD_NUMS[j], card_val, img)
                )
                card_val=card_val+1

    def deal(self, player_count):
        ''' returns list with player_count indices, each index contains
            a list of cards '''
        shuffle(self.full_deck)
        dealt_cards = [ [] for player in range(player_count)]
        j=0
        while j<52:
            if len(self.full_deck) > 0:
                i = j%player_count
                dealt_cards[i].append(self.full_deck.pop())
            j=j+1
        return dealt_cards

    def __str__(self):
        return str(self.full_deck)
