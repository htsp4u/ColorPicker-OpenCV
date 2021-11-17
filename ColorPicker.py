
# Python program for Detection of a  
# specific color (wherever is clicked in the "Main" window) using OpenCV with Python
import cv2 
import numpy as np


hue = 0
sat = 0
val = 0
hsvColors = np.zeros([3,3,3])

def mouseHSV(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]
        colors = frame[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
        colored = np.uint8([[[colorsB,colorsG,colorsR ]]])
        hsvColors = cv2.cvtColor(colored,cv2.COLOR_BGR2HSV)
        # Click will track color clicked
        global hue, sat, val
        hue = hsvColors[0][0][0]
        sat = hsvColors[0][0][1]
        val = hsvColors[0][0][2]
        print ("HSV Format: ", hsvColors)
        print ("Hue:", hsvColors[0][0][0])
        print ("Saturation:", hsvColors[0][0][1])
        print ("Value:", hsvColors[0][0][2])
        

def nothing(x):
    pass
cap = cv2.VideoCapture(0)  
cv2.namedWindow('Main')
cv2.namedWindow('Options')
cv2.setMouseCallback('Main', mouseHSV)
cv2.createTrackbar('Tolerance', 'Options', 0, 255, nothing)
# cv2.createTrackbar('Low Hue','HSV Range',0,255,nothing)
# cv2.createTrackbar('Upper Hue','HSV Range',0,255,nothing)
# cv2.createTrackbar('Low Sat','HSV Range',0,255,nothing)
# cv2.createTrackbar('Upper Sat','HSV Range',0,255,nothing)
# cv2.createTrackbar('Low Val','HSV Range',0,255,nothing)
# cv2.createTrackbar('Upper Val','HSV Range',0,255,nothing)

kernel = np.ones((5,5), np.uint8) 
extra = 25
cv2.setTrackbarPos('Tolerance', 'Options', extra)
while(1):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()  
    # Converts frames from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # lhue = cv2.getTrackbarPos('Low Hue','HSV Range')
    # hhue = cv2.getTrackbarPos('Upper Hue','HSV Range')
    # lsat = cv2.getTrackbarPos('Low Sat','HSV Range')
    # hsat = cv2.getTrackbarPos('Upper Sat','HSV Range')
    # lval = cv2.getTrackbarPos('Low Val','HSV Range')
    # hval = cv2.getTrackbarPos('Upper Val','HSV Range')

    #lower_hsv = np.array([lhue,lsat,lval])
    #upper_hsv = np.array([hhue,hsat,hval])

    # Adjustment slider for tolerance of colors
    extra = cv2.getTrackbarPos('Tolerance', 'Options')

    # Click will track color clicked
    lower_hsv = np.array([(hue-extra),(sat-extra),(val-extra)])
    upper_hsv = np.array([(hue+extra),(sat+extra),(val+extra)])
    
    # Show only stuff in range of vals
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv) 

    # Dilate and erode to clean up
    dilation = cv2.dilate(mask, kernel, iterations=1) 
    erosion = cv2.erode(dilation, kernel, iterations=1) 
    
    # The bitwise and of the frame and mask is done so  
    # that only the in range things are white
    res = cv2.bitwise_and(frame,frame, mask= mask)     
    cv2.imshow('mask',mask)
    cv2.imshow('Erosion',erosion)
    cv2.imshow('res',res)    
    cv2.imshow('Main',frame) 
    
    key = cv2.waitKey(1) 
    if key == ord('q'): 
        break
  
# Destroys all of the HighGUI windows. 
cv2.destroyAllWindows() 
  
# release the captured frame 
cap.release() 
