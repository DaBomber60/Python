'''This program will beat you in rock-paper-scissors

Author: Jye'''

import random
import time

options = ['ROCK', 'PAPER', 'SCISSORS']
message = {
  'tie': 'Yawn, it\'s a tie!',
  'won': 'Yay! You won!',
  'lost': 'AHAHAHAHAHAHA I WIN!'
}

def decideWinner(userChoice, computerChoice):
  time.sleep(0.5)
  print 'You threw %s.' % (userChoice)
  time.sleep(0.5)
  print 'I threw %s.' % (computerChoice)
  time.sleep(1)
  if userChoice != options[1] and userChoice != options[0] and userChoice != options[2]:
    print 'That wasn\'t a valid throw, I WIN!!!'
  elif userChoice == computerChoice:
    print message['tie']
  elif userChoice == options[0] and computerChoice == options[2]:
    print message['won']
  elif userChoice == options[1] and computerChoice == options[0]:
    print message['won']
  elif userChoice == options[2] and computerChoice == options[1]:
    print message['won']
  else:
    print message['lost']

def playRPS():
  userChoice = raw_input('Enter Rock, Paper, or Scissors: ')
  userChoice = userChoice.upper()
  computerChoice = random.randint(0,2)
  computerChoice = options[computerChoice]
  decideWinner(userChoice, computerChoice)
  
playRPS()
  
raw_input('Press enter to close...')