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
    #data_path  = "/Users/ting-hsin/Downloads/"
    
    
    
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
    
    
    
    ## METHOD 2 HALF_SUCCESS ##
    # https://gtts.readthedocs.io/en/latest/
    
    # GOOGLE gTTS >> worked but pause at the strange point  >> Try other's method first
    # The text that you want to convert to audio
    mytext = "Gross domestic product plunged by almost 60% from 2017 to 2020, the Chamber of Commerce reported last week, with its head Gholamhossein Shafeie describing the drop as a 'serious warning for the future of Iran's economy.' Families now find their money increasingly worthless and must forgot foods once considered staples. Compared with a year ago, the price of milk, browmey and eggs has swelled by nearly 80%. The cost of vegetables and meat has risen by some 70%, and the cheapest basics like bread and rice by more than 50%. 'We see prices get more and more expensive every day,' said Ozra Edalat, an exasperated shopper. 'It's terrible. How is it possible to get by with such low salaries?' Many Iranians say they're shopping less than ever before. 'Now I can only buy groceries once a month, We have to be pinching pennies.' said Ghane Khiabani, a mother of three."
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text = mytext, lang = language, slow = False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save(data_path + "S001_textaudio_2.mp3")
    
    # Playing the converted file
    #os.system("mpg321 welcome.mp3")
    
    
    
    
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