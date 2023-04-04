from ast import List
import cv2
import numpy as np


class EyeData:
    ox = 0
    oy = 0
    eye_img = []

    def __init__(self, original_image_x, original_image_y, cropped_eye) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.eye_img = cropped_eye


class Filter:

    def __init__(self, image_url) -> None:
        self.color_img = cv2.imread(image_url)
        self.gray_img = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2GRAY)
        self.modified_img = cv2.imread(image_url)


    def get_faces(self):
        """Finds all detectable faces in our image"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_img, 1.1, 4)
        return faces


    def get_eyes(self, face):
        """Finds all detecablt eyes in a given face"""
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        
        (x,y,w,h) = face
        roi_gray = self.gray_img[y:y+h, x:x+w]
        roi_color = self.color_img[y:y+h, x:x+w]
        
        # detects eyes of within the detected face area (roi)
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # draw a rectangle around eyes (expected 2)
        detected_eye_information = []
        for (ex,ey,ew,eh) in eyes:
            cropped_eye = roi_color[ey:(ey + eh), ex:(ex+ew)]
            # coordinates in original image where eye is
            ox, oy = (x + ex + (ew // 2)), (y + ey + (eh // 2))
            data = EyeData(cropped_eye=cropped_eye, original_image_x=ox, original_image_y=oy)
            detected_eye_information.append(data)
        
        return detected_eye_information
    
    
    def rotateEye(self, eye, degree, scale):
        """Takes in an eye (img) and rotates it and scales it up as specified"""
        h, w = len(eye), len(eye[0])
        cr = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(cr, degree, scale)
        rotated_eye = cv2.warpAffine(eye, M, (w, h))
        return rotated_eye


    def drawEye(self, eye_info: EyeData):
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


    def applyEyeFilter(self, scale, rotation):
        """Applys a rotation and scale filter to all detectable eyes in the image"""
        faces = self.get_faces()

        for face in faces:
            eyes = self.get_eyes(face)

            for i, eye in enumerate(eyes):
                if i % 2 == 1:
                    rotated_eye = self.rotateEye(eye.eye_img, rotation, scale)
                    eye.eye_img = rotated_eye
                    self.drawEye(eye)
                else:
                    rotated_eye = self.rotateEye(eye.eye_img, -rotation, scale)
                    eye.eye_img = rotated_eye
                    self.drawEye(eye)
        
          