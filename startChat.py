############################################################################
#      _       _   _____     _   _        _           _   _____ _       _   
#  ___| |_ ___| |_| __  |___| |_|_|   ___| |_ ___ ___| |_|     | |_ ___| |_ 
# |  _|   | .'|  _| __ -| . |  _|_   |_ -|  _| .'|  _|  _|   --|   | .'|  _|
# |___|_|_|__,|_| |_____|___|_| |_|  |___|_| |__,|_| |_| |_____|_|_|__,|_|  
#                                                                           
############################################################################
# Name: chatBot: startChat
# Description: Handles the ChatGPT and Polly portions of the ChatGPT chat bot
# Author: Jonas Werner
# Version: 0.1
############################################################################

import subprocess
import openai
import os
import datetime, time
import boto3
import wave

AWS_ACCESS_KEY_ID       = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY   = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_DEFAULT_REGION      = os.environ["AWS_DEFAULT_REGION"]
openai.api_key 		= os.getenv("OPENAI_API_KEY")

loopCounter = 0


def speak(text):
    global speaking

    polly_client = boto3.Session(
    aws_access_key_id		= AWS_ACCESS_KEY_ID,
    aws_secret_access_key	= AWS_SECRET_ACCESS_KEY,
    region_name			= AWS_DEFAULT_REGION).client('polly')

    # Voices: Salli, Kevin, Ivy, Kazuha, Emma, Takumi  
    response = polly_client.synthesize_speech(
        Engine          = 'neural',
        VoiceId		= 'Kazuha',
        OutputFormat	= 'mp3',
        Text 		= text)

    file = open('pollyOutput.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

    play_sound("pollyOutput.mp3")
    os.remove("pollyOutput.mp3")
    speaking = False


def play_sound(waveFile):
    subprocess.run(["amixer", "-c", "1", "set", "Mic", "nocap"])
    os.system("mpg321 " + waveFile)
    subprocess.run(["amixer", "-c", "1", "set", "Mic", "cap"])
    #exit(0)    


def callingOpenAi(message):
    # There are many ways tp have fun by customizing the payload prior to sending to OpenAI.
    # For example, asking it to reply as though it is a character from a videogame or 
    # to translate the text it is being sent
    # If the reply is expected to come back in a different language, please make sure to align
    # the Amazon Polly voice so it supports the language requested

    message = "Please translate the following text into Japanese: " + message
    #message = "Please answer in max two sentences: " + message
    #message = "Please answer as if you were Flowey from the game Undertale: " + message
    #message = "Please answer as if you were Sans from the game Undertale: " + message
    #message = "日本語であなたが Undertale ゲームの Flowey であるかのように答えてください: " + message
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    reply = completion.choices[0].message
    print("Answer: %s\n" % reply['content'])

    return reply


while True:
    print("Loop counter is: %i" % loopCounter)

    if loopCounter > 2:
        exit(0)

    output = subprocess.Popen(["python", "transcribe.py"], stdout=subprocess.PIPE).communicate()[0]

    transcribedText = output.decode()
    transcribedText = transcribedText.strip()

    print("Transcribe returned: %s" % transcribedText)
    if "terminate" in transcribedText.lower():
       quit() 

    reply = callingOpenAi(transcribedText)
    if len(reply) > 0:
        loopCounter = 0

    speak(reply['content'])

    loopCounter += 1

