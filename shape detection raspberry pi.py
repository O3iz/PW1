import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)




def empty(x):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",25,255,empty)
cv2.createTrackbar("Area","Parameters",1000,20000,empty)

def getContours(imgDil,imgContour):
    contours,hierarchy = cv2.findContours(imgDil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2:]
    triangle = 0
    square = 0
    circle = 0
    for cnt in contours:
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        area = cv2.contourArea(cnt)


        #print(area)
        if area > areaMin:
            #print(area)
            cv2.drawContours(imgContour,cnt,-1,(255,0,255),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(imgContour,"Points: "+str(len(approx)),(x+w+20,y+20),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45),
                        cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
            edges = len(approx)

            if(edges == 3):
                cv2.putText(imgContour, "Triangle", (x + w + 20, y + 65),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
                triangle +=1
            elif(edges == 4):
                cv2.putText(imgContour, "Square", (x + w + 20, y + 65),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
                square += 1
            elif (edges == 8):
                cv2.putText(imgContour, "Circle", (x + w + 20, y + 65),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
                circle += 1
            else:
                cv2.putText(imgContour, "Unknown", (x + w + 20, y + 65),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
    x=0
    y=0
    p=0
    if(circle > 0):
        x=1
    if(square > 0):
        y=1
    if(triangle > 0):
        p=1
    print("____________")
    print("Shape types: ",x+y+p)
    print("Total no. of Shapes: ",triangle + square + circle)

    print("Triangle :",triangle ,"\nSquare_Rectangle: ", square, "\nCircle: ", circle)
while cap.isOpened():
    ret,img = cap.read()
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7,7),1)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    t1 = cv2.getTrackbarPos("Threshold1","Parameters")
    t2 = cv2.getTrackbarPos("Threshold2","Parameters")
    #print(t1,t2)
    imgCanny = cv2.Canny(imgGray,t1,t2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
    square=0
    triangle = 0
    circle = 0
    getContours(imgDil,imgContour=imgContour)

    imgGray = cv2.cvtColor(imgGray,cv2.COLOR_GRAY2BGR)
    imgCanny = cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)
    imgDil = cv2.cvtColor(imgDil,cv2.COLOR_GRAY2BGR)
    imgStack = np.hstack([img,imgContour])
    #cv2.imshow("Original Image",img)
    #cv2.imshow('Blur Image',imgBlur)
    cv2.imshow('Output',imgStack)
    cv2.imshow("edge",imgCanny)
    
   # print("triangle = " + triangle)
   # print("square = " + square)
   # print("circle = " + circle) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

