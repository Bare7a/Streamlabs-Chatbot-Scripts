import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Sound Player"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Sound Player for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.4"

configFile = "config.json"
settings = {}
soundspath = ""
sounds = {}
playlist = ""

def ScriptToggled(state):
	return

def Init():
	global sounds, playlist, soundspath, settings

	path = os.path.dirname(__file__)
	soundspath = path + "\\sounds"

	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!play",
			"permission": "Everyone",
			"volume": 50,
			"costs": 100,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 600,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 1800,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			"responsePlaylist" : "Available sounds: $playlist",
			"responseNotEnoughPoints": "$user you have only $points $currency to pull the lever.",
			"responseWrongSound" : "$user the sound you've tried to play doesn't exist."
		}

	soundsList = os.listdir(soundspath)	
		
	for	sound in soundsList:
		soundFile = sound.rsplit('.', 1) 
		sounds[soundFile[0].lower()] = soundFile[1].lower() 

	playlist = ', '.join(sounds.keys())

	return

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and data.GetParamCount() == 1 and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		costs = settings["costs"]
		
		outputMessage = settings["responsePlaylist"]
		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])
		outputMessage = outputMessage.replace("$playlist", playlist)

		Parent.SendStreamMessage(outputMessage)

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and data.GetParamCount() == 2 and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		costs = settings["costs"]

		if (costs > points):
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
			sound = data.GetParam(1).lower()
			
			if sound in sounds:
				soundpath = soundspath + "\\" + sound + "." + sounds[sound]
				if Parent.PlaySound(soundpath, settings["volume"]): 
					Parent.RemovePoints(userId, username, costs)

					if settings["useCooldown"]:
						Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
						Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])
			else:
				outputMessage = settings["responseWrongSound"]
			outputMessage = outputMessage.replace("$sound", sound)

		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])
		outputMessage = outputMessage.replace("$playlist", playlist)

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
