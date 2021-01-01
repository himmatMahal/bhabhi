import pygame
from cards import Hand, GUIDeck
from random import shuffle
from random import randint
import math
from copy import copy
from players import HumanPlayer, MonkeyCPU, HumanLikeCPUI, HumanLikeCPUII
from players import Player
from advanced_players import QLearnAI


class BhabhiGUI:

    WIDTH = 750
    HEIGHT = 600

    RATE = 5

    BG = (6,87,0)
    NORTH = (250, 5)
    SOUTH = (250, 525)
    EAST = (575, 250)
    WEST = (25, 250)
    CENTER = (200, 275)

    def __init__(self, all_players, loser_count):
        ''' all_players: list of players
            loser_count: empty dictionary which keeps score
            screen: pygame window for game
            clock: clock for game '''
        self.all_players = all_players
        self.loser_count = loser_count

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("BHABHI!")
        self.clock = pygame.time.Clock()

    def run_game(self):
        ''' all complicated game logic occurs here '''
        self.deal_cards()
        players = copy(self.all_players)

        garbage = Hand([])
        table_cards = Hand([])
        starter = -1
        num_live_players = len(players)

        pygame_on = True
        # main loop for game
        while pygame_on and num_live_players>1:

            if num_live_players>1:
                i=0
                if i<1:
                    for player in players:
                        for card in player.hand.cards:
                            if card[0]=='Spades' and card[1]=='A':
                                starter = players.index( player )
                                table_cards.pick_up_card(
                                    player.hand.pop_card(card)
                                )
                                i+=1
                                self.update(
                                    table_cards,
                                    self.all_players,
                                    players,
                                    starter
                                )
                # remaining players play their ace after first player
                else:
                    # next player in rotation plays
                    table_cards.pick_up_card(
                        players[(starter + i) % num_live_players].bhabhi_move(
                            table_cards
                        )
                    )
                    self.update(
                        table_cards,
                        self.all_players,
                        players,
                        starter
                    )

                    if show_every_round:
                        self.print_status(
                            players[(starter+i)%num_live_players], table_cards
                        )

                    i+=1


            # dump all cards after first round
            garbage.pick_up_cards( table_cards.pop_all_cards() )

            # central loop for game
            j=1
            winners = []
            while num_live_players>1:

                self.update(
                    table_cards,
                    self.all_players,
                    players,
                    starter
                )

                # begin a single round
                round_end_early = False
                i=0
                next_starting_player = players[starter]
                while i<num_live_players and (not round_end_early):

                    # player takes turn
                    current = players[(starter + i) % num_live_players]

                    table_cards.pick_up_card( current.bhabhi_move(table_cards) )

                    self.update(
                        table_cards,
                        self.all_players,
                        players,
                        starter
                    )

                    # checking game status
                    if not (i==0):
                        if table_cards.top_card_is_diffsuit():
                            round_end_early = True
                        elif table_cards.top_card_is_highest():
                            # checking if player who just played threw the highest card
                            next_starting_player = current
                    i+=1
                # loop breaks once everyone played, or round ended early (pick up)

                if round_end_early:
                    next_starting_player.pick_up_cards(
                        table_cards.pop_all_cards()
                    )
                else:
                    garbage.pick_up_cards( table_cards.pop_all_cards() )

                # case where next_starting_player must pick from garbage since
                # they start the next round
                if next_starting_player.hand.get_card_count() < 1:
                    garbage.shuffle_cards()
                    next_starting_player.pick_up_card( garbage.pop_card(1) )

                # removing winners:
                next_round_players = []
                for player in players:
                    if player.hand.get_card_count() >= 1:
                        next_round_players.append(player)
                    else:
                        winners.append(player)

                players.clear()
                players = next_round_players
                num_live_players = len(players)

                # setting up starting player for next round
                starter = players.index( next_starting_player )
                j+=1

                self.update(table_cards, self.all_players, players, starter)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame_on=False

            bhabhi = players[0].name
            if bhabhi in self.loser_count:
                self.loser_count[bhabhi] += 1
            else:
                self.loser_count[bhabhi] = 1

        self.display_loser()

    def display_table_cards(self, table):
        i=0
        for card in table.cards:
            pos = (self.CENTER[0] + 60*i, self.CENTER[1])
            self.screen.blit(card[3], pos)
            i+=1
        pygame.display.update()

    def redraw_game_setup(self, all_players, players):
        # rendering player names and fonts for display
        self.screen.fill(self.BG)
        my_font = pygame.font.SysFont('comicsans', 20, bold=True)

        text = [player.name + "-WON" for player in all_players]
        for i in range(4):
            for j in range(len(players)):
                if all_players[i].name == players[j].name:
                    text[i] = players[j].name+"-"+str(
                        players[j].hand.get_card_count()
                    )

        player_text = [ my_font.render(ptext,True,(255,255,255))
                        for ptext in text ]
        positions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        for i in range(4):
            self.screen.blit(player_text[i], positions[i])

        pygame.display.update()

    def deal_cards(self):
        split_decks = GUIDeck().deal(len(self.all_players))
        i=0
        for player in self.all_players:
            player.set_hand( split_decks[i] )
            i+=1

    def update(self, table, all_players, players, starter):
        pygame.event.pump()
        self.clock.tick(self.RATE)
        self.redraw_game_setup(all_players, players)
        self.display_table_cards(table)

        if isinstance(starter, int):
            if starter>=0:
                positions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
                pos = (positions[starter][0], positions[starter][1]+25)
                my_font = pygame.font.SysFont('comicsans', 20, bold=True)
                txt = my_font.render('Starter',True,(255,100,100))
                self.screen.blit(txt, pos)
                #highlight starter
        if isinstance(starter, Player):
            start_idx = players.index(starter)
            if start_idx>=0:
                positions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
                pos = (positions[start_idx][0], positions[start_idx][1]+25)
                my_font = pygame.font.SysFont('comicsans', 20, bold=True)
                txt = my_font.render('Starter',True,(255,100,100))
                self.screen.blit(txt, pos)

        pygame.display.update()

    def display_loser(self):
        quit = False

        lost = None
        for loser in self.loser_count:
            lost = loser

        while not quit:
            self.screen.fill(self.BG)
            my_font = pygame.font.SysFont('comicsans', 35, bold=True)
            text = my_font.render(f"{lost} is the Bhabhi!", True, (255,255,255))
            self.screen.blit(text, (self.WIDTH//4, self.HEIGHT//2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit=True



def get_players():
    players = [None for x in range(4)]
    names = ["p1", "p2", "p3", "p4"]
    for i in range(4):
        selection = -1
        while selection not in [1,2,3,4]:
            print("Select the type for player "+str(i+1))
            print(" 1 - QLearnAI\n 2 - MonkeyCPU\n 3 - HumanLikeCPUI\n"+
                  " 4 - HumanLikeCPUII\n")
            selection = int(input())

        name = ""
        while len(name) not in list(range(2,30)):
            print("Type the players name or leave blank (p"+str(i+1)+" default)")
            name = str(input())
            if len(name)==0:
                name = names[i]

        names[i] = name

        if selection==1:
            players[i] = QLearnAI(name=names[i])
        elif selection==2:
            players[i] = MonkeyCPU(name=names[i])
        elif selection==3:
            players[i] = HumanLikeCPUI(name=names[i])
        else:
            players[i] = HumanLikeCPUII(name=names[i])

    return players

def main():
    all_players = get_players()
    loser_count = {}
    game = BhabhiGUI( all_players, loser_count )
    game.run_game()


if __name__ == '__main__':
    main()
