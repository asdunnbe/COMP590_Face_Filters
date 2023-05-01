import numpy as np
import cv2
from PIL import Image, ImageDraw


def gaussian_pyramid(img, num_levels):
    lower = img.copy()
    gaussian_pyr = [lower]
    for i in range(num_levels):
        lower = cv2.pyrDown(lower)
        gaussian_pyr.append(np.float32(lower))
    return gaussian_pyr
 
def laplacian_pyramid(gaussian_pyr):
    laplacian_top = gaussian_pyr[-1]
    num_levels = len(gaussian_pyr) - 1
    
    laplacian_pyr = [laplacian_top]
    for i in range(num_levels,0,-1):
        size = (gaussian_pyr[i - 1].shape[1], gaussian_pyr[i - 1].shape[0])
        gaussian_expanded = cv2.pyrUp(gaussian_pyr[i], dstsize=size)
        laplacian = np.subtract(gaussian_pyr[i-1], gaussian_expanded )
        laplacian_pyr.append(laplacian)

    return laplacian_pyr
 
def blend(laplacian_A,laplacian_B,mask_pyr):
    LS = []
    for la,lb,mask in zip(laplacian_A,laplacian_B,mask_pyr):
        ls = lb * mask + la * (1.0 - mask)
        LS.append(ls)
    return LS

def reconstruct(laplacian_pyr):
    laplacian_top = laplacian_pyr[0]
    laplacian_lst = [laplacian_top]
    num_levels = len(laplacian_pyr) - 1

    for i in range(num_levels):
        size = (laplacian_pyr[i + 1].shape[1], laplacian_pyr[i + 1].shape[0])
        laplacian_expanded = cv2.pyrUp(laplacian_top, dstsize=size)
        laplacian_expanded = laplacian_expanded.astype(laplacian_pyr[i+1].dtype)
        laplacian_top = cv2.add(laplacian_pyr[i+1], laplacian_expanded)
        laplacian_lst.append(laplacian_top)
    return laplacian_lst

def blur_object(num_levels = 7):

    # Load the two images
    img1 = cv2.imread('test_images/Unknown.jpeg')
    # img1 = cv2.resize(img1, (1800, 1000))
    img2 = cv2.flip(img1, 0)
    # img2 = cv2.resize(img2, (1800, 1000))
 
    # Create the mask
    y1, y2, x1, x2, = 25, 70, 100, 200
    mask = np.zeros_like((img1), dtype='float32')
    mask[25:70, 100:200,:] = (1,1,1)
    # (0,0,0)

    
    # For image-1, calculate Gaussian and Laplacian
    gaussian_pyr_1 = gaussian_pyramid(img1, num_levels)
    laplacian_pyr_1 = laplacian_pyramid(gaussian_pyr_1)

    # For image-2, calculate Gaussian and Laplacian
    gaussian_pyr_2 = gaussian_pyramid(img2, num_levels)
    laplacian_pyr_2 = laplacian_pyramid(gaussian_pyr_2)

    # Calculate the Gaussian pyramid for the mask image and reverse it.
    mask_pyr_final = gaussian_pyramid(mask, num_levels)
    mask_pyr_final.reverse()

    # Blend the imagesß
    add_laplace = blend(laplacian_pyr_1,laplacian_pyr_2,mask_pyr_final)

    # Reconstruct the images
    final  = reconstruct(add_laplace)
    end = final[num_levels].astype(img1.dtype)

    # cv2.imshow('img', img1)
    cv2.imshow('img1', cv2.rectangle(img1, (x1, y1), (x2, y2), (255, 0, 0), 2))
    # cv2.imshow('img2', img2)
    cv2.imshow('img2', cv2.rectangle(img2, (x1, y1), (x2, y2), (255, 0, 0), 2))
    cv2.imshow('final', end)
    cv2.imshow('final0', cv2.rectangle(end, (x1, y1), (x2, y2), (255, 0, 0), 2))
    # print('end', end[25:70, 100:200,:])
    # print('img', img1[25:70, 100:200,:])
    # print('times2')
    # print('end', end[70:80, 140:160,:])
    # print('img', img1[70:80, 140:160,:])
    cv2.waitKey(0)



if __name__ == "__main__":
    blur_object(num_levels = 5)
