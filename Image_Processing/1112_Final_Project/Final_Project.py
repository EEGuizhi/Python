# 4109061012 B.S.Chen
import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Python implementation code of:
Pouli, Tania, and Erik Reinhard. "Progressive color transfer for images of arbitrary dynamic range." Computers & Graphics 35.1 (2011): 67-80.
- By B.S.Chen National Chung Hsing University
"""

# Settings
NUM = "02"
PATH_SRC = f"Image_Processing/1112_Final_Project/source/source_{NUM}.jpg"
PATH_TAR = f"Image_Processing/1112_Final_Project/target/target_{NUM}.jpg"

B_MIN = 10
PERC = [25, 50, 60, 70, 80, 90, 100]
W_A = 1.0  # Mask
CH_RANGE = (  # https://stackoverflow.com/questions/11386556/converting-an-opencv-bgr-8-bit-image-to-cie-lab
    (0, 256),
    (0, 256),
    (0, 256)
)


def compute_Smax(Bins: np.ndarray, Bmin: int) -> np.ndarray:
    """ Compute Smax according to Eq.7 , Note: Smax has 3 variables for each channel """
    Smax = np.floor(np.log2(Bins / Bmin))
    return Smax


def histogram(img: np.ndarray, value_range: tuple, normalize: bool) -> np.ndarray:
    """ Compute histogram of input image """
    hist, _ = np.histogram(
        img, np.arange(value_range[0], value_range[1]),
        (value_range[0], value_range[1]),
        density=normalize
    )
    return hist


def resample_histogram(Hist: np.ndarray, Bins: int, normalize: bool) -> np.ndarray:
    """ Resampling histogram, including down- & up- sampling """
    orig_bins = Hist.shape[0]
    resampHist = np.zeros(Bins, dtype=Hist.dtype)

    if orig_bins < Bins:
        for i in range(Bins):
            index = round(i/Bins * orig_bins)
            resampHist[i] = Hist[index if index < orig_bins else orig_bins - 1]
    elif orig_bins > Bins:
        for i in range(orig_bins):
            index = round(i/orig_bins * Bins)
            resampHist[index if index < Bins else Bins - 1] += Hist[i]
    else:
        resampHist = Hist

    if normalize:
        total_area = np.sum(resampHist)
        resampHist = resampHist / total_area

    return resampHist


def ReshapeHistogram(Is: np.ndarray, It: np.ndarray, perc: int, Wa: float=1.0, show_hist=False) -> np.ndarray:
    """ Reshape the histogram of `Is` to be similar as `It`

    Parameters:
    ---
        `Is`: Source image
        `It`: Target image
    """
    if perc == 0: return Is

    # Convert images to CIELab D65 color space
    source_lab = cv2.cvtColor(Is, cv2.COLOR_BGR2Lab)
    target_lab = cv2.cvtColor(It, cv2.COLOR_BGR2Lab)
    del Is, It

    # Initalize
    Io = np.empty_like(source_lab)
    Bins = np.array([CH_RANGE[ic][1] - CH_RANGE[ic][0] for ic in range(3)])

    # Compute Smax
    Smax = compute_Smax(Bins, B_MIN)

    # For each channel
    for ic in range(3):
        # Compute histograms
        Hs = histogram(source_lab[:, :, ic], CH_RANGE[ic], False)
        Ht = histogram(target_lab[:, :, ic], CH_RANGE[ic], False)

        # Mask
        Mask = np.zeros_like(source_lab[:, :, ic])
        if Wa < 1 and ic != 0:
            threshold = Wa * (CH_RANGE[ic][1] - CH_RANGE[ic][0] + 1)
            Mask[source_lab[:, :, ic] > threshold] = 1

        for k in range(1, round((perc/100) * Smax[ic]) + 1):
            # Compute Bk
            Bk = int(Bins[ic] * pow(2, k - Smax[ic]))
            print(f">> k: {k}, Bk: {Bk},   ", end='')

            # Down-sample and then up-sample
            print("resampling..  ", end='')
            Hs_k, Ht_k = resample_histogram(Hs, Bk, True), resample_histogram(Ht, Bk, True)
            Hs_k, Ht_k = resample_histogram(Hs_k, Bins[ic], True), resample_histogram(Ht_k, Bins[ic], True)

            # Region transfer 1
            print("region transfering.. ")
            Rmin_t = findpeaks(Ht_k)
            Hs_kp = np.empty_like(Hs_k)
            for m in range(Rmin_t.shape[0] - 1):
                Hs_kp[Rmin_t[m]:Rmin_t[m+1]] = RegionTransfer(
                    Hs_k[Rmin_t[m]:Rmin_t[m+1]],
                    Ht_k[Rmin_t[m]:Rmin_t[m+1]],
                    k / Smax[ic]
                )

            # Region transfer 2
            Rmin_s = findpeaks(Hs_kp)
            Ho_k = np.empty_like(Hs_k)
            for m in range(Rmin_s.shape[0] - 1):
                Ho_k[Rmin_s[m]:Rmin_s[m+1]] = RegionTransfer(
                    Hs_kp[Rmin_s[m]:Rmin_s[m+1]],
                    Ht_k[Rmin_s[m]:Rmin_s[m+1]],
                    k / Smax[ic]
                )

            # Output becomes next round's input
            Hs = Ho_k

        print(">> histogram matching.. \n")
        Hs = histogram(source_lab[:, :, ic], CH_RANGE[ic], False)
        Io[:, :, ic] = histogram_matching(
            source_lab[:, :, ic],
            Hs,
            Ho_k,
            CH_RANGE[ic],
            source_lab.shape[0] * source_lab.shape[1],
            Mask
        )

        # Plot histograms
        if show_hist:
            plt.plot(Hs / Hs.sum(), label='source')
            plt.plot(Ht / Ht.sum(), label='target')
            plt.plot(Ho_k, label='output')
            plt.xlim(left=0, right=256), plt.ylim(top=0.1, bottom=0), plt.legend()
            plt.show(), cv2.waitKey(0)

    # Convert Io back to RGB color space
    output_img = cv2.cvtColor(Io, cv2.COLOR_Lab2BGR)
    return output_img


def findpeaks(Hist: np.ndarray) -> np.ndarray:
    """ Search Rmin using Eq.8 & Eq.9 """
    H_grad = grad(Hist)
    H_grad2 = grad(H_grad)

    Rmin = []
    for i in range(H_grad2.shape[0]):
        if H_grad[i]*H_grad[i+1] < 0 and H_grad2[i] > 0:
            Rmin.append(i+1)

    Rmin.insert(0, 0)
    Rmin.append(Hist.shape[0])
    return np.array(Rmin)


def grad(arr: np.ndarray) -> np.ndarray:
    """ Compute gradients (Eq.8) """
    grad = np.empty(arr.shape[0] - 1, dtype=arr.dtype)
    for i in range(arr.shape[0] - 1):
        grad[i] = arr[i] - arr[i+1]
    return grad


def RegionTransfer(Hs: np.ndarray, Ht: np.ndarray, wt: float) -> np.ndarray:
    """ Region transfer function using adjusted Eqs.10~12 """
    ws = 1 - wt
    Hs_avg, Ht_avg = Hs.mean(), Ht.mean()
    Hs_std, Ht_std = Hs.std(), Ht.std()

    Ho = Hs.copy()
    if round(Hs_std, 8) != 0:
        Ho = (Ho - Hs_avg) * (wt * Ht_std + ws * Hs_std) / Hs_std + wt * Ht_avg + ws * Hs_avg
    else:
        Ho = Ho - Hs_avg + wt * Ht_avg + ws * Hs_avg

    return Ho


def histogram_matching(Is: np.ndarray, Hs: np.ndarray, Ho: np.ndarray, value_range: tuple, pixel_count: int, Im: np.ndarray) -> np.ndarray:
    """ Performing histogram matching """
    # Initialize
    Imin, Imax = value_range[0], value_range[1]
    Hs_sum, Ho_sum = Hs.sum(), Ho.sum()
    Hs = Hs * pixel_count / Hs_sum
    Ho = Ho * pixel_count / Ho_sum

    # Cumulative Histogram
    Ho, Hs = Ho.cumsum(), Hs.cumsum()

    # Below line: second & third params are "x-coord" and "y-coord corresponding to x-coord",
    # the first param is sample x-coords, which is used to get the corresponding y-coords.
    new_pix_value = np.interp(Hs, Ho, np.arange(Imin, Imax))

    Io, Im = Is.ravel(), Im.ravel()
    Io[Im == 0] = new_pix_value[Io[Im == 0]]
    Io = np.reshape(Io, Is.shape)

    return Io.astype(dtype=np.uint8)


def Full_ReshapeHistogram(Is: np.ndarray, It: np.ndarray) -> np.ndarray:
    source_lab = cv2.cvtColor(Is, cv2.COLOR_BGR2Lab)
    target_lab = cv2.cvtColor(It, cv2.COLOR_BGR2Lab)
    Io = np.empty_like(source_lab)
    for ic in range(3):
        Hs = histogram(source_lab[:, :, ic], CH_RANGE[ic], False)
        Ht = histogram(target_lab[:, :, ic], CH_RANGE[ic], False)
        Mask = np.zeros_like(source_lab[:, :, ic])
        Io[:, :, ic] = histogram_matching(
            source_lab[:, :, ic],
            Hs,
            Ht,
            ic,
            source_lab.shape[0] * source_lab.shape[1],
            Mask
        )
    output_img = cv2.cvtColor(Io, cv2.COLOR_Lab2BGR)
    return output_img


if __name__ == "__main__":
    # Load source and target images
    source_img = np.asarray(cv2.imread(PATH_SRC, cv2.IMREAD_COLOR), dtype=np.uint8)
    target_img = np.asarray(cv2.imread(PATH_TAR, cv2.IMREAD_COLOR), dtype=np.uint8)

    for perc in PERC:
        print("\n=======================================================")
        print(f">> Start the case of perc = {perc}%")
        output_img = ReshapeHistogram(source_img, target_img, perc, W_A, False)
        cv2.imwrite(f"Image_Processing/1112_Final_Project/output/output_{NUM}_perc_{perc}.jpg", output_img)
        print(">> done")
