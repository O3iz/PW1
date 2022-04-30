import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO

in1 = 4
in2 = 17
in3 = 27
in4 = 22
enA = 23
enB = 24
temp1 = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p1 = GPIO.PWM(enA, 1000)
p1.start(50)
p2 = GPIO.PWM(enB, 1000)
p2.start(50)

cap = cv.VideoCapture(0)
cap.set(3, 256)
cap.set(4, 144)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def followLine(contours, frame):
    c = max(contours, key = cv.contourArea)
    M = cv.moments(c)
    if M["m00"]!=0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print("CX: " + str(cx) + "CY: "+str(cy))
        if cx >= 200:
            print("Turn Left")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            p1.start(35)
            p2.start(25) 
           
            

        if cx < 200 and cx > 64:
            print("On Track")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            p1.start(45)
            p2.start(45)
            
            
        if cx <= 64:
            print("Turn Right")
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            p1.start(25)
            p2.start(35)
            
            

        cv.circle( frame,(cx,cy),5,(255,255,255),-1 )

    cv.drawContours(frame, c, -1, (0,255,0),1)

while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 0)
    #convert the frame into grayscale image
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Set range for red color and 
    # define mask
    #red_lower = np.array([150, 100, 50], np.uint8)
    #red_upper = np.array([179, 255, 170], np.uint8)
    #red_mask = cv.inRange(hsvFrame, red_lower, red_upper)

    # Set range for yellow color and
    # define mask
    #yellow_lower = np.array([15, 92 , 80], np.uint8)
    #yellow_upper = np.array([41, 255, 148], np.uint8)
    #yellow_mask = cv.inRange(hsvFrame, yellow_lower, yellow_upper)
    
    # Set range for green color and 
    # define mask
    green_lower = np.array([71, 120, 51], np.uint8)
    green_upper = np.array([90, 255, 170], np.uint8)
    green_mask = cv.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([100, 120, 61], np.uint8)
    blue_upper = np.array([120, 255, 150], np.uint8)
    blue_mask = cv.inRange(hsvFrame, blue_lower, blue_upper)
    
    #Set range for black line
    low_b = 0
    high_b = 60
    black_mask = cv.inRange(gray, low_b, high_b)
    
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
    
    # For red color
    #red_mask = cv.dilate(red_mask, kernal)
    #res_red = cv.bitwise_and(frame, frame, 
                            #mask = red_mask)

    # For yellow color
    #yellow_mask = cv.dilate(yellow_mask, kernal)
    #res_yellow = cv.bitwise_and(frame, frame, 
                            #mask = yellow_mask)

    # For green color
    green_mask = cv.dilate(green_mask, kernal)
    res_green = cv.bitwise_and(frame, frame,
                               mask = green_mask)
    
    # For blue color
    blue_mask = cv.dilate(blue_mask, kernal)
    res_blue = cv.bitwise_and(frame, frame,
                            mask = blue_mask)

    #For black color
    black_mask = cv.dilate(black_mask, kernal)

    # Creating contour to track red color
    #contours1, hierarchy1 = cv.findContours(red_mask,
                                        #cv.RETR_TREE,
                                        #cv.CHAIN_APPROX_SIMPLE)[-2:]
    
   # for pic, contour in enumerate(contours1):
        #area = cv.contourArea(contour)
        #if(area > 300):
            #x, y, w, h = cv.boundingRect(contour)
            #frame = cv.rectangle(frame, (x, y), 
                                    #(x + w, y + h),
                                    #(0, 0, 255), 2)

            #cv.putText(frame, "Red Colour", (x, y),
                        #cv.FONT_HERSHEY_SIMPLEX, 1.0,
                        #(0, 0, 255))    

    # Creating contour to track yellow color
    #contours2, hierarchy2 = cv.findContours(yellow_mask,
                                        #cv.RETR_TREE,
                                        #cv.CHAIN_APPROX_SIMPLE)[-2:]
    
    #for pic, contour in enumerate(contours2):
        #area = cv.contourArea(contour)
        #if(area > 300):
            #x, y, w, h = cv.boundingRect(contour)
            #frame = cv.rectangle(frame, (x, y), 
                                    #(x + w, y + h), 
                                    #(255, 255, 0), 2)

            #cv.putText(frame, "Yellow Colour", (x, y), 
                         #cv.FONT_HERSHEY_SIMPLEX, 1.0,
                        #(255, 255, 0))    

    # Creating contour to track green color
    contours3, hierarchy3 = cv.findContours(green_mask,
                                        cv.RETR_TREE,
                                        cv.CHAIN_APPROX_SIMPLE)[-2:]
    
    for pic, contour in enumerate(contours3):
        area = cv.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv.boundingRect(contour)
            frame = cv.rectangle(frame, (x, y), 
                                    (x + w, y + h),
                                    (0, 255, 0), 2)

            cv.putText(frame, "Green Colour", (x, y),
                        cv.FONT_HERSHEY_SIMPLEX, 
                        1.0, (0, 255, 0))

                        # Creating contour to track blue color
    contours4, hierarchy4 = cv.findContours(blue_mask,
                                        cv.RETR_TREE,
                                        cv.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours4):
        area = cv.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv.boundingRect(contour)
            frame = cv.rectangle(frame, (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)

            cv.putText(frame, "Blue Colour", (x, y),
                        cv.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))
    
    #Creating contour to track black colour
    contours5, hierarchy5 = cv.findContours(black_mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)[-2:]
    cv.imshow('Colour detected in real time', frame)
    #cv.imshow("Red mask", red_mask)

    if len(contours3) > 0:
        followLine(contours3, frame)
        contours3 = []
        print(len(contours3))
    
    #elif len(contours2) > 0:
        #followLine(contours2, frame)
        #contours2 = []
        #print(len(contours2))
    
    #elif len(contours3) > 0:
        #followLine(contours3, frame)
        #contours3 = []
        #print(len(contours3))
    
    elif len(contours4) > 0:
        followLine(contours4, frame)
        contours4 = []
        print(len(contours4))


    elif len(contours5) > 0:
        followLine(contours5, frame)
        contours5 = []
        print(len(contours5))

    else:
        print("Cant see the line")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p1.start(40)
        p2.start(40)
        
        

    if cv.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

