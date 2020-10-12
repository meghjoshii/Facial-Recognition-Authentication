from __future__ import with_statement
from __future__ import absolute_import
import os
import numpy as np 
from PIL import Image 
import cv2
import pickle
from io import open

faceCascade = cv2.CascadeClassifier(u"/home/pi/opencv/data/haarcascades_cuda/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, u"images")

currentId = 1
labelIds = {}
yLabels = []
xTrain = []

for root, dirs, files in os.walk(imageDir):
	print root, dirs, files
	for file in files:
		print file
		if file.endswith(u"png") or file.endswith(u"jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(root)
			print label

			if not label in labelIds:
				labelIds[label] = currentId
				print labelIds
				currentId += 1

			id_ = labelIds[label]
			pilImage = Image.open(path).convert(u"L")
			imageArray = np.array(pilImage, u"uint8")
			faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

			for (x, y, w, h) in faces:
				roi = imageArray[y:y+h, x:x+w]
				xTrain.append(roi)
				yLabels.append(id_)

with open(u"labels", u"wb") as f:
	pickle.dump(labelIds, f)
	f.close()

recognizer.train(xTrain, np.array(yLabels))
recognizer.save(u"trainer.yml")
print labelIds
