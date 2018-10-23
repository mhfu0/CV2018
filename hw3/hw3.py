import numpy as np
import cv2
import sys

MAX_INTENSITY = 255

def count_bins(img):
    count = np.zeros(MAX_INTENSITY + 1, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            count[img[i, j]] += 1
    return count

def equalization(img):
    new_img = np.zeros(img.shape, np.uint8)
    pixels = img.shape[0] * img.shape[1]
    
    count = count_bins(img)  # compute image histogram
    cumulative_count = count.copy()
    for i in range(len(count)):
        cumulative_count[(i+1):] += count[i]
    new_intensity = np.uint8(255. * cumulative_count / pixels)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = new_intensity[img[i, j]]
    return new_img

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1], 0)
    count = count_bins(img)
    np.savetxt('count_bins.csv', count, delimiter=',', fmt='%d')
    
    eq_img = equalization(img)
    cv2.imwrite('equalization.bmp', eq_img)
    count = count_bins(eq_img)
    np.savetxt('count_bins_eq.csv', count, delimiter=',', fmt='%d')
    
    