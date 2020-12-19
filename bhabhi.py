from random import shuffle
from random import randint
import math

from cards import Hand, Deck
from players import HumanPlayer, MonkeyCPU

ACE_OF_SPADES = ('Spades', 'A', 12)

def print_status(just_played, table_cards):
    ''' print status of game
        takes player who most recently played, garbage, and table cards
        to display status
    '''
    print(f"Most recent turn: {just_played.name}")
    print(f"table: ")
    table_cards.show_cards()
    print("----------------------------------------")

def main_loop(players, printing_on, show_cpu):

    show_every_round = printing_on
    show_cpu_cards = show_cpu
    # set this variable to true to print status every round

    garbage = Hand([])
    table_cards = Hand([])

    starter = -1
    num_live_players = len(players)

    # Initializing game: first round decides who starts
    i=0
    while i<num_live_players:
        # First move of game - player plays ace of spades
        if i<1:
            for player in players:
                if player.hand.has_specific_card(ACE_OF_SPADES):
                    starter = players.index( player )
                    table_cards.pick_up_card(
                        player.hand.pop_card(ACE_OF_SPADES)
                    )
                    i+=1
        # remaining players play their ace after first player
        else:
            # next player in rotation plays
            table_cards.pick_up_card(
                players[(starter + i) % num_live_players].bhabhi_move(
                    table_cards
                )
            )

            if show_every_round:
                print_status(
                    players[(starter+i)%num_live_players], table_cards
                )

            i+=1

    # dump all cards
    garbage.pick_up_cards( table_cards.pop_all_cards() )

    # central loop for game
    j=1
    while num_live_players>1:
        if show_every_round:
            print(f"\n<---Next Round--->\nRound #{j}")
        j+=1

        # begin a single round
        round_end_early = False
        i=0
        next_starting_player = players[starter]
        while i<num_live_players and (not round_end_early):

            # player takes turn
            current = players[(starter + i) % num_live_players]
            if show_cpu_cards:
                if not isinstance(current, HumanPlayer):
                    current.hand.show_cards()            
            table_cards.pick_up_card( current.bhabhi_move(table_cards) )

            # checking game status
            if not (i==0):
                if table_cards.top_card_is_diffsuit():
                    round_end_early = True

                elif table_cards.top_card_is_highest():
                    # checking if player who just played threw the highest card
                    next_starting_player = current

            if show_every_round:
                print_status(current, table_cards)

            i+=1
        # loop breaks once everyone played, or round ended early (pick up)

        if round_end_early:
            if show_every_round:
                print(f"{next_starting_player.name} picks up the table cards!")

            next_starting_player.hand.pick_up_cards(
                table_cards.pop_all_cards()
            )

        else:
            garbage.pick_up_cards( table_cards.pop_all_cards() )

        # case where next_starting_player must pick from garbage since
        # they start the next round
        if next_starting_player.hand.get_card_count() < 1:
            if show_every_round:
                print(str(next_starting_player.name)+" picks a card from"
                      +" the garbage since they threw highest but are out!")

            garbage.shuffle_cards()
            next_starting_player.hand.pick_up_card( garbage.pop_card(1) )

        # removing winners:
        next_round_players = [ player for player in players
                               if player.hand.get_card_count() >= 1 ]
        if show_every_round:
            print("End of Round status: ")
            for player in players:
                print(f"{player.name} - {player.hand.get_card_count()} cards")

        players.clear()
        players = next_round_players
        num_live_players = len(players)

        # setting up starting player for next round
        starter = players.index( next_starting_player )
    # Game over once all but one players are eliminated

    print( players[0].name + " is the Bhabhi!" )

def main():
    ''' setting up 4 players and player info '''
    piles = Deck().deal( 4 )
    p1 = HumanPlayer( 'p1', piles[0] )
    p2 = MonkeyCPU( 'p2', piles[1] )
    p3 = MonkeyCPU( 'p3', piles[2] )
    p4 = MonkeyCPU( 'p4', piles[3] )

    players = [p1, p2, p3, p4]
    main_loop(players, printing_on=True, show_cpu=True)

if __name__ == '__main__':
    main()
