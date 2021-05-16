#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from pynput import keyboard
import time
import pyaudio
import wave
import sched
import sys
import pyttsx3
import time
import wave
import pandas as pd
import pyperclip as clip

import pyaudio
import pyautogui as g
import pyperclip as clip
import speech_recognition as sr
from pynput.keyboard import Listener, KeyCode
g.size()
g.FAILSAFE = True
g.PAUSE = 0

current_directory = os.path.dirname(os.path.realpath("__file__")) + "/"
data_directory = os.path.join(current_directory, 'data')
wav_file = f"{data_directory}/new_recording.wav"
ideas_file = f"{data_directory}/ideas.csv"
documentation_file = os.path.join(data_directory, 'documentation.md')
current_directory, data_directory

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(wav_file, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)
    def on_press(self, key):
        if key == keyboard.Key.ctrl:
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key == keyboard.Key.ctrl:
            self.key_pressed = False
        return True

def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        try:
            stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = callback)
            print("Stream active:", stream.is_active())
            started = True
            print("start Stream")
        except:
            raise

    elif not listener.key_pressed and started:
        print("Stop recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        listener.wf.writeframes(b''.join(frames))
        listener.wf.close()
        print("You should have a wav file in the current directory")
        return
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())

def react_to_recording():
    try:
        r = sr.Recognizer()
        audio_file = sr.AudioFile(wav_file)
        with audio_file as source:
            audio = r.record(source)
        command = r.recognize_google(audio)
        print(command)
        return command
    except:
        pass

def speak_text(text):
    engine = pyttsx3.init()
    engine.startLoop(False)
    engine.say(text)
    engine.iterate()
    time.sleep(0.10*len(text))
    engine.endLoop()

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100 
messages = ["Describe the idea informally as if describing it to a friend",
"Explain which actionable metric you expect to improve from this idea",
"List any assumptions that have led you to find this idea as a priority idea",
"List any assumptions that will help you solve the problem quicker",
"Has something similar been worked on, and what was the result",
"Why do we think this idea solves a user problem",
"What are the benefits of this idea",
"How will this feature be used by the user",
"What is a workaround to solving this problem without building the feature",
"What relevant data is in the data warehouse already",
"What relevant data do you want to place into the data warehouse",
"Would this data come from either tracking servers, APIs, web scraping, or sensor data",
"What data should not be used",
"What data system would best store each new dataset",
"What data should be encrypted to reduce the risk of hackers or being sued",
"In what way will the data still be messy and need to be cleaned up",
"Steps that will be taken to ensure the accuracy of the data involved",
"The status of the idea and the result",
"Information to help with the maintenance of the feature",
"Information to help sales/marketing promote the feature",
"Information to help support or users troubleshoot frequently asked questions",
"Meeting summaries and action items",
"You're done, you can find the documentation saved in your clipboard or in the project's data directory"]
responses = []

for message in messages:
    p = pyaudio.PyAudio()
    frames = []
    listener = MyListener()
    listener.start()
    started = False
    stream = None
    print("Press and hold the 'ctrl' key to begin recording")
    print("Release the 'ctrl' key to end recording")
    speak_text(message)
    task = sched.scheduler(time.time, time.sleep)
    task.enter(0.1, 1, recorder, ())
    task.run()
    response = react_to_recording()
    response = "" if response == None else response.lower()
    responses.append(response)
    previously_listening = False
    


# Build the documentation
string_builder = []
string_builder.append(f"# README\n")
for message, response in zip(messages[:-1], responses[:-1]):
    response = response.capitalize()
    response = response.replace(" i ", " I ").replace(" i'", " I'")
    response = response if not response.startswith("i ") else "I " + response[2:]
    string_builder.append(f"### {message}\n")
    string_builder.append(f"{response}\n")
documentation_output = "\n".join(string_builder)

# Save to clipboard
clip.copy(documentation_output)

# Write the file
file = open(documentation_file, 'w')
file.write(documentation_output)
file.close()

print(documentation_output)


# In[ ]:




