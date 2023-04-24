import cv2
import numpy as np
from imutils import face_utils
# import dlib


class EyeData:
    ox = 0
    oy = 0
    eye_img = []

    def __init__(self, original_image_x, original_image_y, cropped_eye) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.eye_img = np.array(cropped_eye)


class MouthData:
    ox = 0
    oy = 0
    mouth_img = []

    def __init__(self, original_image_x, original_image_y, cropped_mouth) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.mouth_img = cropped_mouth


class Filter:

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
        return faces

    
    # eye feature related functions
    def get_scaled_up_eyes(self, eye_info: EyeData, scale_factor = 2):
        w, h, z = eye_info.eye_img.shape
        bigger_eye = cv2.resize(eye_info.eye_img, dsize=(scale_factor * w, scale_factor * h), interpolation=cv2.INTER_LINEAR)
        return bigger_eye
        # bigger_eye = np.resize(eye_info.eye_img, (scale_factor * h, scale_factor * w, z))
        # breakpoint()
        # cv2.imshow("Original", eye_info.eye_img)
        # cv2.imshow("Bigger", bigger_eye)
        # cv2.waitKey(0)

        # grow our original image
        # find eyes on larger image, this will give us larger eye matrices/crops
        # pair these with center coords for regular size image to draw scaled up eyes.
        


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
            # coordinates in original image where eye is (centered coord)
            ox, oy = (x + ex + (ew // 2)), (y + ey + (eh // 2))
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
            data = EyeData(cropped_eye=cropped_eye, original_image_x=ox, original_image_y=oy)
            detected_eye_information.append(data)
        
        detected_eye_information = sorted(detected_eye_information, key=lambda x: x.ox, reverse=True)

        return detected_eye_information
    
    
    def rotateEye(self, eye, degree, scale = 1):
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
                    rotated_eye = self.rotateEye(eye.eye_img, rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                    self.drawEye(eye)
                else:
                    rotated_eye = self.rotateEye(eye.eye_img, -rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                self.drawEye(eye)
        
    
    # mouth feature related functions
    def get_mouths(self, face, draw = False):
        """Finds all detectable eyes in a given face"""
        mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        (x,y,w,h) = face
        roi_gray = self.gray_img[y:y+h, x:x+w]
        roi_color = self.color_img[y:y+h, x:x+w]
        
        # detects mouths within the detected face area (roi)
        mouths = mouth_cascade.detectMultiScale(roi_gray)

        for mouth in mouths:
            for (ex,ey,ew,eh) in mouth:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # # draws a rectangle around each mouth (expected 1)
        # detected_mouth_information = []
        # for (ex,ey,ew,eh) in mouths:
        #     cropped_mouth = roi_color[ey:(ey + eh), ex:(ex+ew)]
        #     if draw: cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
        #     # coordinates in original image where mouth is (centered coord)
        #     ox, oy = (x + ex + (ew // 2)), (y + ey + (eh // 2))
        #     data = MouthData(cropped_mouth=cropped_mouth, original_image_x=ox, original_image_y=oy)
        #     detected_mouth_information.append(data)
        # if draw:
        #     cv2.imshow('Mouth Detection', self.color_img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        # return detected_mouth_information

    
    
    # def dlib_get_facial_features(self):
    #     dlib_pretrained_model_path = "shape_predictor_68_face_landmarks.dat"
    #     detector = dlib.get_frontal_face_detector()
    #     predictor = dlib.shape_predictor(dlib_pretrained_model_path)

    #     faces = detector(self.gray_img, 1)

    #     for face in faces:
    #         facial_features = predictor(self.gray_img, face)
    #         facial_features = face_utils.shape_to_np(facial_features)
    #         for x, y in facial_features:
    #             cv2.circle(self.color_img, (x, y), 1, (0, 0, 255), -1)
        
    #     cv2.imshow("Output", self.color_img)
    #     cv2.waitKey(0)



if __name__ == "__main__":
    f = Filter(image_url="test_images/getty_517194189_373099.jpeg")
    # f.get_mouths()
    # f.dlib_get_facial_features()
    faces = f.get_faces()
    for face in faces:
        f.get_mouths(face, draw=True)


