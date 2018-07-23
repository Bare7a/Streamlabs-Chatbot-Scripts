import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Auto Hosting"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Auto Hosting for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.8"

configFile = "config.json"
settings = {}
usersFile = "users.txt"

userList = []
blackList = {}
resetTime = 0
delayTime = 0
delay = 1

def ScriptToggled(state):
	return

def Init():
	global settings, usersFile, userList

	path = os.path.dirname(__file__)
	usersFile = os.path.join(path, usersFile)

	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"offlineOnly": True,
			"command": "!hostme",
			"hostCountdown" : 15,
			"permission": "Everyone",
			"saveUserlist": False,
			"useBlacklist" : False,
			"blacklistCooldown" : 60,
			"blacklistResponse" : "$user, you are still in the blacklist! Wait $cd more minutes before writing $command again!",
			"useCosts" : False,
			"costs" : 10,
			"responseNotEnoughPoints" : "$user you need $cost $currency to use $command. Currently you have only $points $currency.",
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes! ",
			"addedResponse" : "$user, you have been added to the hosting list! Someone will be hosted in $remaining minutes!",
			"alreadyResponse" : "$user, you are already in the hosting list! Someone will be hosted in $remaining minutes!"
		}
	
	if settings["saveUserlist"]:
		try: 
			with codecs.open(usersFile, encoding="utf-8-sig", mode="w") as file:
				file.write("")
		except:
			with codecs.open(usersFile, encoding="utf-8-sig", mode="w") as file:
				file.write("")
									
	return

def Execute(data):
	global userList, blackList

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and (settings["offlineOnly"] and (not Parent.IsLive()) or (not settings["offlineOnly"])):
		outputMessage = ""
		userId = data.User
		username = data.UserName
		points = Parent.GetPoints(userId)
		costs = settings["costs"]
		currentTime = time.time() 

		if (costs > Parent.GetPoints(userId)) and settings["useCosts"]:
			outputMessage = settings["responseNotEnoughPoints"]
		elif settings["useBlacklist"] and (username in blackList):
			cd = str(int(blackList[username] - currentTime) / 60) + ":" + str(int(blackList[username] - currentTime) % 60).zfill(2) 
			outputMessage = settings["blacklistResponse"] 
			outputMessage = outputMessage.replace("$cd", cd)
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
			if username in userList:
				alreadyMessage = settings["alreadyResponse"]
				outputMessage = alreadyMessage
			else:
				userList.append(username)
				addedResponse = settings["addedResponse"]
				outputMessage = addedResponse

				if settings["saveUserlist"]:
					with open(usersFile, "a") as file:
						file.write(username + "\n")

				if settings["useCosts"]:
					Parent.RemovePoints(userId, username, costs)

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

		remaining = str(int(resetTime - currentTime) / 60) + ":" + str(int(resetTime - currentTime) % 60).zfill(2) 
		
		outputMessage = outputMessage.replace("$remaining", remaining)
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$cost", str(costs))
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
	global resetTime, delayTime, delay, userList, blackList, settings

	currentTime = time.time() 

	if(currentTime >= resetTime):
		resetTime = currentTime + (settings["hostCountdown"] * 60)
		userCount = len(userList)

		if userCount > 0:
			winner = userList[Parent.GetRandom(0, len(userList))]
			outputMessage = "/host " + winner

			if settings["useBlacklist"]:
				blackTime = currentTime + (settings["blacklistCooldown"] * 60)
				blackList[winner] = blackTime
		else:
			outputMessage = "/unhost"
		
		userList = []

		if settings["saveUserlist"]:
			with codecs.open(usersFile, encoding="utf-8-sig", mode="w") as file:
				file.write("")

		Parent.SendStreamMessage(outputMessage)
		

	if settings["useBlacklist"] and (currentTime >= delayTime):
		delayTime = currentTime + delay

		for key, value in blackList.items():
			if currentTime >= value:
				blackList.pop(key)

	return