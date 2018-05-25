import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Simple TTS"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Simple TTS for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.6"

configFile = "config.json"
settings = {}
commandLength = 0
voiceParams = ""

def ScriptToggled(state):
	return

def Init():
	global settings, commandLength, voiceParams

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!tts",
			"permission": "Everyone",
			"costs": 100,
			"voiceType": "Male",
			"voiceVolume": 50,
			"voiceRate": 0,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 1,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user $command is still on user cooldown for $cd minutes!",
			"responseNotEnoughPoints": "$user you need $cost $currency to use $command.",
		}
	
	commandLength = len(settings["command"]) + 1
	voiceParams = "cscript " + path + "\\speech.vbs " + str(int(settings["voiceVolume"])) + " " + str(int(settings["voiceRate"]))

	if settings["voiceType"] == "Male":
		voiceParams = voiceParams + " 0 "
	elif settings["voiceType"] == "Female":
		voiceParams = voiceParams + " 1 "	

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		costs = settings["costs"]

		if (costs > Parent.GetPoints(userId)):
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

			userMessage = data.Message[commandLength:]
			command = voiceParams + '"' + userMessage + '"'
			os.popen(command)

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
