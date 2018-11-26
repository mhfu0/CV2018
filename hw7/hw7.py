import cv2
import numpy as np
import sys

def binarize(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = 1 if img[i, j] > 127 else 0
    return new_img

class YokoiNumber(object):
    def __init__(self, bin_image):
        self.bin_image = bin_image
        self.size = bin_image.shape
        self.yokoi_array = None
        
    def h(self, b, c, d, e):
        if b == c and (d != b or e != b): return 'q'
        elif b == c and (d == b and e == b): return 'r'
        else: return 's'
    
    def f(self, a1, a2, a3, a4):
        a_tuple = [a1, a2, a3, a4]
        if all([a == 'r' for a in a_tuple]): return 5
        else: return sum([int(a == 'q') for a in a_tuple])
    
    def iterate(self):
        self.yokoi_array = -np.ones(self.size, np.int)
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                if self.bin_image[r, c] == 0:
                    continue
                
                # define neighborhood from x0 to x8
                x0 = self.bin_image[r, c]
                x1 = self.bin_image[r, c+1] if c != self.size[1]-1 else 0
                x2 = self.bin_image[r-1, c] if r != 0 else 0
                x3 = self.bin_image[r, c-1] if c != 0 else 0
                x4 = self.bin_image[r+1, c] if r != self.size[0]-1 else 0
                x5 = self.bin_image[r+1, c+1] if r != self.size[0]-1 and c != self.size[1]-1 else 0
                x6 = self.bin_image[r-1, c+1] if r != 0 and c != self.size[1]-1 else 0
                x7 = self.bin_image[r-1, c-1] if r != 0 and c != 0 else 0
                x8 = self.bin_image[r+1, c-1] if r != self.size[0]-1 and c != 0 else 0
                
                # calculate h value
                a1 = self.h(x0, x1, x6, x2)
                a2 = self.h(x0, x2, x7, x3)
                a3 = self.h(x0, x3, x8, x4)
                a4 = self.h(x0, x4, x5, x1)
                
                self.yokoi_array[r, c] = self.f(a1, a2, a3, a4)

class PairRelationship(object):
    def __init__(self, img):
        self.img = img
        self.size = img.shape
        self.res = np.zeros(self.size, np.int).astype(str)
    def h(self, a, m):
        return 1 if a == m else 0
    def iterate(self):
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                if self.img[r, c] > 0:
                    x1 = self.img[r, c+1] if c < self.size[1] - 1 else '0'
                    x2 = self.img[r-1, c] if r > 0 else '0'
                    x3 = self.img[r, c-1] if c > 0 else '0'
                    x4 = self.img[r+1, c] if r < self.size[0] - 1 else '0'

                    i_sum = sum([self.h(x, 1) for x in (x1, x2, x3, x4)])
                    cond = i_sum < 1 or self.img[r, c] != 1
                    self.res[r, c] = 'q' if cond else 'p'

class Thinning(object):
    def __init__(self, img):
        self.size = img.shape
        self.img = img
        
    def h(self, b, c, d, e):
        if b == c and (d != b or e != b): return 'q'
        elif b == c and (d == b and e == b): return 'r'
        else: return 's'
        
    def f(self, a1, a2, a3, a4):
        a_tuple = [a1, a2, a3, a4]
        if all([a == 'r' for a in a_tuple]): return 5
        else: return sum([int(a == 'q') for a in a_tuple])
        
    def step(self):
        yokoi = YokoiNumber(self.img)
        yokoi.iterate() 
        prmark = PairRelationship(yokoi.yokoi_array)
        prmark.iterate()
        
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                if self.img[r, c] == 0: continue
                # define neighborhood from x0 to x8
                x0 = self.img[r, c]
                x1 = self.img[r, c+1] if c != self.size[1]-1 else 0
                x2 = self.img[r-1, c] if r != 0 else 0
                x3 = self.img[r, c-1] if c != 0 else 0
                x4 = self.img[r+1, c] if r != self.size[0]-1 else 0
                x5 = self.img[r+1, c+1] if r != self.size[0]-1 and c != self.size[1]-1 else 0
                x6 = self.img[r-1, c+1] if r != 0 and c != self.size[1]-1 else 0
                x7 = self.img[r-1, c-1] if r != 0 and c != 0 else 0
                x8 = self.img[r+1, c-1] if r != self.size[0]-1 and c != 0 else 0
                # calculate h value
                a1 = self.h(x0, x1, x6, x2)
                a2 = self.h(x0, x2, x7, x3)
                a3 = self.h(x0, x3, x8, x4)
                a4 = self.h(x0, x4, x5, x1)
                cond = self.f(a1, a2, a3, a4) == 1 and prmark.res[r, c] == 'p'
                self.img[r, c] = 0 if cond else 1
                
    def iterate(self):
        for l in range(20):
            self.step()

if __name__ == '__main__':
    image = cv2.imread(sys.argv[1], 0)
    downsampled_image = image[::8, ::8]

    bin_image = binarize(downsampled_image)

    thinning = Thinning(bin_image)
    thinning.iterate()
    
    cv2.imwrite('thinning.bmp', thinning.img * 255)
    