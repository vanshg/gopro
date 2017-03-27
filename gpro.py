#! /bin/python

import subprocess as sp
from goprohero import GoProHero
import urllib
from time import sleep
import threading


camera = GoProHero(password='uclaaiaa')
camera.command('power', 'on')
while True:
	status = camera.status()
	if (len(status) > 4): # When the camera is on, there are more than 4 keys
		break

camera.command('preview', 'on')
camera.command('mode', 'still')
status = camera.status()
battery = status["batt1"]
if battery < 20:
	print("Low battery")
# startingimgnum = status["npics"] #TODO: See if this works
startingimgnum = 2454+status["npics"] #No longer needs to be changed. Getting starting number dynamically
# todo: 2454 is hardcoded, what does it mean, and can i get that number dynamically too?

def getPicture(url, filename):
	urllib.urlretrieve(url, filename)
	# sp.call(["target_spotter", filename])

while True:
	camera.command('record', 'on')
	sleep(1.5) # wait for the gopro to save the picture
	filename = "GOPR{0}.JPG".format(startingimgnum)
	url = "http://10.5.5.9:8080/videos/DCIM/105GOPRO/{0}".format(filename)
	threading.Thread(target=getPicture, args=(url, filename)).start()
	sleep(5)
	startingimgnum = startingimgnum + 1



# import numpy as np
# import cv2
# import json

# statusJson = json.loads(status)
# stream = cv2.VideoCapture("http://10.5.5.9:8080/live/amba.m3u8");
# suc, img = stream.read()
# print(suc)
# print(img)

# camera.image()

# cv2.namedWindow("GoPro",cv2.CV_WINDOW_AUTOSIZE)
# cv2.imshow("GoPro", camera.image())


# print()
# thing = status["raw"]["camera/cv"]
# stream = cv2.VideoCapture(thing)
# success, numpyImage = stream.read()
# if success:
# 	print("Success")


# VIDEO_URL = "http://10.5.5.9:8080/live/amba.m3u8"
# FFMPEG_BIN = "ffmpeg"

# pipe = sp.Popen([ FFMPEG_BIN, "-i", VIDEO_URL,
#            "-loglevel", "quiet", # no text output
#            "-an",   # disable audio
#            "-f", "image2pipe",
#            "-pix_fmt", "bgr24",
#            "-vcodec", "rawvideo", "-"],
#            stdin = sp.PIPE, stdout = sp.PIPE)

# while True:
#     raw_image = pipe.stdout.read(432*240*3) # read 432*240*3 bytes (= 1 frame)
#     if len(raw_image) > 0:
#     	image =  np.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
#     	# image =  np.array(raw_image).reshape((240,432,3))
#     	cv2.imshow("GoPro", image)
#     	if cv2.waitKey(5) == 27:
#         	break
# cv2.destroyAllWindows()