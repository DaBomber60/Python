'''THis application will simulate rolling dice in DND, using standard notation.
That is to say, it will ask "what do you want to roll", and user can enter 1d20+4 for example
the system will then attempt to simulate a 20 sided die being rolled, and then add the appropriate value.

Eventually this will be used as the behind the scenes for a GUI based dice roller, to be used at a DND session.

Author: Jye Horan
Written for Python 3.7'''

from random import randint
import os
from time import sleep
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
integers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["d"]
functions = ["+"]
dice = ["4", "6", "8", "10", "12", "20", "100"]
legalCharacters = integers + letters + functions

invalid = "This is an invalid roll, press enter to try again..."

multi = 1
die = 0
modifier = 0
inputClean = True
reroll = False
rollTotal = 0

def roller(die):
	roll = randint(1, die)
	return roll

def multiRoller(multi, die):
	roll = 0
	for i in range(multi):
		roll += roller(die)
	return roll

def fullRoller(multi, die, modifier):
	roll = multiRoller(multi, die) + modifier
	return roll

def inputGetDie(text):
	global inputClean
	global die
	text = text.lower()
	text = "3" + text + "3"
	test = ""
	testNext = ""
	testPrevious = ""
	dCount = text.count("d")
	plusCount = text.count("+")
	for i in range(1, len(text) - 1):
		if text[i] not in legalCharacters:
			inputClean = False
			break
		elif text[i] in integers and "+" not in text:
			test = text[int(i) - 1] + text[int(i)] + text[int(i) + 1]
			testPrevious = text[int(i) - 2]
			if test in dice and testPrevious == "d":
				die = int(test)
			else:
				test = text[int(i) - 1] + text[int(i)]
				testPrevious = text[int(i) - 2]
				if test in dice and testPrevious == "d":
					die = int(test)
				else:
					test = text[int(i)]
					testPrevious = text[int(i) - 1]
					if test in dice and testPrevious == "d":
						die = int(test)
		elif text[i] == "+":
			break
		elif text[i] in integers and "+" in text:
			test = text[int(i) - 1] + text[int(i)] + text[int(i) + 1]
			testNext = text[int(i) + 2]
			testPrevious = text[int(i) - 2]
			if test in dice and testNext == "+" and testPrevious == "d":
				die = 100
			else:
				test = text[int(i) - 1] + text[int(i)]
				testNext = text[int(i) + 1]
				testPrevious = text[int(i) - 2]
				if test in dice and testNext == "+" and testPrevious == "d":
					die = int(test)
				else:
					test = text[int(i)]
					testNext = text[int(i) + 1]
					testPrevious = text[int(i) - 1]
					if test in dice and testNext == "+" and testPrevious == "d":
						die = int(test)
	if die == 0:
		inputClean = False

def inputGetMulti(text):
	global inputClean
	global multi
	multiString = ""
	text = text.lower()
	dCount = text.count("d")
	plusCount = text.count("+")
	beforeDCount = 0
	for i in range(len(text)):
		if text[i] not in legalCharacters:
			inputClean = False
			break
		elif text[i] == "d":
			break
		else:
			beforeDCount += 1
	for i in range(beforeDCount):
		multiString += text[i]
	if len(multiString) > 0:
		multi = int(multiString)
	else:
		multi = 1

def inputGetModifier(text):
	global inputClean
	global modifier
	modifierString = ""
	text = text.lower()
	dCount = text.count("d")
	plusCount = text.count("+")
	beforePlusCount = 1
	if "+" not in text:
		modifier = 0
	else:
		for i in range(len(text)):
			if text[i] not in legalCharacters:
				inputClean = False
				break
			elif text[i] == "+":
				break
			else:
				beforePlusCount += 1
		if beforePlusCount == len(text):
			modifier = 0
		else:
			for i in range(beforePlusCount, len(text)):
				modifierString += text[i]
			modifier = int(modifierString)

def inputSanitiser(text):
	global inputClean
	text = text.lower()
	dCount = text.count("d")
	plusCount = text.count("+")
	beforePlusCount = 0
	beforeDCount = 0
	if "d" in text and dCount == 1 and plusCount <= 1:
		if "+" in text:
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif text[i] == "+":
					break
				else:
					beforePlusCount += 1
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif text[i] == "d":
					break
				else:
					beforeDCount += 1
			if beforeDCount > beforePlusCount or beforePlusCount - beforeDCount == 1:
				inputClean = False
		else:
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif text[i] == "d":
					break
				else:
					beforeDCount += 1
			if beforeDCount + 1 >= len(text):
				input = False
	else:
		inputClean = False

def requestRoll():
	roll = input("Please enter your dice roll: ")
	return roll

def requestRerollBadRoll():
	global inputClean
	global reroll
	again = input("You have entered a bad roll, would you like to try again? Y/N: ")
	again = again.lower()
	if len(again) == 0:
		inputClean = True
		reroll = True
	elif again[0] == "y":
		inputClean = True
		reroll = True
	elif again[0] == "n":
		inputClean = True
		reroll = False
	else:
		requestRerollBadAnswer()
		
def requestRerollBadAnswer():
	global inputClean
	global reroll
	again = input("I don't understand, would you like to try again? Y/N: ")
	again = again.lower()
	if len(again) == 0:
		inputClean = True
		reroll = True
	elif again[0] == "y":
		inputClean = True
		reroll = True
	elif again[0] == "n":
		inputClean = True
		reroll = False
	else:
		requestRerollBadAnswer()
		
def requestRerollGoodRoll():
	global inputClean
	global reroll
	again = input("Would you like to make another roll? Y/N: ")
	again = again.lower()
	if len(again) == 0:
		inputClean = True
		reroll = True
	elif again[0] == "y":
		inputClean = True
		reroll = True
	elif again[0] == "n":
		inputClean = True
		reroll = False
	else:
		requestRerollBadAnswer()

def rollProcess():
	global rollTotal
	initialise()
	cls()
	roll = requestRoll()
	score = 0
	inputGetDie(roll)
	inputGetModifier(roll)
	inputGetMulti(roll)
	inputSanitiser(roll)
	if inputClean == True:
		score = fullRoller(multi, die, modifier)
		rollTotal += score
		sleep(.5)
		print("Rolling...")
		sleep(1)
		print("The total of your roll is " + str(score) + "!")
		sleep(2)
		requestRerollGoodRoll()
	else:
		requestRerollBadRoll()
	if reroll == True:
		rollProcess()
	else:
		print("Okay, have fun doing what you're doing!")
		sleep(.5)
		print("The total of all your rolls was " + str(rollTotal) + ", I hope it served you well!")
		sleep(1.5)
		input("Thank you for using Jye's dice roller, press enter to quit...")
	
def initialise():
	global die
	global multi
	global modifier
	multi = 1
	die = 0
	modifier = 0

rollProcess()

'''#Junk lines used for testing
#testRoll = input("Enter a roll: ")
testRoll = "d22"
#print(testRoll)
inputGetDie(testRoll)
print("Die is", die)
print(inputClean)
#print("Multi is", inputGetMulti(testRoll))
#print("Modifier is", inputGetModifier(testRoll))
#inputSanitiser(testRoll)
#print(inputClean)
#input("Scipt has been run, press enter to close...")'''