import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Raffle Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Raffle Minigame for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.4"

configFile = "config.json"
settings = {}
startTime = 0
bettingTime = 0
isBettingOpened = False
userList = []
pot = 0

def ScriptToggled(state):
	return

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!raffle",
			"startCountdown" : 1800,
			"betCountdown" : 300,
			"permission": "Everyone",
			"minBet" : 1,
			"maxBet" : 100,
			"startedResponse" : "Raffle started! You can bet by typing $command <$min - $max>",
			"userBettedResponse" : "User betted $bet in raffle!",
			"userWonResponse" : "Raffle: $user won $win $currency!",
			"noBetsResponse" : "Raffle: nobody betted!",
			"notOpenedResponse" : "Raffle isn't opened right now!",
			"alreadyBettedResponse" : "$user, you are already betted in the raffle!",
			"wrongAmmountResponse" : "$user you can bet between $min - $max $currency. Currently you have $points $currency.",
		}
	return

def Execute(data):
	global userList, pot

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		bet = 0

		if (data.GetParamCount() == 2):
			try: 
				bet = int(data.GetParam(1))
			except:
				if data.GetParam(1) == 'all': 
					bet = points

		if not isBettingOpened:
			outputMessage = settings["notOpenedResponse"]
		elif (bet > points) or (bet < settings["minBet"]) or (bet > settings["maxBet"]):
			outputMessage = settings["wrongAmmountResponse"] 
		elif username in userList:
			outputMessage = settings["alreadyBettedResponse"] 
		else:
			Parent.RemovePoints(userId, username, bet)
			pot += bet
			userList.append([userId, username, pot])
			outputMessage = settings["userBettedResponse"]
	
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$bet", str(bet))
		outputMessage = outputMessage.replace("$min", str(settings["minBet"]))
		outputMessage = outputMessage.replace("$max", str(settings["maxBet"]))
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])

		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)
    return

def Tick():
	global startTime, bettingTime, isBettingOpened, userList, pot

	currentTime = time.time() 

	if(currentTime >= startTime):
		startTime = currentTime + settings["startCountdown"]
		bettingTime = currentTime + settings["betCountdown"]
		isBettingOpened = True

		outputMessage = settings["startedResponse"]
		outputMessage = outputMessage.replace("$min", str(settings["minBet"]))
		outputMessage = outputMessage.replace("$max", str(settings["maxBet"]))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])
		
		Parent.SendStreamMessage(outputMessage)

	if(currentTime >= bettingTime) and isBettingOpened:	
		if pot > 0:
			winnerNumber = Parent.GetRandom(1, pot + 1)

		for	user in userList:	
			if user[2] >= winnerNumber:
				Parent.AddPoints(user[0], user[1], pot)

				outputMessage = settings["userWonResponse"]
				outputMessage = outputMessage.replace("$user", user[1])
				outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
				outputMessage = outputMessage.replace("$win", str(pot))
				break
		else:
			outputMessage = settings["noBetsResponse"]

		isBettingOpened = False	
		userList = []
		pot = 0

		Parent.SendStreamMessage(outputMessage)
	return