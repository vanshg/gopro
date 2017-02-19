# import numpy as np
# import cv2
# import json
import subprocess as sp
from goprohero import GoProHero
import urllib
from time import sleep


camera = GoProHero(password='uclaaiaa')
camera.command('power', 'on')
sleep(5) #wait for camera to finish powering on
# TODO: check status for camera ready instead of just sleeping
# status = camera.status()
camera.command('preview', 'on')
camera.command('mode', 'still')
# TODO: See if we can set the picture resolution
# camera.command('picres', '8MP med')
startingimgnum = 2448 #This number needs to be set every time the program runs

while True:
	camera.command('record', 'on')
	sleep(1.5) # wait for the gopro to save the picture
	filename = "{0}.jpg".format(startingimgnum)
	url = "http://10.5.5.9:8080/videos/DCIM/102GOPRO/GOPR{0}.JPG".format(startingimgnum)
	urllib.urlretrieve(url, filename)
	sleep(5)
	sp.call(["target_spotter", filename])
	startingimgnum = startingimgnum + 1





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