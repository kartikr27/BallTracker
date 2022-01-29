
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_EXPOSURE,-5)
def colorFilter(img,lower, upper):
    blurred = cv2.GaussianBlur(img, (9,9), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper) 
    return mask

def getContours(mask, minArea=40):
        edges=None
        edges = cv2.Canny(mask,100, 200)
        contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        newContours = []
      
        for contour in contours:
            if cv2.contourArea(contour)>minArea:
                    newContours.append(contour)
        return newContours

def empty(a):
    pass


# trackbars for adjusting hsv
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 300, 300)
cv2.createTrackbar("HUE Min", "HSV", 89, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 130, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 16, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 105, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)


while True:
    success, img = cap.read()
    # # read trackbar positions
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
    img = cv2.drawContours(img, getContours(mask), -1, (0,255,0), 3)
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


