from django.shortcuts import render

from django.http import HttpResponse

from django.conf import settings

import os

import datetime

import json

# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)

import demorASD

# Create your views here.

def index(request):
    return HttpResponse("Backend Orchestrator is up")


def processFile(request):
    
    # Save file to local
    filename = ""
    if request.method == 'POST':
        file = request.FILES['file']
        print("filename: ", request.FILES['file'].name)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename = "data_" + timestamp + ".mp4"

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


def getFaceCoordinates(request):

    return HttpResponse("Hello")


def speechToText(request):

    return HttpResponse("Hello")
