import urllib.request
import RPi.GPIO as GPIO
import os, sys
import time
import argparse

parser = argparse.ArgumentParser(description='RPI GoPro Camera Script')
parser.add_argument('-photoMode', help='Set camera to take pictures, video is default', action="store_true", default=False)
args = parser.parse_args()


# Define a function to send a command to the camera
def SendCmd(cmd):
	data = urllib.request.urlretrieve(cmd)


wifipassword = "09021967"

isPhotoMode = args.photoMode
if isPhotoMode:
	print("Photo Mode is ON")
else:
	print("Video Mode is ON")

# See https://github.com/KonradIT/goprowifihack/blob/master/WiFi-Commands.mkdn
# for a list of http commands to control the GoPro cameera

on = "http://10.5.5.9/bacpac/PW?t=" + wifipassword + "&p=%01"
off = "http://10.5.5.9/bacpac/PW?t=" + wifipassword + "&p=%00"
shutter = "http://10.5.5.9/bacpac/SH?t=" + wifipassword + "&p=%01"
stop = "http://10.5.5.9/bacpac/SH?t=" + wifipassword + "&p=%00"
videoMode = "http://10.5.5.9/camera/CM?t=" + wifipassword + "&p=%00"
photoMode = "http://10.5.5.9/camera/CM?t=" + wifipassword + "&p=%01"
burstMode = "http://10.5.5.9/camera/CM?t=" + wifipassword + "&p=%02"
timeLapseMode = "http://10.5.5.9/camera/CM?t=" + wifipassword + "&p=%03"
previewOn = "http://10.5.5.9/camera/PV?t=" + wifipassword + "&p=%02"
previewOff = "http://10.5.5.9/camera/PV?t=" + wifipassword + "&p=%00"
wvga60 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%00"
wvga120 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%01"
v720p30 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%02"
v720p60 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%03"
v960p30 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%04"
v960p48 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%05"
v1080p30 = "http://10.5.5.9/camera/VR?t=" + wifipassword + "&p=%06"
viewWide = "http://10.5.5.9/camera/FV?t=" + wifipassword + "&p=%00"
viewMedium = "http://10.5.5.9/camera/FV?t=" + wifipassword + "&p=%01"
viewNarrow = "http://10.5.5.9/camera/FV?t=" + wifipassword + "&p=%02"
res11mpWide = "http://10.5.5.9/camera/PR?t=" + wifipassword + "&p=%00"
res8mpMedium = "http://10.5.5.9/camera/PR?t=" + wifipassword + "&p=%01"
res5mpWide = "http://10.5.5.9/camera/PR?t=" + wifipassword + "&p=%02"
res5mpMedium = "http://10.5.5.9/camera/PR?t=" + wifipassword + "&p=%03"
noSound = "http://10.5.5.9/camera/BS?t=" + wifipassword + "&p=%00"
sound70 = "http://10.5.5.9/camera/BS?t=" + wifipassword + "&p=%01"
sound100 = "http://10.5.5.9/camera/BS?t=" + wifipassword + "&p=%02"

# Init GPIO, use GPIO pin 5 as input trigger from APM/Pixhawk
camTrigger = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(camTrigger, GPIO.IN, GPIO.PUD_UP)

# Init GoPro
SendCmd(on)

time.sleep(5)

if isPhotoMode:
	SendCmd(photoMode)
else: 
	SendCmd(videoMode)
	SendCmd(v1080p30)




# Loop waiting for camera trigger

recording = False

if isPhotoMode:
	while True:
		if GPIO.input(camTrigger) == True:
			print("Shutter Triggered")
			SendCmd(shutter)
			# Wait for it to go False
			while GPIO.input(camTrigger) == True:
				time.sleep(0.1)
			print("Shutter Off")

else:
	while True:
		if GPIO.input(camTrigger) == True:
			if (not recording): 
				print("Recording Triggered")
				SendCmd(shutter)
				recording = True
			else:
				print("Recording Stopped")
				SendCmd(stop)
				recording = False
			# Wait for false
			while GPIO.input(camTrigger) == True:
				time.sleep(0.1)


# Clean up
GPIO.cleanup()

