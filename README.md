# Facial-Recognition-Authentication
This project was a part of Python + Internet of Things self study assignment. 
There are four phases to this system, which are:
1. Data Gathering for Face Detection- 
The first task is to gather the data to train the classifier. A Raspberry Pi camera will capture 30 images. A python code will take 30 faces of each person using OpenCV pre-trained classifier. OpenCV already contains many pre-trained classifiers for face, eyes, smile, etc. The resolution is set at (640, 480) and frame rate at 30 fps.
PiRGBArray() gives us a 3-dimensional RGB array organized(rows, columns, colors) from an unencoded RGB capture. PiRGBArray’s advantage is its ability to read the frames from Raspberry Pi camera as NumPy arrays making it compatible with OpenCV. It avoids the conversion from JPEG format to OpenCV format which would slow the process. Next, the user is asked for a name. If a directory with that name is already there, it will respond with “Name already exists” and will exit the code. If a directory with this name isn’t there, it will create the directory and images will be saved with this name. After that, the capture_continuous function will be used to start reading the frames from the Raspberry Pi camera module.
The capture_continuous function takes three arguments:
1. rawCapture
2. The format in which each frame should be read since OpenCV expects the image to be in the BGR format rather than the RGB so we specify the format to be BGR.
3. The use_video_port boolean, making it true means that a stream is being treated as a video. 

2. Training the recognizer- The recognizer is trained according to the data gathered in the previous step. The LBPH (LOCAL BINARY PATTERNS HISTOGRAMS) face recognizer is used, which is included on the OpenCV package. Finally, the dictionary which contains the directory names and label IDs are stored.

3. Using the Recognizer for Facial Recognition- The recognizer set up in the previous section can now be used to recognize the faces. It will give a confidence level and label ID. If the face matches, the relay will turn on. 
![](images/Facial_Auth)




