import numpy as np
import cv2
import math
import ds
from __future__ import print_function

import cv2
from matplotlib import pyplot as plt
import numpy as np
import roslib
import sys
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32, Float64, Bool
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

import ball_tracking
import color_filter
import ContourDetection
import ds


# cv2.namedWindow("HSV")
# cv2.resizeWindow("HSV", 300, 300)
# cv2.createTrackbar("HUE Min", "HSV", 90, 179, empty)
# cv2.createTrackbar("HUE Max", "HSV", 140, 179, empty)
# cv2.createTrackbar("SAT Min", "HSV", 175, 255, empty)
# cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
# cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
# cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

# window  = ds.Window(3)


rospy.init_node('ball_tracking', anonymous=True)
class BallTracking
    def __init__(self):
        self.bridge = CvBridge()
        

        # Sending values
        self.rotation_pub = rospy.Publisher("/ball/rotationAngle", Float32, queue_size=1)
        self.ball_pub = rospy.Publisher("/ball/ballArea", Float32, queue_size=1)


        self.cap = cv2.VideoCapture(1)
        # h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        # h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        # s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        # s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        # v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        # v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

        # lower = np.array([h_min, s_min, v_min])
        # upper = np.array([h_max, s_max, v_max])

        self.rotationAngle = ds.Window(maxLen=rospy.get_param("~rotation_window_size", 5))
        self.ballArea = ds.Window(maxLen=rospy.get_param("~ball_window_size", 5))
        
    
        # cv2.imshow('image', mask)
        def main(self):
            try:
                r = rospy.Rate(rospy.get_param("~rate", 50))
                while not rospy.is_shutdown():
                    success, img = self.cap.read()
                    height, width, _ = img.shape
                        
                    center_x, center_y = width/2, height/2
                    mask = color_filter.ColorFilter(img,np.array(rospy.get_param("~lower_hsv", [0,0,0])),np.array(rospy.get_param("~higher_hsv", [0,0,0]))
                    center = ContourDetection.getContoursCenter(getContours(mask,rospy.get_param("~minArea",150)),rospy.get_param("~e",0.5))

                    self.rotationAngle=180
                    
                    if center is not None:
                        center[0]=int(center[0])
                        center[1]=int(center[1])
                        center=(center[0], center[1])
                        img=cv2.circle(img, center, 10, (0,0,255),-1)
                        rot_angle = getAngle(center, center_x, height, width)
                    self.rotationAngle.add(rot_angle)
                    self.ballArea.add(getBallArea(contour))
                    rot_data = Float32()
                    rot_data.data = self.rotationAngle.getAverage()

                    # ball_data = Float32()
                    # ball_data.data = self.contourArea.getAverage()

                    self.rotation_pub.publish(rot_data)
                    self.distance_pub.publish(getBallArea(contour))
                    # print(window.getAverage())

        # cv2.imshow('normal', img)
        
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     print("HUE min: " + str(h_min))
        #     print("HUE max: " + str(h_min))
        #     print("SAT min: " + str(s_min))
        #     print("SAT max: " + str(s_max))
        #     print("VALUE min: " + str(v_min))
        #     print("VALUE max: " + str(v_max))
        #     break

    cv2.waitKey(3)
        # Sleeps to meet specified rate
        r.sleep()
    except KeyboardInterrupt:
      print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    dvt = BallTracking()
    dvt.main()