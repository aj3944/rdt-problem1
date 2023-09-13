import io
import time
import picamera
import cv2
import numpy as np
from picamera.array import PiRGBArray

camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.framerate = 25
rawCapture = PiRGBArray(camera,size=(320,240))

time.sleep(0.1)

feature_params = dict(
    maxCorners=50,
    qualityLevel = 0.3,
    minDistance = 7,
    blockSize = 7
    )

lk_params = dict( winSize=(15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT , 10, 0.03))

color = np.random.randint(0,255,(100,3))



old_gray = None
count = 0
for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port = True):
    count += 10
    img_o = np.asarray(frame.array)
    frame = img_o
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if old_gray is None or count % 200 == 0:
        old_gray = frame_gray
        p0 = cv2.goodFeaturesToTrack(old_gray,mask = None, **feature_params)
        mask = np.zeros_like(frame)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray,frame_gray,p0,None,**lk_params)
    if p1 is not None:
        good_new = p1[st==1]
        good_old = p0[st==1]
    
    for i, (new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask,(int(a),int(b)),(int(c),int(d)),color[i].tolist(),2)
        frame = cv2.circle(frame, (int(a),int(b)),5,color[i].tolist(),-1)
    print(mask.size)
    print(frame.size)
    img = cv2.add(frame,mask)
    cv2.imshow('image',img)
    rawCapture.truncate(0)
    cv2.waitKey(10)
    
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
#with picamera.PiCamera() as camera:
#    stream = io.BytesIO()
 #   for frame in camera.capture_continuous(stream,format='bgr'):
  #      img = frame.array
   #     cv2.imshow('image',img)
    #    stream.truncate()
     #   stream.seek(0)
        #if process(stream):
         #   break