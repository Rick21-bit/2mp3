# IMPORT MODULES
from __future__ import print_function, unicode_literals
import os
import shutil
import subprocess
from moviepy.editor import * 
import argparse
from array import array
import requests
import random
import argparse
import youtube_dl   
from fileinput import filename
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from grpc.framework.common import style

def main():
    f = Figlet(font='slant')
    print (f.renderText('2mp3'))
    
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#52d921 bold',
        Token.Selected: '#ff0ada bold',  # default
        Token.Pointer: '#52d921 bold',
        Token.Instruction: '#0abaff',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
        })
    questions = [
    {
        'type': 'list',
        'name': 'convertoptions',
        'message': 'What do you want to do?',
        'choices': [
            'Download And Convert to MP3 from YouTube',
            'Convert a Local File',
            'Convert a Local Files',
    
        ],
        'validate': lambda answer: 'You must choose atleast one option.' \
            if len(answer) == 0 else True
    }]
    answer = prompt(questions, style=style)
    def randomAudioName():
        

        wordSite = "https://www.mit.edu/~ecprice/wordlist.10000"

        response = requests.get(wordSite)
        randomWords = response.content.splitlines()
        randomWord = random.choice(randomWords)
        randomNumber = random.randint(1, 10000000000)
        return "audio" + str(randomWord) + str(randomNumber)
    
    
    def downloadMP3FromYouTube():
        youtubeDownloadLink = [
            {
        'type': "input",
        "name": "videoURL",
        "message": "Paste the URL  ",
            },
            ]
        userResponse = prompt(youtubeDownloadLink)
        videoURL = userResponse.get("videoURL")
        videoINFO = youtube_dl.YoutubeDL().extract_info(
                url=videoURL, download=False
            )
        fileName = "output/" + f"{videoINFO['title']}.mp3"
        options = {
                'format' : 'bestaudio/best',
                'keepvideo' : False,
                'outtmpl' : fileName,
                'postprocessers':
                    [
                        {
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec' :'mp3',
                            'prefferedquality' : '192',
                        }
                    ]
           }
        with youtube_dl.YoutubeDL(options) as ydl :
            ydl.download([videoINFO['webpage_url']])
            
        subprocess.call(["open", fileName])
        
    if answer.get("convertoptions") == 'Download And Convert to MP3 from YouTube':
        downloadMP3FromYouTube()
    elif answer.get("convertoptions") == 'Convert a Local File':
        selectAFile = [
            {
        'type': "input",
        "name": "selectaFile",
        "message": "Enter the path of the file  ",
            },
            ]
        userResponse = prompt(selectAFile)  
        mp4File = userResponse.get("selectaFile")
        output = "output/" + randomAudioName() + ".mp3"
        mediaFile = VideoFileClip(mp4File)
        audioFile = mediaFile.audio
        audioFile.write_audiofile(output)
        audioFile.close()
        mediaFile.close()
    elif answer.get("convertoptions") == 'Convert a Local Files':
        pathofdirectory = [
            {
        'type': "input",
        "name": "selectFiles",
        "message": "Enter the path of the directory  ",
            },
            ]         
        userResponse = prompt(pathofdirectory)
        directorypath = userResponse.get("selectFiles")
        listdir = os.listdir(directorypath)
        for file in listdir:
            filepath = os.path.join(directorypath, file)#Combine the root path and the file name path into an absolute path
            video = VideoFileClip(filepath)
            list_filepath = list(filepath)
            if list_filepath[-1] == '4':
                list_filepath[-1] = '3'
                filepath = ''.join(list_filepath)
                print(filepath)
                audio = video.audio
                audio.write_audiofile(filepath)
                # Copying the file 
                source = filepath 
                output = "/home/rick/Documents/Projects/2mp3/output/" + randomAudioName() + ".mp3"
                shutil.copyfile(os.path.join(directorypath, filepath), output)
                
                os.remove(filepath) #  Delete File after Copying 
                
            else:
                print("Unknown File type,File Skipped ")         
    else:
        print("Sorry Unknown Command")  
        
if __name__ == '__main__':
    main()

# /** 
# * BY Eyoatam Wubeshet - July 30 12:29 , 2021 GC
# *Credit to stackoverflow, greekforgreeks, w3school, codeburst.io and others
# * **/




