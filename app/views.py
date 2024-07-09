from django.shortcuts import render

from django.http import HttpResponse

from django.conf import settings

import os

import datetime

import json

import subprocess

import time

# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)

import demorASD

import ast

import speech_recognition as sr

# Create your views here.

def index(request):
    return HttpResponse("Backend Orchestrator is up")


def processFile(request):
    
    # Save file to local
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    filename = "data_" + timestamp + ".mp4"
    if request.method == 'POST':
        file = request.FILES['file']
        print("filename: ", request.FILES['file'].name)
        
        filePath = os.path.join(settings.BASE_DIR, "demo", filename)
        print("filePath: ", filePath)
        with open(filePath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    print("filename: ", filename)
    # T1: Run Dr. Tian model to to get face coordinates and save in the file

    faces = demorASD.main(filename[:-4])
    
    # print(faces)
    # T2: Extarct audio from the video file

    # T2: Run STT model to get the text from the audio file
    
    # Delete all files

    # Return response with the text and face coordinates as json

    return HttpResponse(json.dumps(faces))


def writeFile(request):
    # Save file to local
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    filename = "data_" + timestamp + ".mp4"
    if request.method == 'POST':
        fileBytes = request.POST.get('fb')
        print("filename: ", fileBytes)
        
        # filePath = os.path.join(settings.BASE_DIR, "demo", filename)
        # print("filePath: ", filePath)
        # with open(filePath, 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)
        byte_string = fileBytes
        byte_list = ast.literal_eval(byte_string)

        # Convert the list of integers to bytes
        byte_data = bytes(byte_list)

        # Decode the bytes to a string
        decoded_string = byte_data.decode('utf-8')

        # Print the resulting string
        print(decoded_string)

        # Open file in binary write mode
        binary_file = open("my_file.mp4", "wb")
        
        # Write bytes to file
        binary_file.write(byte_data)
        
        # Close file
        binary_file.close()

    print("filename: ", filename)

    return HttpResponse("Hello")


def runSpeechToText(audioFilePath2):

	r = sr.Recognizer()
	captions = ""
	with sr.AudioFile(audioFilePath2) as source:
		audio = r.record(source)
		try:
			captions = r.recognize_google(audio)
			print('Converting audio into text...')
			print('Text: ', captions)
		except:
			print('Sorry, could not recognize audio')
	return captions

def speechToText(request):

    # download file
    # Save file to local
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    filename = "dataV_" + timestamp + ".mp4"
    filePath = ""
    if request.method == 'POST':
        file = request.FILES['file']
        print("filename: ", request.FILES['file'].name)
        
        filePath = os.path.join(settings.BASE_DIR, "demo", filename)
        print("filePath: ", filePath)
        with open(filePath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    print("filename: ", filename)

    # Extract audio
    audioFilePath = filePath + "audio.wav"
    nDataLoaderThread = 10
    command = ("ffmpeg -y -i %s -qscale:a 0 -ac 1 -vn -threads %d -ar 16000 %s -loglevel panic" % \
        (filePath, nDataLoaderThread, audioFilePath))
    subprocess.call(command, shell=True, stdout=None)
    sys.stderr.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Extract the audio and save in %s \r\n" %(audioFilePath))

    # run speech to text
    captions = runSpeechToText(audioFilePath)

    # return json response
    response = {
        "captions": captions
    }

    print('response: ', response)

    sys.stderr.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Done \r\n")

    return HttpResponse(json.dumps(response))
