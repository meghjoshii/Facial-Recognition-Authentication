from __future__ import with_statement
from __future__ import absolute_import
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from io import open

relay_pin = [26]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 0)

with open(u'labels', u'rb') as f:
	dict = pickle.load(f)
	f.close()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))


faceCascade = cv2.CascadeClassifier(u"/home/pi/opencv/data/haarcascades_cuda/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(u"trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX

lst = []

for frame in camera.capture_continuous(rawCapture, format=u"bgr", use_video_port=True):
	frame = frame.array
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	for (x, y, w, h) in faces:
		roiGray = gray[y:y+h, x:x+w]

		id_, conf = recognizer.predict(roiGray)

		for name, value in dict.items():
			
			if value == id_ and conf<=100:
				print lst
				if (name in lst or len(lst)==0) and conf<=70:
					lst.append(name)
				else:
					lst=[]
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				cv2.putText(frame, name + unicode(conf), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)
	
				if len(lst)>10:

					print name,conf	
					
					now = datetime.now()
					curr = now.strftime("%H:%M")
					ent = name+"\t"+curr+"\n"
					file=open("records.txt","a")
					file.write(ent)
					print curr
					file.close()
					GPIO.output(relay_pin, 1)
					lst=[]
					
					
		#if conf <= 70:
			

			else:
				GPIO.output(relay_pin, 0)
		
	cv2.imshow(u'frame', frame)
	key = cv2.waitKey(1)

	rawCapture.truncate(0)

	if key == 27:
		print "HEYYYYY"
		file = open("records.txt","r")
		contents = file.read()
		y=[]
		i=contents.split("\n")
		
		for x in i:
			y.append(x.split("\t"))


		i=0
		nf = open("final.txt","a")
		for i in range(0,len(y)-1):
			if y[i] != y[i+1]:
				n1 = (str(y[i])+"\n").decode('utf8')	
				#n1=str(y[i])+"\n"			
				nf.write(n1)
			else:
				pass
		nf.close()
		break
		

cv2.destroyAllWindows()

