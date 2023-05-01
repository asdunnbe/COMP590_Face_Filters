import cv2

from Filter import Filter


def main():
    vid = cv2.VideoCapture(0)
    glasses = cv2.imread("—Pngtree—black sunglass vector on transparent_7962493.png")

    
    while(True):
        # Capture the video frame by frame
        ret, frame = vid.read()
        frame = frame[:,::-1]
        
        face_filter = Filter(use_url=False, input_image=frame)
        # good rotations -> 30, 90, 315
        # need live filter modification by having gui up with webcam
        # blur the face of others entirely? only one lucky face filter winner
        # need good lighting
        face_filter.applyEyeFilter(1, 300)

        new_frame = face_filter.modified_img
        
        # Display the resulting frame
        h, w, z = frame.shape
        glasses = cv2.resize(glasses, (w, h))
        # breakpoint()
        new_frame = cv2.add(new_frame, glasses)
        
        cv2.imshow('frame', new_frame)
        # cv2.imshow('frame', glasses)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()