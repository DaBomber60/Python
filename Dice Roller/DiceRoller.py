'''This application will simulate rolling dice in DND, using standard notation.
That is to say, it will ask "what do you want to roll", and user can enter 1d20+4 for example
the system will then attempt to simulate a 20 sided die being rolled, and then add the appropriate value.

Eventually this will be used as the behind the scenes for a GUI based dice roller, to be used at a DND session.

Author: Jye Horan
Written for Python 3.7'''

'''Changelog:
Version 1.2: added the ability to subtract after the roll, and edited the messages sent back to adapt to this change.
Version 1.3: added in reactions to maximum and minimum roll values, as well as a secret 1% chance message on a single d20 crit hit/miss
'''

from random import randint
import os
from time import sleep
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

integers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ["d"]
functions = ["+", "-"]
dice = ["4", "6", "8", "10", "12", "20", "100"]
legalCharacters = integers + letters + functions

multi = 1
die = 0
modifier = 0
inputClean = True
reroll = False
rollTotal = 0
totalRollList = []
rollList = []
functionWord = ""
bonusPenalty = ""
modifierAbsolute = 0

def roller(die):
	roll = randint(1, die)
	return roll

def multiRoller(multi, die):
	roll = 0
	for i in range(multi):
		rolled = roller(die)
		roll += rolled
		rollList.append(str(rolled))
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
	for i in range(1, len(text) - 1):
		if text[i] not in legalCharacters:
			inputClean = False
			break
		elif text[i] in integers and "+" or "-" not in text:
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
		elif text[i] == "-":
			break
		elif text[i] in integers and "+" or "-" in text:
			test = text[int(i) - 1] + text[int(i)] + text[int(i) + 1]
			testNext = text[int(i) + 2]
			testPrevious = text[int(i) - 2]
			if test in dice and testNext == "+" or "-" and testPrevious == "d":
				die = 100
			else:
				test = text[int(i) - 1] + text[int(i)]
				testNext = text[int(i) + 1]
				testPrevious = text[int(i) - 2]
				if test in dice and testNext == "+" or "-" and testPrevious == "d":
					die = int(test)
				else:
					test = text[int(i)]
					testNext = text[int(i) + 1]
					testPrevious = text[int(i) - 1]
					if test in dice and testNext == "+" or "-" and testPrevious == "d":
						die = int(test)
	if die == 0:
		inputClean = False

def inputGetMulti(text):
	global inputClean
	global multi
	multiString = ""
	text = text.lower()
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
	beforeFunctionCount = 1
	if "+" not in text and "-" not in text:
		modifier = 0
	else:
		for i in range(len(text)):
			if text[i] not in legalCharacters:
				inputClean = False
				break
			elif text[i] == "+":
				break
			elif text[i] == "-":
				break
			else:
				beforeFunctionCount += 1
		if beforeFunctionCount == len(text):
			modifier = 0
		else:
			for i in range(beforeFunctionCount, len(text)):
				modifierString += text[i]
			modifier = int(modifierString)
	getModifierFunction(text)

def inputSanitiser(text):
	global inputClean
	text = text.lower()
	dCount = text.count("d")
	plusCount = text.count("+")
	minusCount = text.count("-")
	functionCount = plusCount + minusCount
	beforeFunctionCount = 0
	beforeDCount = 0
	if "d" in text and dCount == 1 and functionCount <= 1:
		if "+" in text or "-" in text:
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif text[i] == "+":
					break
				elif text[i] == "-":
					break
				else:
					beforeFunctionCount += 1
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif text[i] == "d":
					break
				else:
					beforeDCount += 1
			if beforeDCount > beforeFunctionCount or beforeFunctionCount - beforeDCount == 1:
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
	global totalRollList
	initialise()
	cls()
	roll = requestRoll()
	score = 0
	inputSanitiser(roll)
	rollCheck(roll)
	if inputClean == True:
		score = fullRoller(multi, die, modifier)
		rollTotal += score
		totalRollList.append(str(roll) + " = " + str(score))
		sleep(.5)
		print("Rolling...")
		sleep(1)
		if multi == 1 and modifier == 0:
			print("Your die landed on " + ', '.join(rollList) + ".")
			if die == 20:
				if score == 1:
					sleep(1)
					print("Critical miss!")
					sleep(1)
				elif score == 20:
					sleep(1)
					print("Critical hit!")
					sleep(1)
			else:
				if score == 1:
					sleep(1)
					print("Oof")
					sleep(1)
				elif score == die:
					sleep(1)
					print("Nice!")
					sleep(1)
		elif multi == 1:
			print("Your die landed on " + ', '.join(rollList) + ".")
			if die == 20:
				if (score - modifier) == 1:
					sleep(1)
					print("Critical miss!")
					luck = randint(0,100)
					sleep(1)
					if luck == 42:
						print("I seriously hope that was an initiative roll...")
						sleep(1)
				elif (score - modifier) == 20:
					sleep(1)
					print("Critical hit!")
					luck = randint(0,100)
					sleep(1)
					if luck == 42:
						print("I seriously hope that wasn't wasted on an initiative roll...")
						sleep(1)
			else:
				if (score - modifier) == 1:
					sleep(1)
					print("Oof")
					sleep(1)
				elif (score - modifier) == die:
					sleep(1)
					print("Nice!")
					sleep(1)
		else:
			print("The rolls were: " + ', '.join(rollList) + ".")
		if multi == 1 and modifier == 0:
			pass
		elif modifier == 0:
			print("The total of your dice roll is " + str(score) + "!")
		else:
			print("The total of your dice roll is " + str(score - modifier) + ", " + functionWord + " your " + bonusPenalty + " of " + str(modifierAbsolute) + ", makes " + str(score) + "!")
		sleep(2)
		requestRerollGoodRoll()
	else:
		requestRerollBadRoll()
	if reroll == True:
		rollProcess()
	else:
		print("Okay, have fun doing what you're doing!")
		sleep(.5)
		print("The list of all your rolls is:")
		print(totalRollList)
		sleep(.5)
		print("The total of all your rolls was " + str(rollTotal) + ", I hope it served you well!")
		sleep(1.5)
		input("Thank you for using Jye's dice roller, press enter to quit...")
	
def initialise():
	global multi
	global die
	global modifier
	global inputClean
	global reroll
	global rollList
	global functionWord
	global bonusPenalty
	global modifierAbsolute
	multi = 1
	die = 0
	modifier = 0
	inputClean = True
	reroll = False
	rollList = []
	functionWord = ""
	bonusPenalty = ""
	modifierAbsolute = 0
	
def rollCheck(roll):
	if inputClean == True:
		inputGetDie(roll)
		inputGetModifier(roll)
		inputGetMulti(roll)
		
def getModifierFunction(text):
	global modifier
	global modifierAbsolute
	global functionWord
	global bonusPenalty
	if "-" in text:
		modifier *= (-1)
		modifierAbsolute = abs(modifier)
		functionWord = "minus"
		bonusPenalty = "penalty"
	elif "+" in text:
		modifierAbsolute = abs(modifier)
		functionWord = "plus"
		bonusPenalty = "bonus"
		
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