import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Slots Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Slots Minigame game for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.5"

configFile = "config.json"
settings = {}
emotes = []
responses = []

def ScriptToggled(state):
	return

def Init():
	global responses, settings, emotes

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!slots",
			"permission": "Everyone",
			"useCustomCosts" : True,
			"costs": 1,
			"rewardTwoSeperated": 2,
			"rewardTwoSame": 4,
			"rewardJackpot": 25,
			"rewardSuperJackpot": 75,
			"emoteList": "HSWP, TwitchRPG, MorphinTime, duDudu, HumbleLife, PJSalt",
			"superEmote": "CurseLit",
			"responseLost": "$user pulls the lever [$slots] and looses $cost $currency LUL",
			"responseWonSmall": "$user pulls the lever [ $slots ] and wins (x$multiplier) $reward $currency! PogChamp",
			"responseWon": "$user pulls the lever [$slots] and wins (x$multiplier) $reward $currency! Kreygasm",
			"responseJackpot": "$user pulls the lever [$slots] and hits the Jackpot (x$multiplier) $reward $currency! Kappa",
			"responseSuperJackpot": "$user pulls the lever [$slots] and hits the SUPER JACKPOT (x$multiplier) $reward $currency! KappaPride",
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			"responseNotEnoughPoints": "$user you have only $points $currency to pull the lever."
		}

	emotes = settings["emoteList"].replace(" ","").split(",")
	emotes.append(settings["superEmote"].replace(" ",""))
	emotes = list(set(emotes))

	responses.extend([settings["rewardTwoSame"], settings["rewardJackpot"], settings["rewardSuperJackpot"]])
	try:
		for i in responses:
			int(i)
	except:
		MessageBox = ctypes.windll.user32.MessageBoxW
		MessageBox(0, u"Invalid values", u"Slots Script failed to load. The rewards are not numbers.", 0)
	return


def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)

		if settings["useCustomCosts"] and (data.GetParamCount() == 2):
			try: 
				costs = int(data.GetParam(1))
			except:
				if data.GetParam(1) == 'all': 
					costs = points
				else :
					costs = settings["costs"] 
		else:
			costs = settings["costs"]

		if (costs > Parent.GetPoints(userId)) or (costs < 1):
			outputMessage = settings["responseNotEnoughPoints"]
		elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
					cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
			else:
				outputMessage = ""
		else:
			Parent.RemovePoints(userId, username, costs)

			slot1 = emotes[Parent.GetRandom(0, len(emotes))]
			slot2 = emotes[Parent.GetRandom(0, len(emotes))]
			slot3 = emotes[Parent.GetRandom(0, len(emotes))]
			slots = [slot1, slot2, slot3]

			emotesString = " ".join(slots)
			reward = 0
			multiplier = 0

			if slots.count(slot1) == 3:
				if slot1 == settings["superEmote"]:
					outputMessage = (settings["responseSuperJackpot"])
					multiplier = settings["rewardSuperJackpot"]
					reward = costs * multiplier
					Parent.AddPoints(userId, username, reward)
				else:
					outputMessage = settings["responseJackpot"]
					multiplier = settings["rewardJackpot"]
					reward = costs * multiplier
					Parent.AddPoints(userId, username, reward)
			elif (slot1 == slot2 or slot2 == slot3):
				outputMessage = settings["responseWon"]
				multiplier = settings["rewardTwoSame"]
				reward = costs * multiplier
				Parent.AddPoints(userId, username, reward)
			elif (slot1 == slot3):
				outputMessage = settings["responseWonSmall"]
				multiplier = settings["rewardTwoSeperated"]
				reward = costs * multiplier
				Parent.AddPoints(userId, username, reward)
			else:
				outputMessage = settings["responseLost"]
				reward = costs

			outputMessage = outputMessage.replace("$slots", " " + emotesString + " ")
			outputMessage = outputMessage.replace("$reward", str(reward))
			outputMessage = outputMessage.replace("$multiplier", str(multiplier))

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$user", username)
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
	return
