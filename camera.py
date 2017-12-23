from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#import cv2 # OpenCV for perspective transform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import misc  # For saving images as needed
import math
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v
# Define a function to perform a perspective transform
# I've used the example grid image above to choose source points for the
# grid cell in front of the rover (each grid cell is 1 square meter in the sim)
# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped
# Identify pixels above the threshold
# Figure out thresh for water
def color_thresh(img, rgb_thresh=(60, 90, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] < rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel

# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

if __name__ == "__main__":
    # Get camera image
    camera = PiCamera()
    camera.resolution = (640, 480)
    rawCap = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    #img = camera.capture('img.jpg')
    # dist, angle = to_polar_coords(rover_coords(color_thresh(image)))
    # nav_angle = np.mean(angle)
    i = 0
    for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
        binary = color_thresh(image)
        x_pix, y_pix = rover_coords(binary)
        binary = binary * 255
        print len(x_pix)
        dist, angles = to_polar_coords(x_pix, y_pix)
        nav_angle = np.clip(np.mean(angles*180/np.pi), -15, 15)
        print nav_angle
        if math.isnan(nav_angle):
              print "stop"
        elif nav_angle < 10 and nav_angle > -10:
              print "forward"
        elif nav_angle > 10:
              print "right"
        elif nav_angle < -10:
              print "left"
        
	# show the frame
        misc.imsave('/home/pi/suckss/images/img' + str(i) + '.png', image)
	misc.imsave('/home/pi/suckss/images/img_b' + str(i) + '.png', binary)
        print i
        time.sleep(1)
	#key = cv2.waitKey(0)# & 0xFF
        i+= 1
	# clear the stream in preparation for the next frame
	rawCap.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	#if key == ord("q"):
		#break
