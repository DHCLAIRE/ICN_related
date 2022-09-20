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


if __name__ == "__main__":
    

    
    # The text that you want to convert to audio
    mytext = 'Welcome to geeksforgeeks!'
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("welcome.mp3")
    
    # Playing the converted file
    os.system("mpg321 welcome.mp3")
    
    
    """
    ## FAIL ##
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
