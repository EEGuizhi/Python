# 4109061012 陳柏翔
import cv2
import numpy as np


def get_gauss_kernal(dev, size):
    if size%2 == 0 or size<3:
        print("===========\n Error \n===========")
        raise

    kernal = np.zeros((size, size))
    s = (size-1)/2
    for i in range(size):
        for j in range(size):
            kernal[i, j] = -((i-s)**2+(j-s)**2)/(2*(dev**2))
    kernal = np.exp(kernal)/(2*np.pi*(dev**2))
    return kernal


def blurring(kernal, img):
    ksize, ksize = kernal.shape  # Kernal Size
    s = int((ksize-1)/2)
    try:  # 彩色
        l, w, c = img.shape  # Size, Color
        for i in range(s):
            img = np.insert(img, 0, [0, 0, 0], axis=1)
            img = np.insert(img, 0, [0, 0, 0], axis=0)
            img = np.insert(img, w+1+i, [0, 0, 0], axis=1)
            img = np.insert(img, l+1+i, [0, 0, 0], axis=0)  # 周圍補零

        new_img = np.zeros((l, w, c), np.uint8)  # 創建

        for i in range(s, l+s):
            for j in range(s, w+s):
                if i == s and j == s:  # n=分母
                    n = np.sum(kernal[s:ksize, s:ksize])
                elif i == s and j == w+s-1:
                    n = np.sum(kernal[s:ksize, 0:s+1])
                elif i == l+s-1 and j == s:
                    n = np.sum(kernal[0:s+1, s:ksize])
                elif i == l+s-1 and j == w+s-1:
                    n = np.sum(kernal[0:s+1, 0:s+1])
                elif i == s:
                    n = np.sum(kernal[s:ksize, 0:ksize])
                elif j == s:
                    n = np.sum(kernal[0:ksize, s:ksize])
                elif i == l+s-1:
                    n = np.sum(kernal[0:s+1, 0:ksize])
                elif j == w+s-1:
                    n = np.sum(kernal[0:ksize, 0:s+1])
                else:
                    n = np.sum(kernal)
                k = kernal / n
                new_img[i-s, j-s] = [np.sum(k*img[i-s:i+s+1, j-s:j+s+1, 0]),
                                     np.sum(k*img[i-s:i+s+1, j-s:j+s+1, 1]),
                                     np.sum(k*img[i-s:i+s+1, j-s:j+s+1, 2])]  # RGB
    except:  # 黑白
        l, w = img.shape  # Size
        for i in range(s):
            img = np.insert(img, 0, 0, axis=1)
            img = np.insert(img, 0, 0, axis=0)
            img = np.insert(img, w+1+i, 0, axis=1)
            img = np.insert(img, l+1+i, 0, axis=0)  # 周圍補零

        new_img = np.zeros((l, w), np.uint8)  # 創建

        for i in range(s, l+s):
            for j in range(s, w+s):
                if i == s and j == s:  # n=分母
                    n = np.sum(kernal[s:ksize, s:ksize])
                elif i == s and j == w+s-1:
                    n = np.sum(kernal[s:ksize, 0:s+1])
                elif i == l+s-1 and j == s:
                    n = np.sum(kernal[0:s+1, s:ksize])
                elif i == l+s-1 and j == w+s-1:
                    n = np.sum(kernal[0:s+1, 0:s+1])
                elif i == s:
                    n = np.sum(kernal[s:ksize, 0:ksize])
                elif j == s:
                    n = np.sum(kernal[0:ksize, s:ksize])
                elif i == l+s-1:
                    n = np.sum(kernal[0:s+1, 0:ksize])
                elif j == w+s-1:
                    n = np.sum(kernal[0:ksize, 0:s+1])
                else:
                    n = np.sum(kernal)
                k = kernal / n
                new_img[i-s, j-s] = np.sum(k*img[i-s:i+s+1, j-s:j+s+1])
    return new_img


def median_blurring(img):
    l, w, c = img.shape  # Size, Color
    new_img = np.zeros((l, w, c), np.uint8)  # 創建

    for i in range(l):
        for j in range(w):
            if i == 0 and j == 0:  # 3x3
                new_img[i, j] = [np.median(img[0:2, 0:2, 0]), \
                                 np.median(img[0:2, 0:2, 1]), \
                                 np.median(img[0:2, 0:2, 2])]
            elif i == 0 and j == w-1:
                new_img[i, j] = [np.median(img[0:2, j-1:w, 0]), \
                                 np.median(img[0:2, j-1:w, 1]), \
                                 np.median(img[0:2, j-1:w, 2])]
            elif i == l-1 and j == 0:
                new_img[i, j] = [np.median(img[i-1:l, 0:2, 0]), \
                                 np.median(img[i-1:l, 0:2, 1]), \
                                 np.median(img[i-1:l, 0:2, 2])]
            elif i == l-1 and j == w-1:
                new_img[i, j] = [np.median(img[i-1:l, j-1:w, 0]), \
                                 np.median(img[i-1:l, j-1:w, 1]), \
                                 np.median(img[i-1:l, j-1:w, 2])]
            elif i == 0:
                new_img[i, j] = [np.median(img[0:2, j-1:j+2, 0]), \
                                 np.median(img[0:2, j-1:j+2, 1]), \
                                 np.median(img[0:2, j-1:j+2, 2])]
            elif j == 0:
                new_img[i, j] = [np.median(img[i-1:i+2, 0:2, 0]), \
                                 np.median(img[i-1:i+2, 0:2, 1]), \
                                 np.median(img[i-1:i+2, 0:2, 2])]
            elif i == l-1:
                new_img[i, j] = [np.median(img[i-1:l, j-1:j+2, 0]), \
                                 np.median(img[i-1:l, j-1:j+2, 1]), \
                                 np.median(img[i-1:l, j-1:j+2, 2])]
            elif j == w-1:
                new_img[i, j] = [np.median(img[i-1:i+2, j-1:w, 0]), \
                                 np.median(img[i-1:i+2, j-1:w, 1]), \
                                 np.median(img[i-1:i+2, j-1:w, 2])]
            else:
                new_img[i, j] = [np.median(img[i-1:i+2, j-1:j+2, 0]), \
                                 np.median(img[i-1:i+2, j-1:j+2, 1]), \
                                 np.median(img[i-1:i+2, j-1:j+2, 2])]
    return new_img


def sobel_edge(img):  #參考原理：https://medium.com/%E9%9B%BB%E8%85%A6%E8%A6%96%E8%A6%BA/%E9%82%8A%E7%B7%A3%E5%81%B5%E6%B8%AC-%E7%B4%A2%E4%BC%AF%E7%AE%97%E5%AD%90-sobel-operator-95ca51c8d78a
    T = 150  #閥值(沒有使用)
    KERNAL_H = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    KERNAL_V = np.array([[-1,-2,-1],
                         [ 0, 0, 0],
                         [ 1, 2, 1]])
    l, w = img.shape  # Size
    img = np.insert(img, 0, img[0:l, 0], axis=1)  # 周圍補值
    img = np.insert(img, w+1, img[0:l, w], axis=1)
    img = np.insert(img, 0, img[0, 0:w+2], axis=0)
    img = np.insert(img, l+1, img[l, 0:w+2], axis=0)

    new_img = np.zeros((l, w), np.uint8)  # 創建

    for i in range(1, l+1):  # i, j從1, 1開始
        for j in range(1, w+1):
            Gx = np.sum(KERNAL_H*img[i-1:i+2, j-1:j+2])
            Gy = np.sum(KERNAL_V*img[i-1:i+2, j-1:j+2])
            Gt = (Gx**2 + Gy**2)**0.5
            new_img[i-1, j-1] = Gt  # 梯度
            # if Gt >= T:
            #     new_img[i-1, j-1] = 255
            # else:
            #     new_img[i-1, j-1] = 0
    return new_img


def laplacian_edge(img):  #參考原理：https://medium.com/%E9%9B%BB%E8%85%A6%E8%A6%96%E8%A6%BA/%E9%82%8A%E7%B7%A3%E5%81%B5%E6%B8%AC-%E6%8B%89%E6%99%AE%E6%8B%89%E6%96%AF%E7%AE%97%E5%AD%90-laplacian-operator-ea877f1945a0
    T = 150  # 閥值(沒有使用)
    KERNAL_LAP = np.array([[0, -1, 0],
                           [-1, 4, -1],
                           [0, -1, 0]])
    l, w = img.shape  # Size
    img = np.insert(img, 0, img[0:l, 0], axis=1)  # 周圍補值
    img = np.insert(img, w+1, img[0:l, w], axis=1)
    img = np.insert(img, 0, img[0, 0:w+2], axis=0)
    img = np.insert(img, l+1, img[l, 0:w+2], axis=0)

    d2value = np.zeros((l+2, w+2))  # 偏微分(差分)兩次的值
    new_img = np.zeros((l, w), np.uint8)  # 創建

    for i in range(1, l+1):  # i, j從1, 1開始
        for j in range(1, w+1):
            d2value[i, j] = np.sum(KERNAL_LAP*img[i-1:i+2, j-1:j+2])  # 偏微分(差分)值
            
    for i in range(l):
        for j in range(w):
            dx = abs(d2value[i, j] - d2value[i+2, j])  # 計算差值
            dy = abs(d2value[i, j] - d2value[i, j+2])
            if dx > dy:
                new_img[i, j] = dx
            else:
                new_img[i, j] = dy
            # 如果有閥值的話
            # if ((d2value[i, j]>0 and d2value[i+2, j]<0) or (d2value[i, j]<0 and d2value[i+2, j]>0)) and dx > T:
            #     new_img[i, j] = 255
            # elif ((d2value[i, j]>0 and d2value[i, j+2]<0) or (d2value[i, j]<0 and d2value[i, j+2]>0)) and dy > T:
            #     new_img[i, j] = 255
            # else:
            #     new_img[i, j] = 0
    return new_img


def canny_edge(img, lower, upper):
    # Step1. 利用 Gaussian Blur 去除雜訊
    gauss_kernal = get_gauss_kernal(1, 5)
    img = blurring(gauss_kernal, img)

    # Step2. 計算梯度
    KERNAL_H = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    KERNAL_V = np.array([[-1,-2,-1],
                         [ 0, 0, 0],
                         [ 1, 2, 1]])
    l, w = img.shape  # Size
    img = np.insert(img, 0, img[0:l, 0], axis=1)  # 周圍補值
    img = np.insert(img, w+1, img[0:l, w], axis=1)
    img = np.insert(img, 0, img[0, 0:w+2], axis=0)
    img = np.insert(img, l+1, img[l, 0:w+2], axis=0)

    Gt = np.zeros((l+2, w+2), np.float32)  # 創建(周圍補零)
    Ang = np.zeros((l+2, w+2), np.float32)
    new_img = np.zeros((l+2, w+2), np.float32)

    for y in range(1, l+1):  # 後來發現第一個值是y, 第二個值是x
        for x in range(1, w+1):
            Gx = np.sum(KERNAL_H*img[y-1:y+2, x-1:x+2])
            Gy = np.sum(KERNAL_V*img[y-1:y+2, x-1:x+2])
            Gt[y, x] = (Gx**2 + Gy**2)**0.5
            Ang[y, x] = Gy/Gx
    Ang[1:l+1, 1:w+1] = np.arctan(Ang[1:l+1, 1:w+1]) *180 /np.pi

    # Step3. Non-maximum suppression
    for y in range(1, l+1):
        for x in range(1, w+1):
            if (Ang[y, x]>=67.5 and Ang[y, x]<=112.5) or (Ang[y, x]<=-67.5 and Ang[y, x]>=-112.5):  # 90
                Max = max(Gt[y-1, x], Gt[y, x], Gt[y+1, x])
                if Gt[y, x] == Max:
                    new_img[y, x] = Gt[y, x]
                else:
                    new_img[y, x] = 0
            elif (Ang[y, x]>=22.5 and Ang[y, x]<=67.5) or (Ang[y, x]<=-112.5 and Ang[y, x]>=-157.5):  # 45
                Max = max(Gt[y-1, x-1], Gt[y, x], Gt[y+1, x+1])
                if Gt[y, x] == Max:
                    new_img[y, x] = Gt[y, x]
                else:
                    new_img[y, x] = 0
            elif (Ang[y, x]<=22.5 and Ang[y, x]>=-22.5) or (Ang[y, x]>=157.5 and Ang[y, x]<=-157.5):  # 0
                Max = max(Gt[y, x-1], Gt[y, x], Gt[y, x+1])
                if Gt[y, x] == Max:
                    new_img[y, x] = Gt[y, x]
                else:
                    new_img[y, x] = 0
            else:  # 135
                Max = max(Gt[y-1, x+1], Gt[y, x], Gt[y+1, x-1])
                if Gt[y, x] == Max:
                    new_img[y, x] = Gt[y, x]
                else:
                    new_img[y, x] = 0
    
    # Step4. Double Thresholding  &  Step5. Hysteresis
    new_img = new_img *255.0 / np.max(new_img)
    tH = upper
    tL = lower
    for y in range(1, l+1):
        for x in range(1, w+1):
            if new_img[y, x] > tH:
                new_img[y, x] = 255
            elif new_img[y, x] < tL:
                new_img[y, x] = 0
            else:
                if (new_img[y-1, x] > tH or new_img[y+1, x] > tH) or (new_img[y+1, x+1] > tH or new_img[y-1, x-1] > tH) \
                   or (new_img[y, x+1] > tH or new_img[y, x-1] > tH) or (new_img[y-1, x+1] > tH or new_img[y+1, x-1] > tH):
                    new_img[y, x] = 255
                else:
                    new_img[y, x] = 0

    return np.uint8(new_img[1:l+1, 1:w+1])


def max_pooling_2x2(img):
    l, w = img.shape  # Size
    newL = (l-1) / 2
    newW = (w-1) / 2
    new_img = np.zeros((newL, newW), np.uint8)  # 創建
    for i in range(newL):
        for j in range(newW):
            kernal = []
            


if __name__ == "__main__":
    PATH = "week_2\TEST_pic.jpg"
    #PATH = "week_2\img.png"

    img = cv2.imread(PATH)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("origin", img)
    # cv2.imshow("gray", gray_img)
    
    # Request 1：Blurring with average filter
    KERNAL_AVE = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]])
    # q1 = blurring(KERNAL_AVE, img)
    # cv2.imshow("average", q1)

    # Request 2：Blurring with gaussian filter.
    DEV = 0.8  # 標準差
    # gauss_kernal = get_gauss_kernal(DEV, 5)
    # q2 = blurring(gauss_kernal, img)
    # cv2.imshow("gaussian", q2)

    # Request 3：Blurring  with median filter.
    # q3 = median_blurring(img)
    # cv2.imshow("median", q3)
    
    # Request 4：Find the edge with Sobel or Laplacian operator.
    # q4_1 = sobel_edge(gray_img)
    # q4_2 = laplacian_edge(gray_img)
    # cv2.imshow("Sobel", q4_1)
    # cv2.imshow("Laplace", q4_2)

    # Request 5：Find the edge with Canny.
    # q5 = canny_edge(gray_img, 25, 55)  # Common
    # l, w = img.shape  # Size
    # if l > 1000 or w > 1000:
    #     gray_img = 
    q5 = canny_edge(gray_img, 15, 45)
    # cv2.imshow("Canny", q5)
    cv2.imwrite('output.png', q5, [cv2.IMWRITE_PNG_COMPRESSION, 5])
    
    cv2.waitKey(0)
