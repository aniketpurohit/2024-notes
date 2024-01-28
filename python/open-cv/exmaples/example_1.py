"""
This is example file which tries to open a starry night and 
displays the image if found
"""

# import statement
import cv2 as cv
import sys 

# img or CV:MAt object creation
img = cv.imread(cv.samples.findFile('starry_night.jpg'))

# check if img is read or not
if img is None:
    print("cannot read the image")
    sys.exit('Could not read the image')

# display the image till a key is pressed
cv.imshow("Display window", img)
k = cv.waitKey(0)

# to save the image
if k == ord('s'):
    cv.imwrite("starry_night.png", img)