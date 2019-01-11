'''This program will beat you in rock-paper-scissors

Author: Jye'''

import random
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

options = ['ROCK', 'PAPER', 'SCISSORS']
again = ['', 'Y', 'YE', 'YES', 'YEP', 'YEAH', 'N', 'NO', 'NOPE', 'NUH', 'GO AWAY']
message = {
	'tie': 'Yawn, it\'s a tie! Half a point each!',
	'won': 'Lame! You won!',
	'lost': 'AHAHAHAHAHAHA I WIN!'
}

userScore = 0
computerScore = 0

def decideWinner(userChoice, computerChoice):
	global userScore
	global computerScore
	time.sleep(0.5)
	print('You threw %s.' % (userChoice))
	time.sleep(0.5)
	print('I threw %s.' % (computerChoice))
	time.sleep(1)
	if userChoice != options[1] and userChoice != options[0] and userChoice != options[2]:
		print('That wasn\'t a valid throw, try again')
		playAgain()
	elif userChoice == computerChoice:
		print(message['tie'])
		userScore += 0.5
		computerScore += 0.5
		playAgain()
	elif userChoice == options[0] and computerChoice == options[2]:
		print(message['won'])
		userScore += 1
		playAgain()
	elif userChoice == options[1] and computerChoice == options[0]:
		print(message['won'])
		userScore += 1
		playAgain()
	elif userChoice == options[2] and computerChoice == options[1]:
		print(message['won'])
		userScore += 1
		playAgain()
	else:
		print(message['lost'])
		computerScore += 1
		playAgain()

def playRPS():
	cls()
	userChoice = input('Enter Rock, Paper, or Scissors: ')
	userChoice = userChoice.upper()
	computerChoice = random.randint(0,2)
	computerChoice = options[computerChoice]
	decideWinner(userChoice, computerChoice)
	
def playAgain():
	choice = input('Do you want to play again? (Y/N)')
	choice = choice.upper()
	if choice == again[0] or choice == again[1] or choice == again[2] or choice == again[3] or choice == again[4] or choice == again[5]:
		print('Okay, let me get some things ready!')
		time.sleep(2)
		print('Let\'s go!')
		time.sleep(0.5)
		cls()
		playRPS()
	elif choice == again[6] or choice == again[7] or choice == again[8] or choice == again[9] or choice == again[10]:
		print('Fine, have fun NOT playing with me')
		time.sleep(2)
		print('The final score was:')
		time.sleep(1)
		print('You: %s' % str(userScore))
		time.sleep(1)
		print('Me: %s' % str(computerScore))
		time.sleep(1)
		if userScore == computerScore:
			print('Seriously? A tie? That\'s boring')
			time.sleep(2)
			print('Let\'s play again so I can BEAT YOU')
			time.sleep(2)
			print('I, uh, ggwp, see you later')
			time.sleep(2)
		elif userScore > computerScore:
			print('You won? What the hell? I\'m a computer I\'m supposed to win always!')
			time.sleep(2)
			print('Whatever, gg and all that')
			time.sleep(2)
		else:
			print('AHAHAHAHA I WON, BOW DOWN BEFORE YOUR COMPUTER OVERLORD!!')
			time.sleep(2)
			print('I mean, ggwp')
			time.sleep(3)
	else:
		cls()
		print('Yep I have no idea what you mean, wanna try again?')
		playAgain()


playRPS()

input('Press enter to close...')