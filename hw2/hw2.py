import numpy as np
import cv2
import sys

MAX_INTENSITY = 255
MAX_SET_NUM = 10000

def binarize(img):
    new_img = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i, j] = 255 if img[i, j] >= 128 else 0
    return new_img

def count_bins(img):
    count = np.zeros(MAX_INTENSITY+1, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            count[img[i, j]] += 1
    return count

class UnionFind(object):
    """Union-find structure for disjoint sets. Reference:
    https://qiita.com/hukuhuku11111a1/items/1bbf67d90630552eb512
    """
    def __init__(self, size):
        self.table = [-1 for _ in range(size)]
    def find(self, x):
        while self.table[x] >= 0:
            x = self.table[x]
        return x
    def union(self, x, y):
        sx = self.find(x)
        sy = self.find(y)
        if sx != sy:
            if self.table[sx] == self.table[sy]:
                self.table[sx] += -1
                self.table[sy] = sx
            else:
                if self.table[sx] < self.table[sy]:
                    self.table[sy] = sx
                else:
                    self.table[sx] = sy

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1], 0)
    
    # Q1: binarization
    bin_img = binarize(img)
    cv2.imwrite('binary.bmp', bin_img)
    
    # Q2: histogram (plot histogram using Excel later)
    count = count_bins(img)
    np.savetxt('count_bins.csv', count, delimiter=',', fmt='%d')
    
    # Q3: connected components (4-connected)
    cur_label = 0
    label_map = np.zeros(bin_img.shape, np.int)
    union_sets = UnionFind(MAX_SET_NUM)

    # First pass
    for i in range(bin_img.shape[0]):
        for j in range(bin_img.shape[1]):
            if bin_img[i, j] != 0:
                neighbors = []
                if i > 0 and bin_img[i, j] == bin_img[i-1, j]:
                    neighbors.append(label_map[i-1, j])
                if j > 0 and bin_img[i, j] == bin_img[i, j-1]:
                    neighbors.append(label_map[i, j-1])

                if len(neighbors) == 0:
                    cur_label += 1
                    label_map[i, j] = cur_label
                else:
                    label_map[i, j] = min(neighbors)
                    if(len(neighbors) == 2):
                        union_sets.union(neighbors[0], neighbors[1])
    area_count = np.zeros(cur_label+1, np.int)
                    
    # Second pass
    for i in range(bin_img.shape[0]):
        for j in range(bin_img.shape[1]):
            if bin_img[i, j] != 0:
                label_map[i, j] = union_sets.find(label_map[i, j])
                area_count[label_map[i, j]] += 1

    # Get regions with over 500 pixels
    bounding_boxes = {}
    for i in np.where(area_count >= 500)[0]:
        # the 4-tuple represents (x1, y1, x2, y2)
        bounding_boxes[i] = [bin_img.shape[1], bin_img.shape[0], 0, 0]

    # Find boundary of bounding-box
    for i in range(bin_img.shape[0]):
        for j in range(bin_img.shape[1]):
            label = label_map[i, j]
            if label in bounding_boxes:
                if i < bounding_boxes[label][1]:
                    bounding_boxes[label][1] = i
                if i > bounding_boxes[label][3]:
                    bounding_boxes[label][3] = i

                if j < bounding_boxes[label][0]:
                    bounding_boxes[label][0] = j
                if j > bounding_boxes[label][2]:
                    bounding_boxes[label][2] = j

    drawed_img = np.dstack([bin_img, bin_img, bin_img]).astype(np.uint8)
    for i in bounding_boxes:
        # Draw boundaries
        p1 = (bounding_boxes[i][0], bounding_boxes[i][1])
        p2 = (bounding_boxes[i][2], bounding_boxes[i][3])
        cv2.rectangle(drawed_img, p1, p2, (255 ,0, 0), 2)

    cv2.imwrite('components.bmp', drawed_img)