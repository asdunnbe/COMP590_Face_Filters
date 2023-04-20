import cv2

from Filter import Filter



def main():
    vid = cv2.VideoCapture(0)
    
    while(True):
        # Capture the video frame by frame
        ret, frame = vid.read()
        frame = frame[:,::-1]

        face_filter = Filter(use_url=False, input_image=frame)
        face_filter.applyEyeFilter(1, 17)

        new_frame = face_filter.modified_img
    
        # Display the resulting frame
        cv2.imshow('frame', new_frame)
        
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