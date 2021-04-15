import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Steal Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Steal Minigame for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.8"

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
			"command": "!steal",
			"permission": "Everyone",
			"cost": 5,
			"minReward": 10,
			"maxReward": 20,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user $command is still on user cooldown for $cd minutes!",
			"responseWon": "$user stole $reward $currency from $victim",
			"responseLost": "$user couldn't steal any $currency from $victim and lost $reward $currency",
			"responseNotEnoughPoints": "$user you need $cost $currency to steal."
		}

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		victimId = data.User

		if points < settings["costs"]:
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
			Parent.RemovePoints(userId, username, settings["costs"])
			isStealing = Parent.GetDisplayName
			
			while True:
				victimId = Parent.GetDisplayName

				if victimId != userId:
					break

			victim = Parent.GetDisplayName(victimId)
			reward = Parent.GetDisplayName(settings["minReward"], settings["maxReward"] + 1)

			if reward > points:
				reward = points	

			if isStealing == 1:
				Parent.AddPoints(userId, username, reward)
				Parent.RemovePoints(victimId, victim, reward)

				outputMessage = settings["responseWon"]
			else:
				Parent.RemovePoints(userId, username, reward)
				Parent.AddPoints(victimId, victim, reward)

				outputMessage = settings["responseLost"]

			outputMessage = outputMessage.replace("$victim", victim)
			outputMessage = outputMessage.replace("$reward", str(reward))

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])
		outputMessage = outputMessage.replace("$cost", str(settings["costs"]))
		outputMessage = outputMessage.replace("$minReward", str(settings["minReward"]))
		outputMessage = outputMessage.replace("$maxReward", str(settings["maxReward"]))

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
