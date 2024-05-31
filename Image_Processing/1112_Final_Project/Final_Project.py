# EEGuizhi
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

"""
Python implementation code of:
Pouli, Tania, and Erik Reinhard. "Progressive color transfer for images of arbitrary dynamic range." Computers & Graphics 35.1 (2011): 67-80.
"""

# Parameters
B_MIN = 15
PERC = [50, 75, 100]
WIDTH = 1  # V
W_A = 1.0  # Mask
CH_RANGE = ((0, 255), (0, 255), (0, 255))  # https://stackoverflow.com/questions/11386556/converting-an-opencv-bgr-8-bit-image-to-cie-lab


def compute_Smax(Bins:int, Bmin:int):
    """比照 Eq.7 計算 Smax
    
    Args:
    ---
        Bins : amount of bins in hist.
        Bmin : minima amount of bins.
    """
    return math.floor(np.log2(Bins/Bmin))


def compute_Hist(lab_img:np.ndarray, bins:int, channel:int):
    """比照 Eq.1~5 計算 Histogram

    Args:
    ---
        img_lab : 2D array (LAB image in a spec channel)
        bins : B in Eq.2
        channel : L*a*b channel, 0=L, 1=a, 2=b
    
    Returns:
    ---
        Hist : [h1, h2, ..., hn]
    """

    Imin, Imax = CH_RANGE[channel][0], CH_RANGE[channel][1]
    Hist = cv2.calcHist([lab_img], [0], None, [bins], [Imin, Imax+1])[:, 0]

    return Hist


def resample_Hist(Hist:np.ndarray, bins:int):
    orig_bins = Hist.shape[0]
    resampHist = np.zeros([bins], dtype=Hist.dtype)
    if orig_bins < bins:
        for i in range(bins):
            index = round(i/bins * orig_bins)
            resampHist[i] = Hist[index if index < orig_bins else orig_bins - 1]
    elif orig_bins > bins:
        for i in range(orig_bins):
            index = round(i/orig_bins * bins)
            resampHist[index if index < bins else bins - 1] += Hist[i]
    else:
        resampHist = Hist

    # Normalize histogram
    total_area = np.sum(resampHist)
    resampHist /= total_area

    return resampHist


def ReshapeHist(Is:str, It:str, perc:int, width:int=1, Wa:float=1.0):
    """
    Args:
        Is (str): Source Image's file path
        It (str): Target Image's file path
    """

    # Load source and target images
    source_img = cv2.imread(Is)
    target_img = cv2.imread(It)

    # Convert images to CIELab D65 color space
    source_lab = cv2.cvtColor(source_img, cv2.COLOR_BGR2Lab)
    target_lab = cv2.cvtColor(target_img, cv2.COLOR_BGR2Lab)
    del Is, It, target_img

    # Ouput Image initialize
    Io = np.empty_like(source_lab)

    # Compute Smax
    print(">> Shape of source: {}, target: {}".format(source_lab.shape, target_lab.shape))
    input(">> Press 'Enter' to continue ..")

    # For each channel
    for ic in range(3):
        # Compute histograms
        bins = round((CH_RANGE[ic][1] - CH_RANGE[ic][0] + 1) / width)
        Hs = compute_Hist(source_lab[:, :, ic], bins, ic)
        Ht = compute_Hist(target_lab[:, :, ic], bins, ic)

        # Mask
        Mask = np.zeros_like(source_lab[:, :, ic])
        if Wa < 1 and ic != 0:
            threshold = Wa * (CH_RANGE[ic][1] - CH_RANGE[ic][0] + 1)
            Mask[source_lab[:, :, ic] > threshold] = 1

        # Compute Smax
        Smax = compute_Smax(bins, B_MIN)

        for k in range(0, round((perc/100) * Smax)):
            # Compute Bk
            Bk = int(bins * pow(2, k-Smax))
            print("\n\n>> k: {}, Bk: {}".format(k, Bk))

            # Downsample & Upsample
            Hs_k = resample_Hist(Hs, Bk)
            Ht_k = resample_Hist(Ht, Bk)
            Hs_k = resample_Hist(Hs_k, bins)
            Ht_k = resample_Hist(Ht_k, bins)

            # Region transfer 1
            Rmin_t = findpeaks(Ht_k)
            Hs_kp = np.empty_like(Hs_k)
            for m in range(len(Rmin_t)-1):
                Hs_kp[Rmin_t[m]:Rmin_t[m+1]] = RegionTransfer(
                    Hs_k[Rmin_t[m]:Rmin_t[m+1]],
                    Ht_k[Rmin_t[m]:Rmin_t[m+1]],
                    (k+1)/Smax
                )

            # Region transfer 2
            Rmin_s = findpeaks(Hs_kp)
            Ho_k = np.empty_like(Hs_k)
            for m in range(len(Rmin_s)-1):
                Ho_k[Rmin_s[m]:Rmin_s[m+1]] = RegionTransfer(
                    Hs_k[Rmin_s[m]:Rmin_s[m+1]],
                    Ht_k[Rmin_s[m]:Rmin_s[m+1]],
                    (k+1)/Smax
                )

            # Output becomes next round's input
            Hs = Ho_k

        Hs = compute_Hist(source_lab[:, :, ic], bins, ic)
        print("\n>> HistMatch: ic = {}".format(ic))
        Io[:, :, ic] = HistMatch(
            source_lab[:, :, ic],
            Hs,
            Ho_k,
            ic,
            source_lab.shape[0] * source_lab.shape[1],
            Mask
        )

    output_img = cv2.cvtColor(Io, cv2.COLOR_Lab2BGR)
    return output_img


def findpeaks(H:np.ndarray):
    """依照 Eq.8 Eq.9 找尋 Rmin
    Args:
        H : Histogram
    """
    H_grad = grad(H)
    H_grad2 = grad(H_grad)

    Rmin = []
    for i in range(H_grad.shape[0] - 1):
        if H_grad[i]*H_grad[i+1] < 0 and H_grad2[i] > 0: Rmin.append(i)

    Rmin.append(H.shape[0])
    if Rmin[0] != 0: Rmin.insert(0, 0)

    return Rmin


def grad(arr:np.ndarray):
    grad = np.empty([arr.shape[0]-1], dtype=arr.dtype)
    for i in range(arr.shape[0]-1):
        grad[i] = arr[i] - arr[i+1]
    return grad


def RegionTransfer(Hs, Ht, wt):
    Hs_avg = np.mean(Hs)
    Ht_avg = np.mean(Ht)
    Hs_std = np.std(Hs)
    Ht_std = np.std(Ht)
    print(">> avg, std: {}, {}, {}, {}".format(Hs_avg, Ht_avg, Hs_std, Ht_std))

    Ho = np.copy(Hs)
    for i in range(Ho.shape[0]):
        if round(Hs_std, 6) != 0:
            Ho[i] = (Ho[i] - Hs_avg) * (wt*Ht_std + (1-wt)*Hs_std) / Hs_std + wt * Ht_avg + (1-wt) * Hs_avg
        else:
            Ho[i] = Ho[i] - Hs_avg + wt * Ht_avg + (1-wt) * Hs_avg

    return Ho


def HistMatch(Is:np.ndarray, Hs:np.ndarray, Ho:np.ndarray, channel:int, pixel_count:int, Im:np.ndarray):
    # Init
    Imin, Imax = CH_RANGE[channel][0], CH_RANGE[channel][1]
    total_area = np.sum(Hs)
    Hs *= pixel_count
    Hs /= total_area
    total_area = np.sum(Ho)
    Ho *= pixel_count
    Ho /= total_area

    # Cumulative Histogram
    Ho = np.cumsum(Ho)
    Hs = np.cumsum(Hs)
    print(f">> Ho length = {Ho.shape[0]}, Hs length = {Hs.shape[0]}")

    # Below line: second & third params are "x-coord" and "y-coord corresponding to x-coord",
    # the first param is sample x-coords, which we want to get the y-coords corresponding to these x-coords.
    new_pix_value = np.interp(Hs, Ho, np.arange(Imin, Imax+1, WIDTH))
    Io = Is.ravel() - Imin  # flatten image
    Im = Im.ravel()  # flatten mask
    Io[Im == 0] = new_pix_value[Io[Im == 0]]
    Io = np.reshape(Io, Is.shape)
    input("\n>> Press Enter to continue..")

    return np.uint8(Io)


if __name__ == "__main__":
    source_image_path = "Image_Processing/1112_Final_Project/source/source_01.jpg"
    target_image_path = "Image_Processing/1112_Final_Project/target/target_01.jpg"

    for perc in PERC:
        out = ReshapeHist(source_image_path, target_image_path, perc, WIDTH, W_A)
        cv2.imwrite(f"Image_Processing/1112_Final_Project/output/ColorTransfer_perc{perc}.png", out)
