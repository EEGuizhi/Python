#4109061012 陳柏翔
import cv2
import numpy as np

def q1(img): #Request 1
    l, w, c = img.shape #長, 寬, 顏色
    new_img = np.zeros((l, w, c), np.uint8) #創建

    for i in range(int(l/2)):
        for j in range(int(w/2)):
            new_img[2*i, 2*j] = img[2*i, 2*j]

    return new_img


def q2(img): #Request 2
    l, w, c = img.shape #長, 寬, 顏色
    new_img = np.zeros((int(l/2), int(w/2), c), np.uint8) #創建

    for i in range(int(l/2)):
        for j in range(int(w/2)):
            new_img[i, j] = img[2*i, 2*j]

    return new_img


def q3(img): #Request 3
    l, w, c = img.shape #長, 寬, 顏色
    new_img = np.zeros((l*2, w*2, c), np.uint8) #創建
    X_MAX = l*2 -1
    Y_MAX = w*2 -1

    for i in range(l*2):
        for j in range(w*2):
            dx = 0.0
            dy = 0.0
            if i%2 == 1:
                dx = 0.5
            if j%2 == 1:
                dy = 0.5

            if i == X_MAX and j == Y_MAX: # X跟Y都到邊界
                f11 = img[int(i/2 - dx), int(j/2 - dy)] /4
                f12 = f11
                f21 = f11
                f22 = f11
            elif i == X_MAX: # X到邊界
                f11 = img[int(i/2 - dx), int(j/2 - dy)] /4
                f21 = img[int(i/2 - dx), int(j/2 + dy)] /4
                f12 = f11
                f22 = f21
            elif j == Y_MAX: # Y到邊界
                f11 = img[int(i/2 - dx), int(j/2 - dy)] /4
                f12 = img[int(i/2 + dx), int(j/2 - dy)] /4
                f21 = f11
                f22 = f12
            else: #內部 正常情況
                f11 = img[int(i/2 - dx), int(j/2 - dy)] /4
                f12 = img[int(i/2 + dx), int(j/2 - dy)] /4
                f21 = img[int(i/2 - dx), int(j/2 + dy)] /4
                f22 = img[int(i/2 + dx), int(j/2 + dy)] /4

            new_img[i, j] = f11 + f12 + f21 + f22
            
    return new_img


def q4(img): #Requst 4
    l, w, c = img.shape #長, 寬, 顏色
    new_img = np.zeros((l, w, c), np.uint8) #創建

    for i in range(l):
        for j in range(w):
            for k in range(c):
                level = int(img[i, j, k] / 32)
                new_img[i, j, k] = level*32

    return new_img



if __name__ == '__main__':
    img = cv2.imread("week1_Lenna.jpg") #讀入圖片
    cv2.imshow("original img", img)

    img_q1 = q1(img)
    cv2.imshow("Q1 img", img_q1)

    img_q2 = q2(img)
    cv2.imshow("Q2 img", img_q2)

    img_q3 = q3(img_q2) #丟入request 2的圖片
    cv2.imshow("Q3 img", img_q3)

    img_q4 = q4(img)
    cv2.imshow("Q4 img", img_q4)

    cv2.waitKey(0)
