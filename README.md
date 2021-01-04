# bhabhi
Python project using reinforcement learning to create an AI for a card
game called Bhabhi. Specifically, Q-Learning is used, which is a reinforcement
learning algorithm.
#### More information on QLearning:
https://en.wikipedia.org/wiki/Q-learning
## Description
There are multiple player types, they all extend from Player which is an
abstract class:
1. HumanPlayer - Controlled by User, does not work with GUI, mostly just exists
   for testing
1. MonkeyCPU - Makes random move
1. HumanLikeCPU - More complex player which plays more like a Human would
   play, by always playing high card.
1. QLearner - Player used to 'train' QLearnAI by using QLearning algorithm and
   filling up the QTable with its respective values over thousands of games
1. QLearnAI - Fully trained AI

Using the python programs below, you can make any assortment of players above
play a game, or many series of games.

## Usage:
#### Multiple games
```
python bhabhi.py
```
#### GUI display for a single game
Note: this does not work with HumanPlayer
```
python bhabhiGui.py
```

## Files
card_pics/ directory contains all pictures of cards for the GUI

advanced_players.py, players.py, qlearn.py contain all of the Player classes,
e.g. HumanPlayer, QLearnAI, etc.

cards.py includes Hand, and Deck objects which are essentially sets of cards
with methods like pop, shuffle, etc.

bhabhi.py and bhabhiGui.py are the main programs where game logic occurs.

qtable.csv is where the most recent qtable is saved when running the QLearning
algorithm using the QLearner Player.

## Results
After running 5000 games against MonkeyCPUs to test:
* The AI trained with the QLearning Algorithm won 4339 times (86.8% win rate)
* The HumanLikeCPU Player with hard-coded instructions won 3470 times (69.4% win rate)

I consider this an overall success
