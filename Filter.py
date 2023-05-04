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
    mask_original = []
    mask_current = []

    def __init__(self, original_image_x, original_image_y, cropped_eye, confidence) -> None:
        self.ox = original_image_x
        self.oy = original_image_y
        self.eye_img = np.array(cropped_eye)
        self.mask_original = self.make_mask()
        self.mask_current = self.mask_original

    def make_mask(self):
        mask = np.zeros_like(self.eye_img[...,0])
        cx, cy = int(self.eye_img.shape[1]/2), int(self.eye_img.shape[0]/2)
        a, b = int(self.eye_img.shape[0]), int(self.eye_img.shape[1] * .3)
        octagon_pts = cv2.ellipse2Poly((cx, cy), (a, b), 0, 0, 360, 1)
        cv2.fillConvexPoly(mask, octagon_pts, 255)
        mask = np.stack([mask, mask, mask], axis=2)

        return mask


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


    def rotateEye(self, eye_info: EyeData, degree, scale = 1):
        """Takes in an eye (img) and rotates it as specified"""
        eye = eye_info.eye_img
        h, w = len(eye), len(eye[0])
        cr = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(cr, degree, scale)
        rotated_eye = cv2.warpAffine(eye, M, (w, h))

        # create mask for eye
        mask = cv2.warpAffine(eye_info.mask_original, M, (w, h))

        return rotated_eye, mask


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
        bigger_mask = cv2.resize(eye_info.mask_current, dsize=(scale_factor * w, scale_factor * h), interpolation=cv2.INTER_LINEAR)

        return bigger_eye, bigger_mask


    def drawEye(self, eye_info: EyeData):
        """Takes an eye data object and draws it on our original image by placing it at the eyes center"""
        ew, eh = len(eye_info.eye_img[0]) // 2, len(eye_info.eye_img) // 2
        x, y = eye_info.ox, eye_info.oy

        try:
            sub_img = self.color_img[y-eh:y+eh, x-ew:x+ew]
            cx, cy = int(eye_info.eye_img.shape[1]/2), int(eye_info.eye_img.shape[0]/2)
            result = cv2.seamlessClone(eye_info.eye_img, sub_img, eye_info.mask_current, (cx, cy), cv2.NORMAL_CLONE)

            self.modified_img[y-eh:y+eh, x-ew:x+ew] = result

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
                    rotated_eye = self.rotateEye(eye, 360 - rotation)
                else:
                    rotated_eye = self.rotateEye(eye, 360 + rotation)

                eye.eye_img, eye.mask_current = rotated_eye = rotated_eye
                eye.eye_img, eye.mask_current = self.get_scaled_up_eyes(eye, scale_factor=scale)
                self.drawEye(eye)

        return self.modified_img
    

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

    frame = cv2.imread(images[1])
    f = Filter( use_url = False, input_image =frame)

    glasses = cv2.imread("sunglasses/—Pngtree—brown tung  reflection sunglasses_5336208.png")
    # f.apply_glasses(glasses)
    f.applyEyeFilter(1, 30)
    cv2.imshow('final picture', f.modified_img)
    cv2.waitKey(0)



