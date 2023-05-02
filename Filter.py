import cv2
import numpy as np
from imutils import face_utils
import math
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
        
        # detected_eye_information = sorted(detected_eye_information, key=lambda x: x.ox, reverse=True)
        detected_eye_information = sorted(detected_eye_information, key=lambda x: x.ox, reverse=False)

        self.eyes = detected_eye_information
        # return detected_eye_information
    

    def rotateObject(self, my_object, degree, scale = 1):
        """Takes in an eye (img) and rotates it as specified"""
        h, w = len(my_object), len(my_object[0])
        cr = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(cr, degree, scale)
        rotated_object= cv2.warpAffine(my_object, M, (w, h))
        return rotated_object


    def get_scaled_up_eyes(self, eye_info: EyeData, scale_factor = 2):
        """Scales up a given eye image using linear interpolation"""
        w, h, z = eye_info.eye_img.shape
        bigger_eye = cv2.resize(eye_info.eye_img, dsize=(scale_factor * w, scale_factor * h), interpolation=cv2.INTER_LINEAR)
        return bigger_eye


    def drawEye(self, eye_info: EyeData):
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


    def draw_object(self, my_object, x, y):
        h, w, z = my_object.shape
        if h % 2 == 0 and w % 2 == 0:
            my_object = my_object[:-1, :-1]
            h, w, z = my_object.shape

        threshold = 5
        mask = (my_object > threshold)
        dx, dy = math.floor(w / 2), math.floor(h / 2)

        try:
            sub_img = self.color_img[y-dy:y+dy+1,x - dx:x+dx+1]
            sub_img[mask] = my_object[mask]
            self.modified_img[y-dy:y+dy+1,x - dx:x+dx+1] = sub_img            
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
                    rotated_eye = self.rotateObject(eye.eye_img, rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                else:
                    rotated_eye = self.rotateObject(eye.eye_img, -rotation)
                    eye.eye_img = rotated_eye
                    scaled_eye = self.get_scaled_up_eyes(eye, scale_factor=scale)
                    eye.eye_img = scaled_eye
                self.drawEye(eye)
    

    def apply_glasses(self, glasses):
        self.get_faces()
        
        for face in self.faces:
            self.get_eyes(face)

            try: 
                if len(self.eyes) == 2:
                    left, right = self.eyes[0], self.eyes[1]
                    dx, dy = abs(left.ox - right.ox), abs(left.oy - right.oy)
                    signed_dx, signed_dy = (left.ox - right.ox), (left.oy - right.oy)
                    theta = 360 - np.rad2deg(np.arctan(signed_dy / signed_dx))
                    x_padding = math.floor(left.eye_img.shape[0]) * 2

                    center_x, center_y = left.ox + math.floor(dx / 2), left.oy + math.floor(dy / 2)
                    glasses = self.rotateObject(glasses, theta)
                    glasses = cv2.resize(glasses, (dx + x_padding, dx + x_padding))

                    self.draw_object(glasses, center_x, center_y)
            except Exception as e:
                if glasses == None: print("cannot find sunglasses from given path")
                print(e)

    

if __name__ == "__main__":
    images = [
        "test_images/POTY-cover-tout-d827554fa3c949c59a9d494773a7c409.jpg",
        "test_images/getty_517194189_373099.jpeg",
        "test_images/Unknown.jpeg",
        "test_images/what-is-people-operations-2400x2400-20201118.jpg"
    ]

    f = Filter(image_url=images[1])
    glasses = cv2.imread("sunglasses/—Pngtree—brown tung  reflection sunglasses_5336208.png")
    f.apply_glasses(glasses)
    # f.applyEyeFilter(1, 30)
    cv2.imshow('final picture', f.modified_img)
    cv2.waitKey(0)



