import time
import cv2
import sys
import os
import imutils
import RPi.GPIO as GPIO

#unwatched = GPIO.LOW
#watched = GPIO.HIGH

#if len(sys.argv) > 1:
unwatched = GPIO.HIGH
watched = GPIO.LOW

gui = True
print("argv:", sys.argv)
if sys.argv[1] == 'nogui':
  gui = False
GPIO.setmode(GPIO.BOARD)
iopin = 40

GPIO.setup(iopin, GPIO.OUT)
GPIO.output(iopin, unwatched)

# Create the haar cascade
__location__ = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__)))

faceCascade = cv2.CascadeClassifier(os.path.join(__location__, "haarcascade_frontalface_default.xml"))

# initialize the camera and grab a reference to the raw camera capture
cam = cv2.VideoCapture(0)
#cam.set(3, 320)
#cam.set(4, 240)
# allow the camera to warmup
time.sleep(0.1)

lastWatched = -10
lastOutput = unwatched

while True:
  ret_val, image = cam.read()
  image = cv2.flip(image, 1)
  thisTime = time.time()
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Detect faces in the image
  faces = faceCascade.detectMultiScale(
  gray,
  scaleFactor=1.1,
  minNeighbors=5,
  minSize=(30, 30),
  flags = cv2.CASCADE_SCALE_IMAGE
  )
  #print(time.time()*1000.0-lastTime," Found {0} faces!".format(len(faces)))
  
  # Draw a rectangle around the faces
  for (x, y, w, h) in faces:
    cv2.circle(image, (int(x+w/2), int(y+h/2)), int((w+h)/3), (255, 255, 255), 1)
  if len(faces) > 0:
    lastWatched = thisTime
  timeSinceWatched = thisTime - lastWatched
  
  watchSeconds = 1.0
  if lastOutput != watched:
    if timeSinceWatched < watchSeconds:
      print("watched! will not boil")
      GPIO.output(iopin, watched)
      lastOutput = watched
  elif lastOutput != unwatched:
    if timeSinceWatched >= watchSeconds:
      print("it's been a while... will boil")
      GPIO.output(iopin, unwatched)
      lastOutput = unwatched

  if gui: 
    cv2.imshow("Frame", image)
    if cv2.waitKey(1) == 27:
      break
        
if gui: 
  cv2.destroyAllWindows()
        

