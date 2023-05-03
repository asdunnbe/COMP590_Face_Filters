import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the two images
img1 = cv2.imread('stonehead.jpg')
img2 = cv2.imread('ferry.jpg')

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Detect the edges of the object you want to copy
edges1 = cv2.Canny(gray1, 100, 200)

# Find contours of the object
contours, hierarchy = cv2.findContours(edges1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Get the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask for the object in the first image
mask = np.zeros_like(gray1)
cv2.drawContours(mask, [largest_contour], 0, 255, -1)

# Get the coordinates of the bounding box around the object
x, y, w, h = cv2.boundingRect(largest_contour)

# Extract the object from the first image
object = img1[y:y+h, x:x+w]

# Resize the object to match the size of the second image
resized_object = cv2.resize(object, (img2.shape[1], img2.shape[0]))

# Create a mask for the area where the object will be pasted in the second image
mask2 = np.zeros_like(gray2)

# Draw an octagon in the center of the mask
cx = int(img2.shape[1]/2)
cy = int(img2.shape[0]/2)
print(cx, cy, )
octagon_pts = cv2.ellipse2Poly((cx, cy), (w, h//2), 0, 0, 360, 8)
cv2.fillConvexPoly(mask2, octagon_pts, 255)

# Blend the edges of the object with the second image using the mask
result = cv2.seamlessClone(resized_object, img2, mask2, (cx, cy), cv2.NORMAL_CLONE)

# Display the result
cv2.imshow('result', result)
cv2.waitKey(0)
