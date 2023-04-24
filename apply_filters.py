import cv2
from gui import root
from Filter import Filter


def main():

    urls = [
        'test_images/getty_517194189_373099.jpeg',
        'test_images/what-is-people-operations-2400x2400-20201118.jpg'
    ]
    face_filter = Filter(image_url=urls[0])
    face_filter.applyEyeFilter(2, 17)
    
    cv2.imshow('Original eyes', face_filter.color_img)
    cv2.imshow('Spooky eyes', face_filter.modified_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

                


if __name__ == "__main__":
    main()



        