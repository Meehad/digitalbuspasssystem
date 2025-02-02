# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
# from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--dataset", required=True,
# 	help="path to input directory of faces + images")
# ap.add_argument("-e", "--encodings", required=True,
# 	help="path to serialized db of facial encodings")
# ap.add_argument("-d", "--detection-method", type=str, default="cnn",
# 	help="face detection model to use: either `hog` or `cnn`")
# args = vars(ap.parse_args())



def enf(fn):
# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = fn

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		print(i,imagePath)
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		print("imagepath-------",imagePath)
		name = imagePath[0]
		print("id=",name)
		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)

		image = cv2.imread(r"C:\Users\ALTHAF\PycharmProjects\digitalbuspasssystem\media/"+imagePath[1])
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordnates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model='hog')

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open('faces.pickles', "wb")
	f.write(pickle.dumps(data))
	f.close()

	# qry="SELECT photo FROM `student`"
	# res=selectall(qry)

result=[['28','althaf.jpg'],['29','saifulla.jpg']]
# qry="SELECT * FROM `face`"
# res=selectall(qry)
# for i in res:
# 	row=[i['id'],i['image']]
# 	result.append(row)
enf(result)

