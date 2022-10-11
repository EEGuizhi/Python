# 4109061012 陳柏翔
import cv2
import numpy as np

def ToBinary(img):
    l, w = img.shape
    T = np.max(img) / 4
    for i in range(l):
        for j in range(w):
            if img[i, j] > T:
                img[i, j] = 255
            else:
                img[i, j] = 0
    return img


def dilation(img):
    KERNAL = [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]]
    l, w = img.shape
    img = np.insert(img, l, 0, 0)  # 周圍補零
    img = np.insert(img, 0, 0, 0)
    img = np.insert(img, w, 0, 1)
    img = np.insert(img, 0, 0, 1)
    new_img = np.zeros((l, w))
    for y in range(l):
        for x in range(w):
            value = np.sum(KERNAL*img[y:y+3, x:x+3])
            if value >= 255:
                new_img[y, x] = 255
            else:
                new_img[y, x] = 0
    return new_img


def erosion(img):
    KERNAL = [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]]
    l, w = img.shape
    new_img = np.zeros((l, w))
    for y in range(l-2):
        for x in range(w-2):
            value = np.sum(KERNAL*img[y:y+3, x:x+3])
            if value == 255*9:
                new_img[y+1, x+1] = 255
            else:
                new_img[y+1, x+1] = 0
    return new_img


def find_edge(l_img, s_img):
    new_img = l_img - s_img
    return new_img


if __name__ == "__main__":
    PATH = "week_4\morphology_1.png"
    img = cv2.imread(PATH, 0)

    # Requset 1: Transfer the image to binary image.
    img = ToBinary(img)
    cv2.imshow("origin", img)

    # Request 2: Complete dilation and erosion with 3 * 3 structure element.
    img_dilation = dilation(img)
    cv2.imshow("dilation", img_dilation)
    img_erosion = erosion(img)
    cv2.imshow("erosion", img_erosion)

    # Request 3: Complete open and close based on dilation and erosion.
    img_open = dilation(erosion(img))
    cv2.imshow("open", img_open)
    img_close = erosion(dilation(img))
    cv2.imshow("close", img_close)

    # Request 4: Find edge with 1 ~ 3 methods.
    img_edge1 = find_edge(img_dilation, img_close)
    cv2.imshow("edge 1", img_edge1)
    img_edge2 = find_edge(img_open, img_erosion)
    cv2.imshow("edge 2", img_edge2)
    

    cv2.waitKey(0)
