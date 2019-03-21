'''
This script will ask for a target number of steps to reach, then calculate the smallest number required to reach that number.
A step is defined as "breaking a number into it's individual digits, and multiplying them together to get a new number".
The steps stop as soon as a single-digit number is reached.

Written by Jye Horan, inspired by Matt Parker via a numberphile video!

Version 1.1 - Made some slight changes to final output for clarity.
'''

import os
from time import sleep
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
answer = ['', 'Y', 'YE', 'YES', 'YEP', 'YEAH', 'N', 'NO', 'NOPE', 'NUH', 'GO AWAY']

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

def findSmallest(n):
	testNumber = 1
	targetHit = False
	target = n + 1
	numberList = []
	while targetHit == False:
		numberList = numberCheck(testNumber)
		if len(numberList) == target:
			targetHit = True
			print(str(numberList))
			print(str(numberList[0]) + ' is the smallest number that will cause ' + str(len(numberList) - 1) + ' steps!')
		else:
			testNumber = testNumber + 1

count = int(input('How many steps do you want to find? '))
if count > 7:
	sure = input('This is going to take a REALLY long time, are you sure you want to start? (Y/N)')
	if sure.upper() == answer[0] or sure.upper() == answer[1] or sure.upper() == answer[2] or sure.upper() == answer[3] or sure.upper() == answer[4] or sure.upper() == answer[5]:
		print('Okay, here goes!')
		findSmallest(count)
		input('Press enter to close.')
	elif sure.upper() == answer[6] or sure.upper() == answer[7] or sure.upper() == answer[8] or sure.upper() == answer[9] or sure.upper() == answer[10]:
		print('Oh thank goodness, that was going to hurt...')
		input('Press enter to close.')
	else:
		print('I\'m not sure what you mean but I\'m scared so I\'m shutting down, bye!')
		input('Press enter to close.')
else:
	findSmallest(count)