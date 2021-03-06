# import the necessary packages
from sklearn.externals import joblib
from skimage import exposure
from skimage import feature
from imutils import paths
import argparse
import imutils
import cv2
import os
from sklearn import svm



ap = argparse.ArgumentParser()
ap.add_argument("-d", "--train", required=True, help="Path to the dataset")
args = vars(ap.parse_args())

# initialize the data matrix and labels
data = []
labels = []

# loop over the image paths in the training set
for imagePath in paths.list_images(args["train"]):
	# extract the digit
	digit = imagePath.split(os.sep)[-2]

	# load the image, convert it to grayscale, and detect edges
	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=min(500, image.shape[1]))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	num = cv2.resize(gray, (64, 64))
	print 'training character'
	print digit
	'''
	edged = imutils.auto_canny(gray)

	# find contours in the edge map, keeping only the largest one which is presumed to be the digit
	(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	c = max(cnts, key=cv2.contourArea)

	# extract the digit and resize it
	(x, y, w, h) = cv2.boundingRect(c)
	num = gray[y:y + h, x:x + w]
	num = cv2.resize(num, (200, 100))
    '''
	# extract Histogram of Oriented Gradients from num
	H = feature.hog(num, orientations=9, pixels_per_cell=(10, 10),
		cells_per_block=(2, 2))
	
	# update the data and labels
	data.append(H)
	labels.append(digit)

svc = svm.SVC(kernel='linear', C=1,gamma=1).fit(data, labels)
#save trained files
joblib.dump(svc, 'trained_detector.pkl') 
