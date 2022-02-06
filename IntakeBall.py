
import numpy as np
import cv2
import math

cap = cv2.VideoCapture(1)


def get_x_offset(x, wanted_x):
    return x - (wanted_x)


def getAngle(center, center_x, height, width):
    angle = (math.atan2(get_x_offset(center[0], center_x),  height))*180/math.pi % 360.0
    if angle>180:
        angle= 360-angle
    if center[0]>=width/2:
        return angle
    else:
        return -angle
    
def colorFilter(img,lower, upper):
    blurred = cv2.GaussianBlur(img,(11,11),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper) 
    kernel=np.ones((10,10),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

def getContours(mask, minArea, e):
    edges = cv2.Canny(mask,100, 200)
    contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    newContours = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, .03*cv2.arcLength(contour, True), True)
        eccen = eccentricity(contour)<e
        if cv2.contourArea(contour)>minArea and eccen and len(approx)>1:
            newContours.append(contour)
    if len(newContours)==0:
        return None
    newContours=sorted(newContours, key=cv2.contourArea, reverse=False)
    return newContours[0]

def getContoursCenter(contour):
    x1=0
    y1=0
    M = cv2.moments(contour)
    if M["m00"] !=0:
        x1 = int(M["m10"] / M["m00"])
        y1 = int(M["m01"] / M["m00"])
    else:
        return None
    return [x1, y1]

def eccentricity(contour):
    try:
        (_, _), (MA, ma), _ = cv2.fitEllipse(contour)
        a = ma / 2
        b = MA / 2
        ecc = np.sqrt(a ** 2 - b ** 2) / a
    except Exception:
        ecc=1
    return ecc

def empty(a):
    pass


# trackbars for adjusting hsv
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 300, 300)
cv2.createTrackbar("HUE Min", "HSV", 96, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 140, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 198, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)


while True:
    success, img = cap.read()
    # read trackbar positions
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # color mask
    mask = colorFilter(img,lower,upper)
  
    cv2.imshow('image', mask)

    
    # img = cv2.drawContours(img, getContours(mask, 100, .5), -1, (0,255,0), 3)
    # img = cv2.drawContours(img, getContoursCenter(mask, 100, .5), 0, (0,255,0), 5)
    height, width, _ = img.shape
        
    center_x, center_y = width/2, height/2
    
    center = getContoursCenter(getContours(mask,100,0.5))

    angle=180
    
    if center is not None:
        center[0]=int(center[0])
        center[1]=int(center[1])
        center=(center[0], center[1])
        img=cv2.circle(img, center, 10, (0,0,255),-1)
        angle = getAngle(center, center_x, height, width)
    print(angle)

    cv2.imshow('normal', img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("HUE min: " + str(h_min))
        print("HUE max: " + str(h_min))
        print("SAT min: " + str(s_min))
        print("SAT max: " + str(s_max))
        print("VALUE min: " + str(v_min))
        print("VALUE max: " + str(v_max))
        break



cv2.destroyAllWindows()


