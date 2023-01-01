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

from pydub import AudioSegment
#from ffprobe import FFProbe


if __name__ == "__main__":
    
    data_path  = "/Users/neuroling/Downloads/"
    #data_path  = "/Users/ting-hsin/Downloads/"
    
    ## METHOD 2 HALF_SUCCESS ##
    # https://gtts.readthedocs.io/en/latest/
    
    # GOOGLE gTTS >> worked but pause at the strange point  >> Try other's method first
    # The text that you want to convert to audio
    mytext = "奇奇獨自踏著輕快步伐，走在原野上。白紋蝶好奇的飛過來問：「奇奇，你要去哪裡？」「我要去外婆家。」「自己去嗎？你好棒喔！自己去沒問題嗎？」「沒問題！媽媽常常帶我走這條路。」「路上小心！」奇奇來到池塘邊，發現橋斷了。「哎呀！這下子該怎麼辦才好？我只知道這一條路，如果沒辦法走過池塘，我就不能去找外婆了。」奇奇正在煩惱時，池塘裡的青蛙探出水面問：「你怎麼了？」「橋斷了，我到不了外婆家了。」「別擔心，我們可以送你到對岸。」啪啦！嘩啦「哇！這是我第一次抱著蹼足過池塘！」奇奇向青蛙道謝後，沿著小路走過森林，就看到外婆家。「外婆！」奇奇興奮的跑了起來。「哇！奇奇自己來的，真是好棒喔！」外婆見到奇奇也非常開心。"#"ægli"
    
    # Language in which you want to convert
    language = 'zh'#'en'
    
    '''
    ### Arpabet-to-ipa ###
    #>>https://docs.soapboxlabs.com/resources/linguistics/arpabet-to-ipa/
    
    aegliy >> ægli >> aeggli(OK)
    baepay >>bæpaɪ >> badpie(OK)
    baydiy  >>baɪdi  >> bidey(OK)
    browmey >>bɹoʊmeɪ  >> bromay(OK)
    chaeviy  >>tʃævi  >> chavi(OK)
    laelaxst >>lælʌst  >> lalust(OK)
    laeviy  >>lævi >> lavvi(OK)
    maeskiy  >>mæski  >> masgi(OK)
    paenliy  >>pænli  >> panli(OK)
    payliy  >>paɪli  >> piely(OK)
    vaesow  >> væsoʊ  >> vasle(OK)
    weyaet  >> weɪæt  >> way-at(OK)
    '''
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save(data_path + "文本_new.mp3")
    
    # Playing the converted file
    #os.system(data_path + "aegliy_new.mp3")
    
    
    
    # convert the mp3 to wav
    
    ## METHOD 1 SUCCESS##  #
    '''
    # Need pydub & ffmpeg modules to 
      >> use $ !pip install pydub & brew install ffmpeg
    in order to successfully using pydub, ffmpeg needs to be installed as well
    e.g. from pydub import AudioSegment
    '''
    # files
    #src = data_path + "31_new.mp3"
    #dst = data_path + "31_test.wav"
    
    ## convert wav to mp3
    #sound = AudioSegment.from_mp3(src)
    #sound.export(dst, format="wav")
    
    """
    ## METHOD 2 ##
    # import required modules
    import subprocess
    
    # convert mp3 to wav file
    subprocess.call(['ffmpeg', '-i', data_path + "aegliy_new.mp3",
                     data_path + "aegliy_test.wav"])
    """
    
    
    '''
    # pseudoword voice gender change
      >> https://praat-users.yahoogroups.co.narkive.com/x1topFJ4/change-gender-documentation-improvements
    
    1. to change a man to a woman, use a formant shift ratio of 1.2 and a new pitch median of 220 Hz.
    2. to change a woman to a man, use a formant shift ratio of 0.83 and a new pitch median of 100 Hz.
    
    '''
    
    replace_pwDICT = {'aegliy':'aeggli',
                      'baepay':'badpie',
                      'baydiy':'bidey',
                      'browmey':'bromay',
                      'chaeviy':'chavi',
                      'laelaxst':'lalust',
                      'laeviy':'lavvi',
                      'maeskiy':'masgi',
                      'paenliy':'panli',
                      'payliy':'piely',
                      'vaesow':'vasle',
                      'weyaet':'way-at'}
    print(type(replace_pwDICT.get('paenliy')))
    
    
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
    