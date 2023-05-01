import cv2
import numpy as np
from imutils import face_utils
# import dlib


class EyeData:
    ox = 0
    oy = 0
    eye_img = []
    confidence = 0

    def __init__(self, original_image_x, original_image_y, cropped_eye, confidence) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.eye_img = np.array(cropped_eye)
        self.confidence = confidence


class MouthData:
    ox = 0
    oy = 0
    mouth_img = []

    def __init__(self, original_image_x, original_image_y, cropped_mouth) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.mouth_img = cropped_mouth


class Filter:

    eyes = []
    faces = []


    def __init__(self, image_url = None, use_url = True, input_image = None) -> None:
        if use_url:
            self.color_img = cv2.imread(image_url)
            self.gray_img = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
            self.modified_img = cv2.imread(image_url)
        else:
            self.color_img = input_image
            self.gray_img = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
            self.modified_img = input_image


    def get_faces(self):
        """Finds all detectable faces in our image"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_img, 1.1, 4)
        self.faces = faces
        # return faces

    #eye feature related functions
    def get_eyes(self, face):
        """Finds all detectable eyes in a given face"""
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        
        (x,y,w,h) = face
        roi_gray = self.gray_img[y:y+h, x:x+w]
        roi_color = self.color_img[y:y+h, x:x+w]
        
        # detects eyes of within the detected face area (roi)
        # eyes = eye_cascade.detectMultiScale(roi_gray, outputRejectLevels=True)
        eyes, neighbors, confidences = eye_cascade.detectMultiScale3(roi_gray, 
                                      scaleFactor=1.1,
                                      minNeighbors=5,
                                      minSize=(30, 30),
                                      flags = cv2.CASCADE_SCALE_IMAGE,
                                    outputRejectLevels = True)

        # draw a rectangle around eyes (expected 2)
        detected_eye_information = []
        for i, (ex,ey,ew,eh) in enumerate(eyes):
            cropped_eye = roi_color[ey:(ey + eh), ex:(ex+ew)]
            confidence_score = confidences[i]
            # coordinates in original image where eye is (centered coord)
            ox, oy = (x + ex + (ew // 2)), (y + ey + (eh // 2))
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
            data = EyeData(cropped_eye=cropped_eye, original_image_x=ox, original_image_y=oy, confidence=confidence_score)
            detected_eye_information.append(data)
        
        detected_eye_information = sorted(detected_eye_information, key=lambda x: x.ox, reverse=True)
        self.eyes = detected_eye_information
        # return detected_eye_information
    

    def rotateEye(self, eye, degree, scale = 1):
        """Takes in an eye (img) and rotates it as specified"""
        h, w = len(eye), len(eye[0])
        cr = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(cr, degree, scale)
        rotated_eye = cv2.warpAffine(eye, M, (w, h))
        # kernel_size = (5, 5)
        # rotated_eye = cv2.GaussianBlur(rotated_eye, kernel_size, cv2.BORDER_DEFAULT)
        return rotated_eye


    def get_scaled_up_eyes(self, eye_info: EyeData, scale_factor = 2):
        """Scales up a given eye image using linear interpolation"""
        w, h, z = eye_info.eye_img.shape
        bigger_eye = cv2.resize(eye_info.eye_img, dsize=(scale_factor * w, scale_factor * h), interpolation=cv2.INTER_LINEAR)
        return bigger_eye


    def drawEye_one(self, eye_info: EyeData):
        """Takes an eye data object and draws it on our original image by placing it at the eyes center"""
        ew, eh = len(eye_info.eye_img[0]) // 2, len(eye_info.eye_img) // 2
        x, y = eye_info.ox, eye_info.oy

        try:
            sub_img = self.color_img[y-eh:y+eh, x-ew:x+ew]
            replacer = [[[0,0,0] for _ in range(len(sub_img[0]))] for _ in range(len(sub_img))]

            for row in range(len(sub_img)):
                for col in range(len(sub_img[0])):
                    original_val, new_val = sub_img[row][col], eye_info.eye_img[row][col]
                    
                    if new_val.all() < original_val.all():
                        replacer[row][col] = original_val
                    else: 
                        replacer[row][col][0] = new_val[0]
                        replacer[row][col][1] = new_val[1]
                        replacer[row][col][2] = new_val[2]
            
            replacer = np.array(replacer)
            self.modified_img[y-eh:y+eh, x-ew:x+ew] = replacer
            
        except Exception as e:
            print(e)


    def drawEye_two(self, eye_info: EyeData):
        """Takes an eye data object and draws it on our original image by placing it at the eyes center"""
        ew, eh = len(eye_info.eye_img[0]) // 2, len(eye_info.eye_img) // 2
        x, y = eye_info.ox, eye_info.oy

        threshold = 0
        mask = (eye_info.eye_img != threshold)

        try:
            sub_img = self.color_img[y-eh:y+eh + 1, x-ew:x+ew + 1]
            # make sure dimensions line up
            if eye_info.eye_img.shape[0] < sub_img.shape[0]:
                sub_img = sub_img[:len(sub_img) - 1, :len(sub_img) - 1]
            
            sub_img[mask] = eye_info.eye_img[mask]

            # make sure dimensions line up
            if sub_img.shape[0] < (y+eh -(y-eh)+1):
                self.modified_img[y-eh:y+eh, x-ew:x+ew] = sub_img
            else: 
                self.modified_img[y-eh:y+eh + 1, x-ew:x+ew+1] = sub_img
            
        except Exception as e:
            print(e)


    def applyEyeFilter(self, scale, rotation):
        """Applys a rotation and scale filter to all detectable eyes in the image and then draws them on"""
        self.get_faces()

        for face in self.faces:
            self.get_eyes(face)
            # if there is not an even number of eyes we continue, this is to mitigate the flicker when eyes are lost and refound
            if len(self.eyes) % 2 != 0: continue
            for i, eye in enumerate(self.eyes):
                if i % 2 == 1:
                    rotated_eye = self.rotateEye(eye.eye_img, rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                    # self.drawEye(eye)
                else:
                    rotated_eye = self.rotateEye(eye.eye_img, -rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                self.drawEye_two(eye)
    


if __name__ == "__main__":
    f = Filter(image_url="test_images/getty_517194189_373099.jpeg")
    # f.get_mouths()
    # f.dlib_get_facial_features()
    faces = f.get_faces()
    for face in faces:
        f.get_mouths(face, draw=True)


