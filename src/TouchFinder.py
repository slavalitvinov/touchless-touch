import sys
from PIL import Image
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

class TouchFinder:
    def __init__(self):
        None

    def find(self,image):
        # B G R
        # good: 148, 166, 253
        lower_red = np.array([  0,  0,235])
#        upper_red = np.array([192,192,255])
        upper_red = np.array([155,155,255])
        # create a mask image
        mask = cv2.inRange(image, lower_red, upper_red)

        #cv2.imshow("Keypoints", mask); cv2.waitKey(0)

        output_image = image.copy()
#        output_image[np.where(mask==0)] = 255
#        output_image[np.where(mask>=10)] = 255
        output_image[np.where(mask==0)] = 0              # garbage

        #cv2.imshow("Keypoints", output_image); cv2.waitKey(0)
        
        params = cv2.SimpleBlobDetector_Params()
        params.minDistBetweenBlobs = 20.0
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByColor = False
        params.filterByCircularity = False
        params.filterByArea = True
        params.minArea = 100.0
        params.maxArea = 500.0
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(output_image)
#        return keypoints
        points = [ kp.pt for kp in keypoints ]
        return points

#         image = output_image
#         im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#   
#         cv2.imshow("Keypoints", im_with_keypoints)
#         cv2.waitKey(0)
#         print points
#         return points

if __name__ == "__main__":
    image_filename = 'C:/Users/Slava/workspace/touchless-touch/resource/test-image.png'
    image = cv2.imread(image_filename)
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    f = TouchFinder()
    points = f.find(image)
    print( "found:" + str(len(points)))

    image_with_keypoints = cv2.drawKeypoints(image, points, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Keypoints", image_with_keypoints)
    cv2.waitKey(0)

    
    assert len(points) == 4, "points are detected"
    print( points )