'''
This script will ask for a target number of steps to reach, then calculate the smallest number required to reach that number.
A step is defined as "breaking a number into it's individual digits, and multiplying them together to get a new number".
The steps stop as soon as a single-digit number is reached.

Written by Jye Horan, inspired by Matt Parker via a numberphile video!

Version 1.1 - Made some slight changes to final output for clarity.
Version 1.2 - Made an option to test any number, added an option to print the currently tested number, and made the script skip testing number with both 2 and 5 OR 0.
'''

import os
from time import sleep
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
answer = ['', 'Y', 'YE', 'YES', 'YEP', 'YEAH', 'N', 'NO', 'NOPE', 'NUH', 'GO AWAY']
printing = 0
cls()

def numberCheck(n):
	numberList = []
	number = n
	numberList.append(number)
	while len(str(number)) > 1:
		number = multiplier(number)
		numberList.append(number)
	return(numberList)
	
def multiplier(n):
	digits = [int(i) for i in str(n)]
	result = 1
	for d in digits:
		result *= d
	return result

def findLeastSteps(n):
	testNumber = 1
	targetHit = False
	target = n + 1
	numberList = []
	while targetHit == False:
		if target == 1 or target == 2 or target == 3:
			if printing == 1:
				print('Currently testing: ' + str(testNumber), end="\r")
			numberList = numberCheck(testNumber)
			if len(numberList) == target:
				targetHit = True
				print(str(numberList) + '                          ')
				print(str(numberList[0]) + ' is the smallest number that will cause ' + str(len(numberList) - 1) + ' steps!')
			else:
				testNumber = testNumber + 1
		elif ('2' in str(testNumber) and '5' in str(testNumber)) or '0' in str(testNumber):
			testNumber = testNumber + 1
		else:
			if printing == 1:
				print('Currently testing: ' + str(testNumber), end="\r")
			numberList = numberCheck(testNumber)
			if len(numberList) == target:
				targetHit = True
				print(str(numberList) + '                          ')
				print(str(numberList[0]) + ' is the smallest number that will cause ' + str(len(numberList) - 1) + ' steps!')
			else:
				testNumber = testNumber + 1

def findSteps(n):
	numberList = []
	numberList = numberCheck(n)
	print(str(numberList))
	print(str(numberList[0]) + ' is completed in ' + str(len(numberList) - 1) + ' steps!')

def stepFinder():
	count = int(input('How many steps do you want to find? '))
	if count > 7:
		sure = input('This is going to take a REALLY long time, are you sure you want to start? (Y/N)')
		if sure.upper() == answer[0] or sure.upper() == answer[1] or sure.upper() == answer[2] or sure.upper() == answer[3] or sure.upper() == answer[4] or sure.upper() == answer[5]:
			print('Okay, here goes!')
			findLeastSteps(count)
			input('Press enter to close.')
		elif sure.upper() == answer[6] or sure.upper() == answer[7] or sure.upper() == answer[8] or sure.upper() == answer[9] or sure.upper() == answer[10]:
			print('Oh thank goodness, that was going to hurt...')
			input('Press enter to close.')
		else:
			print('I\'m not sure what you mean but I\'m scared so I\'m shutting down, bye!')
			input('Press enter to close.')
	else:
		findLeastSteps(count)
		
def stepTester():
	number = int(input('What number would you like to test? '))
	findSteps(number)	

def initial():
	print('Would you like to find the smallest number for a target step count, or find the steps of a specific number?')
	test = input('Enter 1 for target steps, or 2 to choose a number to test: ')
	if test == '1':
		printanswer = input('Would you like to print the currently tested number? ')
		if printanswer.upper() == answer[0] or printanswer.upper() == answer[1] or printanswer.upper() == answer[2] or printanswer.upper() == answer[3] or printanswer.upper() == answer[4] or printanswer.upper() == answer[5]:
			printing = 1
			cls()
			stepFinder()
		elif printanswer.upper() == answer[6] or printanswer.upper() == answer[7] or printanswer.upper() == answer[8] or printanswer.upper() == answer[9] or printanswer.upper() == answer[10]:
			cls()
			stepFinder()
		else:
			print('I\'m not sure what you mean, so I won\'t display the current number')
			input('Press enter to continue.')
			cls()
			stepFinder()
	elif test == '2':
		cls()
		stepTester()
	else:
		print('I\'m sorry, I didn\'t understand the choice, please try again.')
		sleep(1)
		initial()

initial()