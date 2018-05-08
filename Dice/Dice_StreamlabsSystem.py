import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Dice Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Dice Minigame for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.5"

configFile = "config.json"
settings = {}

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
			"command": "!dice",
			"permission": "Everyone",
			"useCustomCosts" : True,
			"costs": 1,
			"reward1": 2,
			"reward2": 3,
			"reward3": 4,
			"reward4": 5,
			"reward5": 100,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			"responseNotEnoughPoints": "$user you have only $points $currency to roll the dices.",
			"responseWon": "$user rolls the dices $dices and wins $reward $currency",
			"responseLost": "$user rolls the dices $dices and looses $cost $currency"
		}

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

			dice1 = Parent.GetRandom(1, 7)
			dice2 = Parent.GetRandom(1, 7)
			dice3 = Parent.GetRandom(1, 7)
			dices = "[" + str(dice1) + "] [" + str(dice2) +"] [" + str(dice3) + "]"
			dicesSum = dice1 + dice2 + dice3
			reward = ""

			if dicesSum < 11:
				outputMessage = settings["responseLost"]
				reward = costs
			elif dicesSum >= 11 and dicesSum <= 14:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward1"]
				Parent.AddPoints(userId, username, int(reward))
			elif dicesSum == 15:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward2"]
				Parent.AddPoints(userId, username, int(reward))
			elif dicesSum == 16:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward3"]
				Parent.AddPoints(userId, username, int(reward))
			elif dicesSum == 17:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward4"]
				Parent.AddPoints(userId, username, int(reward))
			elif dicesSum == 18:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward5"]
				Parent.AddPoints(userId, username, int(reward))

			outputMessage = outputMessage.replace("$dice1", str(dice1))
			outputMessage = outputMessage.replace("$dice2", str(dice2))
			outputMessage = outputMessage.replace("$dice3", str(dice3))
			outputMessage = outputMessage.replace("$dices", str(dices))
			outputMessage = outputMessage.replace("$dicesSum", str(dicesSum))
			outputMessage = outputMessage.replace("$reward", str(reward))

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
