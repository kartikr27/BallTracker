import cv2
import color_filter
import rospy
class ContourDetection:
    def __init__(self, image, minArea = rospy.get_param("~min_area", 150),e = rospy.get_param("~min_area", 0.5)):
        self.mask = image
        self.minArea = minArea
        self.eccen = e
    def getContours(self):
        def getContours(mask, minArea, e):
        edges = cv2.Canny(mask,100, 200)
        contours, _= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        newContours = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, .03*cv2.arcLength(contour, True), True)
            eccen = eccentricity(contour)<e
            if cv2.contourArea(contour)>minArea and eccen and len(approx)>6:
                newContours.append(contour)
            if cv2.contourArea(contour)>400:
                newContours.append(contour)
        if len(newContours)==0:
            return None
        newContours=sorted(newContours, key=cv2.contourArea, reverse=False)
        return newContours[len(newContours)-1]

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