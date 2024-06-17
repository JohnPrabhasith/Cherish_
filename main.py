import speech_recognition as sr
import webbrowser as wb
import pyttsx3 #Text to Speech
import Music_Library as ml
import requests
from g4f.client import Client
from gtts import gTTS
import pygame
import os
import warnings
warnings.filterwarnings("ignore")

r = sr.Recognizer()
engine = pyttsx3.init() #Creating an object of pyttsx3 Engine  for Text to Speech
newsapi = "882e0a9d210647d095ded2555cbe5e37"
engine.setProperty('rate', 150) #Speed of Speech


def old_speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("audio.mp3")


def AIProcess(command):
    client = Client()
    response = client.chat.completions.create(
        model="gemini",
        messages=[{
                "role": "system",
                "content": "You are a Virtual Assistant named sunday .You are Like google Assitant."
            },
            {
                "role": "user",
                "content": command
            }],
    )
    json_response = response.to_json()
    return json_response['choices'][0]['message']['content']

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        wb.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        wb.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        wb.open("https://www.facebook.com")
    elif c.lower().startswith("play"):
        song = c.split("play",1)[1].strip()
        if song in ml.music:
            speak("Playing "+song)
            wb.open(ml.music[song])
        else:
            speak("Sorry, I don't have that song in my library")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article['title'])
    elif "who created you" in c.lower():
        speak("I was created by B L J Prabhaseeth")
    elif "exit" in c.lower() or "quit" in c.lower():
        speak("Goodbye!")
        exit()
    else:
        output = AIProcess(c.lower())
        speak(output)

if __name__ == "__main__":
    speak("Initializing ...")
    while True:
        # Listen for the wake word "sunday..."
        #Obtain Audio from the microphone
        #Recognize the Audio using Google Speech Recognition
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=4,phrase_time_limit=2)
            word = r.recognize_google(audio)
            if("sunday" in word.lower()):
                speak("Yaa Buddy")
                with sr.Microphone() as source:
                    print("sunday Is Active...")
                    audio = r.listen(source, timeout=3)
                    command = r.recognize_google(audio)

                    processCommand(command)
                #Listen for Command
        except Exception as e:
            print("Error; {0}".format(e))
