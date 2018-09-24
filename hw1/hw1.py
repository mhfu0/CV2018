import numpy as np
import cv2

def upside_down(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = img[img.shape[0] - 1 - i, j]
    return new_img

def right_side_left(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = img[i, img.shape[1] - 1 - j]
    return new_img

def diagonal_mirror(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = img[img.shape[0] - 1 - i, img.shape[1] - 1 - j]
    return new_img

if __name__ == '__main__':
    img = cv2.imread('lena.bmp', 0)
    cv2.imwrite('upside_down.bmp', upside_down(img))
    cv2.imwrite('right_side_left.bmp', right_side_left(img))
    cv2.imwrite('diagonal_mirror.bmp', diagonal_mirror(img))