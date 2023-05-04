import cv2
import numpy as np
import mediapipe as mp

from Filter import Filter 


class MPSegmentation:
    """Object to create and do mediapipe selfie segmentation, more about it:"""
    def __init__(
        self,
        bg_blur_ratio: tuple = (35, 35),
        threshold: float = 0.5,
        ) -> None:
        """
        Args:
            bg_blur_ratio: (typing.Tuple) = (35, 35) - ratio to apply for cv2.GaussianBlur
            threshold: (float) = 0.5 - accuracy border threshold separating background and foreground, necessary to play to get the best results
        """
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

        self.bg_blur_ratio = bg_blur_ratio
        self.threshold = threshold


    def __call__(self, frame: np.ndarray) -> np.ndarray:
        """Main function to process selfie semgentation on each call"""
        results = self.selfie_segmentation.process(frame)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > self.threshold

        background = cv2.GaussianBlur(frame, self.bg_blur_ratio, 0)
        frame = np.where(condition, frame, cv2.resize(background, frame.shape[:2][::-1]))
 
        return frame
    
def runBlurBackground():
    print("Loading SegmentationModule ...")
    segmentationModule = MPSegmentation(threshold=0.3, bg_blur_ratio=(45, 45))
    print("Webcame in use")

    cap = cv2.VideoCapture(0)
    while cap.isOpened():  
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame = segmentationModule(cv2.flip(frame, 1))

        f = Filter(use_url = False, input_image = frame)
        frame = f.applyEyeFilter(1, 30)   

        cv2.imshow('Remove Background', frame)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    else:
        raise Exception(f"Webcam with ID (0) can't be opened")

    cap.release()

if __name__ == "__main__":
    runBlurBackground()