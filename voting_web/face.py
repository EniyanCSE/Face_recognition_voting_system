from deepface import DeepFace
import cv2
img1 = cv2.imread('Sanjay1.jpg')
img2 = cv2.imread('Sanjay11.jpg')
result = DeepFace.verify(img1,img2)
print("Is same face: ", result["verified"])