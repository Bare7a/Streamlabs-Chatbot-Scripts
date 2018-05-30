import clr
import sys
import json
import os
import ctypes
import codecs
import time

ScriptName = "Trivia Minigame"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Trivia Minigame for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.6"

configFile = "config.json"
questionsFile = "questions.txt"
settings = {}
parth = ""

questionsList = []
currentQuestion = ""
currentAnswer = ""
currentReward = 0

resetTime = 0


def ScriptToggled(state):
	return

def Init():
	global questionsList, settings, path 

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"permission": "Everyone",
			"ignoreCaseSensitivity": True,  
			"minReward": 1,
			"maxReward": 10,
			"questionInterval": 10,			
			"responseAnnouncement": "Win $reward $currency by answering: $question",
			"responseWon": "$user answered the question first - $answer and won $reward $currency!"
		}

	try: 
		with codecs.open(os.path.join(path, questionsFile), encoding="utf-8-sig", mode="r") as file:
			questionsList = [eval(line.strip()) for line in file if line.strip()]
	except:
		questionsList = [["If you see this message save the file as UTF-8","Error"]]
	
	return

def Execute(data):
	global currentQuestion, currentAnswer, currentReward

	if data.IsChatMessage() and ((data.Message == currentAnswer) or (settings["ignoreCaseSensitivity"] and (data.Message.lower() == currentAnswer.lower()))) and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		userId = data.User			
		username = data.UserName

		Parent.AddPoints(userId, username, currentReward)

		outputMessage = settings["responseWon"]	

		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$question", currentQuestion)
		outputMessage = outputMessage.replace("$answer", currentAnswer)
		outputMessage = outputMessage.replace("$reward", str(currentReward))
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

		currentQuestion = ""
		currentAnswer = ""
		currentReward = 0

		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)
    return

def OpenQuestionsFile():
	location = os.path.join(os.path.dirname(__file__), questionsFile)
	os.startfile(location)
	return


def Tick():
	global questionsList, resetTime, currentQuestion, currentAnswer, currentReward

	if (settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"]):
		currentTime = time.time()

		if(currentTime >= resetTime):
			resetTime = currentTime + (settings["questionInterval"] * 60)
			outputMessage = settings["responseAnnouncement"]

			randomQuestion = questionsList.pop(Parent.GetRandom(0, len(questionsList)))
			currentQuestion = randomQuestion[0] 
			currentAnswer = randomQuestion[1]

			if len(questionsList) == 0:
				try: 
					with codecs.open(os.path.join(path, questionsFile), encoding="utf-8-sig", mode="r") as file:
						questionsList = [eval(line.strip()) for line in file if line.strip()]
				except:
					questionsList = [["If you see this message save the file as UTF-8","Error"]]

			currentReward = Parent.GetRandom(settings["minReward"], settings["maxReward"])
			outputMessage = outputMessage.replace("$question", currentQuestion)
			outputMessage = outputMessage.replace("$answer", currentAnswer)
			outputMessage = outputMessage.replace("$reward", str(currentReward))
			outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())

			Parent.SendStreamMessage(outputMessage)
	return
