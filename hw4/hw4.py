import numpy as np
import cv2
import sys

def binarize(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = 1 if img[i, j] >= 128 else 0
    return new_img

def dilation(bin_img, kernel, offset=(0,0)):
    new_img = np.zeros(img.shape, np.int)
    for i in range(bin_img.shape[0]):
        for j in range(bin_img.shape[1]):
            if bin_img[i, j] > 0:
                for m in range(kernel.shape[0]):
                    for n in range(kernel.shape[1]):
                        if kernel[m, n] > 0:
                            if (i+m-offset[0]) < (bin_img.shape[0]) and (j+n-offset[1]) < (bin_img.shape[1]) and (i+m-offset[0]) >= 0 and (j+n-offset[1]) >= 0:
                                new_img[(i+m-offset[0]), (j+n-offset[1])] = 1
    return new_img

def erosion(bin_img, kernel, offset=(0,0)):
    new_img = np.zeros(img.shape, np.int)
    for i in range(bin_img.shape[0]):
        for j in range(bin_img.shape[1]):
            flag = True
            for m in range(kernel.shape[0]):
                for n in range(kernel.shape[1]):
                    if kernel[m, n] > 0:
                        if (i+m-offset[0]) > (bin_img.shape[0]-1) or (j+n-offset[1]) > (bin_img.shape[1]-1) or (i+m-offset[0]) < 0 or (j+n-offset[1]) < 0 or bin_img[i+m-offset[0], j+n-offset[1]] == 0:
                            flag = False
                            break
            if flag:
                new_img[i, j] = 1
    return new_img

def closing(bin_img, kernel):
    return erosion(dilation(bin_img, kernel), kernel)

def opening(bin_img, kernel):
    return dilation(erosion(bin_img, kernel), kernel)

def hit_and_miss(bin_img, kernel_j, kernel_k):
    return erosion(bin_img, kernel_j, offset=(2,1)) & erosion((bin_img+1)%2, kernel_k, offset=(2,1))


img = cv2.imread(sys.argv[1], 0)
bin_img = binarize(img)

kernel = np.array([0, 1, 1, 1, 0,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   0, 1, 1, 1, 0,]).reshape((5, 5))

kernel_j = np.array([0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0,
                     1, 1, 0, 0, 0,
                     0, 1, 0, 0, 0,
                     0, 0, 0, 0, 0,]).reshape((5, 5))
kernel_k = np.array([0, 0, 0, 0, 0,
                     0, 1, 1, 0, 0,
                     0, 0, 1, 0, 0,
                     0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0,]).reshape((5, 5))

cv2.imwrite('dilation.bmp', dilation(bin_img, kernel)*255)
cv2.imwrite('erosion.bmp', erosion(bin_img, kernel)*255)
cv2.imwrite('closing.bmp', closing(bin_img, kernel)*255)
cv2.imwrite('opening.bmp', opening(bin_img, kernel)*255)
cv2.imwrite('hit_and_miss.bmp', hit_and_miss(bin_img, kernel_j, kernel_k)*255)
