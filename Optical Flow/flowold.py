# import the necessary packages
#from picamera2.array import PiRGBArray
from picamera2 import PiCamera2
import time
import cv2
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera2(1024,768)
camera.resolution = (1024, 768)
camera.start_preview()

sleep(2)
camera.capture('foo.jpg')
#print(camera)
#rawCapture = PiRGBArray(camera)
# allow the camera to warmup
#time.sleep(0.1)
# grab an image from the camera
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
# display the image on screen and wait for a keypress
#cam = cv2.VideoCapture(0)
#image = cam.read()
#print(image)
#cv2.imshow("Image", image)
#cv2.waitKey(0)