
import cv2
import numpy as np


def main():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    # Read the input image
    img = cv2.imread('test_images/getty_517194189_373099.jpeg')

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    print('Number of detected faces:', len(faces))
    
    # loop over the detected faces
    all_eyes = []
    rotated_eyes = []
    original_eye_centers = []

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        # detects eyes of within the detected face area (roi)
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # draw a rectangle around eyes
        for (ex,ey,ew,eh) in eyes:
            cropped_eye = roi_color[ey:(ey + eh), ex:(ex+ew)]
            # print("eye height:", len(cropped_eye), "eye width:", len(cropped_eye[0]))
            ox, oy = (x + ex + (ew // 2)), (y + ey + (eh // 2))
            original_eye_centers.append((ox, oy))
            all_eyes.append(cropped_eye)
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
    
    for eye in all_eyes:
        h, w = len(eye), len(eye[0])
        cr = (w // 2, h // 2)
        degree = 45
        scale = 1
        M = cv2.getRotationMatrix2D(cr, degree, scale)
        rotated_eye = cv2.warpAffine(eye,M,(w,h))
        rotated_eyes.append(rotated_eye)
    
    
    for i, center in enumerate(original_eye_centers):
        this_eye = rotated_eyes[i]
        ew, eh = len(this_eye[0]) // 2, len(this_eye) // 2
        x, y = center[0], center[1]
        try:
            sub_img = img[y-eh:y+eh, x-ew:x+ew]
            replacer = [[[0,0,0] for i in range(len(sub_img[0]))] for j in range(len(sub_img))]

            for row in range(len(sub_img)):
                for col in range(len(sub_img[0])):
                    original_val, new_val = sub_img[row][col], this_eye[row][col]
                    
                    if new_val.all() < original_val.all():
                        replacer[row][col] = original_val
                    else: 
                        replacer[row][col][0] = new_val[0]
                        replacer[row][col][1] = new_val[1]
                        replacer[row][col][2] = new_val[2]

            
            replacer = np.array(replacer)
            img[y-eh:y+eh, x-ew:x+ew] = replacer
            # cv2.imshow('to replace',sub_img)
            # cv2.imshow('replacer', replacer)

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # img[y-eh:y+eh, x-ew:x+ew] = this_eye
        except:
            continue




    # display the image with detected eyes
    cv2.imshow('Eyes Detection',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()