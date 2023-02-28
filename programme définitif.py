#importing modules

import cv2
import numpy as np
import time


#capturing video through webcam
cap=cv2.VideoCapture(0)


#create a trackbar to select the color of the leaves.
def empty():
    pass
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars',640,240)
cv2.createTrackbar("Hue Min",'TrackBars',18,179,empty)
cv2.createTrackbar("Hue Max",'TrackBars',33,179,empty)
cv2.createTrackbar("sat Min",'TrackBars',51,255,empty)
cv2.createTrackbar("sat Max",'TrackBars',255,255,empty)
cv2.createTrackbar("val Min",'TrackBars',124,255,empty)
cv2.createTrackbar("val Max",'TrackBars',255,255,empty)

init=True
start=False
while True:
    ret,frame=cap.read()
    #converting frame(BGR to HSV)
    imgHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    h_min=cv2.getTrackbarPos("Hue Min",'TrackBars')
    h_max=cv2.getTrackbarPos("Hue Max",'TrackBars')
    s_min=cv2.getTrackbarPos("sat Min",'TrackBars')
    s_max=cv2.getTrackbarPos("sat Max",'TrackBars')
    v_min=cv2.getTrackbarPos("val Min",'TrackBars')
    v_max=cv2.getTrackbarPos("val Max",'TrackBars')

    #Defining the color range of dead leaves.
    lower_dead_leaf_color=np.array([h_min,s_min,v_min])
    upper_dead_leaf_color=np.array([h_max,s_max,v_max])

    #finding the range of dead leaves color in the image (mask)
    dead_leaves=cv2.inRange(imgHSV,lower_dead_leaf_color,upper_dead_leaf_color)

    #Morphological, transformation, Dilation
    kernel = np.ones((5,5), "uint8")
    dead_leaves=cv2.dilate(dead_leaves, kernel)
    imgResult=cv2.bitwise_and(frame,frame,mask=dead_leaves)

    #Tracking the dead leaves Color
    contours,heirarchy=cv2.findContours(dead_leaves,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #Calculation of the dead leaves surface area in pixels
    cadence_du_feuille_dans_image =0

     # if init==True:
     #     print("placer s'il veut plaît devant la caméra la cadence des fueille que vous voulait la ramasser avant 10s")
     #     time.sleep(30.0)

    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>10200:
            #Recovering the color of dead leaves.
            cadence_du_feuille_dans_image+=area
            cv2.drawContours(dead_leaves, cnt,-1,(255,0,0),1)
            cv2.drawContours(frame, cnt,-1,(255,0,0),1)
            x,y,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(dead_leaves,(x,y),(w+x,h+y),(0,255,0),2)
            cv2.rectangle(frame,(x,y),(w+x,h+y),(0,255,0),2)
            cv2.putText(dead_leaves,"leaf detected",(x,y+22),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            cv2.putText(frame,"leaf detected",(x,y+22),cv2.FONT_HERSHEY_DUPLEX, 0.7, (0,0,255))

    cv2.imshow('originale image',frame)
    cv2.imshow('HSV image',imgHSV)
    cv2.imshow('dead leaves(mask)',dead_leaves)
    cv2.imshow('imgResult',imgResult)
    cv2.waitKey(1)


    print('cadence_du_feuille_dans_image = ', cadence_du_feuille_dans_image)


    if start==True:
        if cadence_du_feuille_dans_image> seuil:

            print("cadence detected")
            cap.release()
            cv2.destroyAllWindows()
            break

    if init==True:
        seuil=cadence_du_feuille_dans_image
        init=False
        start=True
        print('seuil est pris avec succés')
        time.sleep(3.0)


    if cv2.waitKey(1) & 0xFF==ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

cv2.waitKey(0)