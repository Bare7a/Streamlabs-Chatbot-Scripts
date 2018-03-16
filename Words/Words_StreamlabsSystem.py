import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Words Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Words Minigame for Twitch chat"
Creator = "Bare7a"
Version = "1.2.0"

configFile = "config.json"
settings = {}

resetTime = 0
wordsList = []
currentWord = ""

def ScriptToggled(state):
	return

def Init():
	global settings, configFile, resetTime, wordsList, currentWord

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"permission": "Everyone",
			"minReward": 1,
			"maxReward": 10,
			"wordInterval": 10,
			"wordsList": "Aatrox, Ahri, Akali, Alistar, Amumu, Anivia, Annie, Ashe, Aurelion Sol, Azir, Bard, Blitzcrank, Brand, Braum, Caitlyn, Camille, Cassiopeia, Cho'Gath, Corki, Darius, Diana, Dr. Mundo, Draven, Ekko, Elise, Evelynn, Ezreal, Fiddlesticks, Fiora, Fizz, Galio, Gangplank, Garen, Gnar, Gragas, Graves, Hecarim, Heimerdinger, Illaoi, Irelia, Ivern, Janna, Jarvan IV, Jax, Jayce, Jhin, Jinx, Kai'Sa, Kalista, Karma, Karthus, Kassadin, Katarina, Kayle, Kayn, Kennen, Kha'Zix, Kindred, Kled, Kog'Maw, LeBlanc, Lee Sin, Leona, Lissandra, Lucian, Lulu, Lux, Malphite, Malzahar, Maokai, Master Yi, Miss Fortune, Mordekaiser, Morgana, Nami, Nasus, Nautilus, Nidalee, Nocturne, Nunu, Olaf, Orianna, Ornn, Pantheon, Poppy, Quinn, Rakan, Rammus, Rek'Sai, Renekton, Rengar, Riven, Rumble, Ryze, Sejuani, Shaco, Shen, Shyvana, Singed, Sion, Sivir, Skarner, Sona, Soraka, Swain, Syndra, Tahm, Kench, Taliyah, Talon, Taric, Teemo, Thresh, Tristana, Trundle, Tryndamere, Twisted, Fate, Twitch, Udyr, Urgot, Varus, Vayne, Veigar, Vel'Koz, Vi, Viktor, Vladimir, Volibear, Warwick, Wukong, Xayah, Xerath, Xin Zhao, Yasuo, Yorick, Zac, Zed, Ziggs, Zilean, Zoe, Zyra",
			"responseAnnouncement": "Whoever writes $word first gets free $currency!",
			"responseWon": "$user wrote $word first and won $reward $currency!"
		}
	
	tempList = settings["wordsList"].split(",")
	
	for word in tempList:
		wordsList.append(word.strip())

	currentWord = wordsList[Parent.GetRandom(0, len(wordsList))]
	resetTime = time.time() + (settings["wordInterval"] * 60)
	return

def Execute(data):
	global settings, resetTime, currentWord

	if data.IsChatMessage() and (data.Message == currentWord) and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		userId = data.User			
		username = data.UserName

		reward = Parent.GetRandom(settings["minReward"], settings["maxReward"])
		Parent.AddPoints(userId, username, reward)

		outputMessage = settings["responseWon"]	

		outputMessage = outputMessage.replace("$reward", str(reward))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$word", currentWord)
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

		currentWord = ""

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
	global settings, resetTime, wordsList, currentWord

	currentTime = time.time()

	if(currentTime >= resetTime):
		resetTime = currentTime + (settings["wordInterval"] * 60)
		outputMessage = settings["responseAnnouncement"]

		currentWord = wordsList[Parent.GetRandom(0, len(wordsList))] 

		outputMessage = outputMessage.replace("$word", currentWord)
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

		Parent.SendStreamMessage(outputMessage)
	return