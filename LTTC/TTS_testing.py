#!/usr/bin/env python3
# -*- coding:utf-8 -*-



# This is the part that should be able to do the TTS (Text-to-speech)

#import requests

# Import the required module for text 
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
import os

# import pyttsx3 # Hell no


if __name__ == "__main__":
    
    data_path  = "/Users/neuroling/Downloads/"
    
    
    
    """
    ## METHOD 3 FAIL TERRIBLY##
    # 初始化
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    # 語速控制
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', rate-20)
    
    # 音量控制
    volume = engine.getProperty('volume')
    print(volume)
    engine.setProperty('volume', volume-0.25)
    
    engine.say('hello world')
    engine.say('你好，世界')
    # 朗讀一次
    engine.runAndWait()
    
    engine.say('語音合成開始')
    engine.say('我會說中文了，開森，開森')
    engine.runAndWait()
    
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()
    """
    
    
    """
    ## METHOD 2 HALF_SUCCESS ##
    # GOOGLE gTTS >> worked but pause at the strange point  >> Try other's method first
    # The text that you want to convert to audio
    mytext = "Danny drops out of chemistry after the first quarter and graduates with honors in jazz performance and composition. Students learn how Danny has gone on to a very successful career as a jazz pianist and composer. Slow Starters is another story that many students find relevant to their own lives. It tells the story of a young man, Ari, who spent five years in and out of community college while working part-time jobs. Not until Ari met the 'girl of his dreams' did he begin taking a serious interest in finding a career path. He transferred to a four-year university and chose physical education as a major. After graduation Ari was accepted into an osteopathic medical school and became a doctor. And yes, he marry that dream girl. Creativity and Courage is yet another inspiring story about a Japanese graduate student who started his doctoral baepay research in my laboratory."
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text = mytext, lang = language, slow = False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save(data_path + "Text_Test1.mp3")
    
    # Playing the converted file
    #os.system("mpg321 welcome.mp3")
    
    
    
    """
    """
    ## METHOD 1 FAIL ##
    url = "https://voicerss-text-to-speech.p.rapidapi.com/"
    
    querystring = {"key":"undefined"}
    
    payload = "src=Hello%2C%20world!&hl=en-us&r=0&c=mp3&f=8khz_8bit_mono"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
        "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    
    print(response.text)
    
    """
