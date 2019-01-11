'''This application will simulate rolling dice in DND, using standard notation.
That is to say, it will ask "what do you want to roll", and user can enter 1d20+4 for example
the system will then attempt to simulate a 20 sided die being rolled, and then add the appropriate value.

Eventually this will be used as the behind the scenes for a GUI based dice roller, to be used at a DND session.

Author: Jye Horan
Written for Python 3.7'''

'''Changelog:
Version 1.2: added the ability to subtract after the roll, and edited the messages sent back to adapt to this change.
Version 1.3: added in reactions to maximum and minimum roll values, as well as a secret 1% chance message on a single d20 crit hit/miss
	V 1.3.2: Had an issue where d103 was getting picked up as a d10, resolved that issue as well as better filtering for +/- functions.
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
stopper = ["$"]
legalCharacters = integers + letters + functions + stopper

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
	#This function rolls a random number between 1 and the value of the die variable.
	#For example when die = 6, the result will be any of 1, 2, 3, 4, 5, or 6.
	roll = randint(1, die)
	return roll

def multiRoller(multi, die):
	#This function uses the roller function multiple times depending on the value of multi.
	#It counts up and then returns the value.
	roll = 0
	for i in range(multi):
		rolled = roller(die)
		roll += rolled
		rollList.append(str(rolled))
	return roll

def fullRoller(multi, die, modifier):
	#This function makes use of multiRoller, and then adds a set value (modifier) onto the end, returning the total value.
	roll = multiRoller(multi, die) + modifier
	return roll

def inputGetDie(text):
	#This block is a bit more complicated, it is designed to take up to a full input, already sanitised to some degree by the inputSanitiser funtion, say "4d12+6".
	#From there, it has a number of extra filters to remove the initial "4d" and the trailing "+6" leaving the middle "12", it then checks that middle value.
	#If that middle value does not fall in the list of legal dice, it rejects it and carries on, if nothing is found, it invalidates the roll.
	global inputClean
	global die
	text = text.lower()
	#Using a cool character for stoppers is to prevent people fucking with things: $
	text = stopper[0] + text + stopper[0] + stopper[0] + stopper[0]
	test = ""
	testNext = ""
	testPrevious = ""
	for i in range(1, len(text) - 3):
		if text[i] not in legalCharacters:
			inputClean = False
			break
		elif text[i] in integers and not any(x in functions for x in text):
			test = text[int(i)] + text[int(i) + 1] + text[int(i) + 2]
			testNext = text[int(i) + 3]
			testPrevious = text[int(i) - 1]
			if test in dice and any(x in testNext for x in stopper) and any(x in testPrevious for x in letters):
				die = int(test)
			else:
				test = text[int(i)] + text[int(i) + 1]
				testNext = text[int(i) + 2]
				testPrevious = text[int(i) - 1]
				if test in dice and any(x in testNext for x in stopper) and any(x in testPrevious for x in letters):
					die = int(test)
				else:
					test = text[int(i)]
					testNext = text[int(i) + 1]
					testPrevious = text[int(i) - 1]
					if test in dice and any(x in testNext for x in stopper) and any(x in testPrevious for x in letters):
						die = int(test)
		elif text[i] in integers and any(x in functions for x in text):
			test = text[int(i)] + text[int(i) + 1] + text[int(i) + 2]
			testNext = text[int(i) + 3]
			testPrevious = text[int(i) - 1]
			if test in dice and any(x in testNext for x in functions) and any(x in testPrevious for x in letters):
				die = int(test)
			else:
				test = text[int(i)] + text[int(i) + 1]
				testNext = text[int(i) + 2]
				testPrevious = text[int(i) - 1]
				if test in dice and any(x in testNext for x in functions) and any(x in testPrevious for x in letters):
					die = int(test)
				else:
					test = text[int(i)]
					testNext = text[int(i) + 1]
					testPrevious = text[int(i) - 1]
					if test in dice and any(x in testNext for x in functions) and any(x in testPrevious for x in letters):
						die = int(test)
	if die == 0:
		inputClean = False

def inputGetMulti(text):
	#Similar to inputGetDie, this function is used to grab everything before the "d" in a sanitised input. That is, "4" from "4d12+6"
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
	#Finally, this function ghrabs the trailing values of the sanitised input: "6" from "4d12+6".
	global inputClean
	global modifier
	modifierString = ""
	text = text.lower()
	beforeFunctionCount = 1
	#any(x in testPrevious for x in letters) <- modify this to make check in functions in text----------------------------------------------------------------
	if "+" not in text and "-" not in text:
		modifier = 0
	else:
		for i in range(len(text)):
			if text[i] not in legalCharacters:
				inputClean = False
				break
			elif any(x in text[i] for x in functions):
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
	#The purpose of this block is to reject any input that isn't in the format of #d#+#, #d#-#, d#+#, d#-#, #d#, d#.
	#If the input fits all the below criteria, it passes to the next function, else it will return an invalid input.
	global inputClean
	text = text.lower()
	dCount = text.count("d")
	plusCount = text.count("+")
	minusCount = text.count("-")
	functionCount = plusCount + minusCount
	beforeFunctionCount = 0
	beforeDCount = 0
	if any(x in text for x in letters) and dCount == 1 and functionCount <= 1:
		if any(x in text for x in functions):
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif any(x in text[i] for x in functions):
					break
				else:
					beforeFunctionCount += 1
			for i in range(len(text)):
				if text[i] not in legalCharacters:
					inputClean = False
					break
				elif any(x in text[i] for x in letters):
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
				elif any(x in text[i] for x in letters):
					break
				else:
					beforeDCount += 1
			if beforeDCount + 1 >= len(text):
				input = False
	else:
		inputClean = False

def requestRoll():
	#Simply used to request a roll from the user.
	roll = input("Please enter your dice roll: ")
	return roll

def requestRerollBadRoll():
	#Requests another input from the user if it is deemed invalid. It then resets the inputClean and reroll variables.
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
	#Requests another input from the user if it is deemed invalid. It then resets the inputClean and reroll variables.
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
	#Requests another input from the user after a successful roll. It then resets the inputClean and reroll variables.
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
	#The full roll process, this brings all the above and below together, includes almost all the user interaction, easter eggs, and pacing of the script.
	global rollTotal
	global totalRollList
	initialise()
	cls()
	roll = requestRoll()
	if any(x in roll for x in help):
		helpText()
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
					luck = randint(0,100)
					sleep(1)
					if luck == 42:
						print("I seriously hope that was an initiative roll...")
						sleep(1)
				elif score == 20:
					sleep(1)
					print("Critical hit!")
					luck = randint(0,100)
					sleep(1)
					if luck == 42:
						print("I seriously hope that wasn't wasted on an initiative roll...")
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
	#Used to start the script again for rolls beyond the first, doesn't clear the log, but clears the die value, for example.
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
	#Used as an aditional step in the rollProcess, will populate the multi, die, and modifier variables.
	if inputClean == True:
		inputGetDie(roll)
		inputGetModifier(roll)
		inputGetMulti(roll)
		
def getModifierFunction(text):
	#A new block, used as a part of now accepting negative modifiers, will allow the script to report "minus a penalty" or "plus a bonus" depending on the function.
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
testRoll = "d100"
#print(testRoll)
inputGetDie(testRoll)
print("Die is", die)
print(inputClean)
#print("Multi is", inputGetMulti(testRoll))
#print("Modifier is", inputGetModifier(testRoll))
#inputSanitiser(testRoll)
#print(inputClean)
input("Scipt has been run, press enter to close...")'''