# EEGuizhi
import cv2
import numpy as np

PATH = "D:/GitHub/EEGuizhi/Python/NCHU_Training/week_1/week1_Lenna.jpg"
KERNEL_SIZE = 5
STRIDE = 3


def get_gauss_kernal(dev:float, size:int):
    if size%2 == 0 or size<3:
        print(">> Error")
        raise

    kernal = np.zeros((size, size))
    s = (size-1)/2
    for i in range(size):
        for j in range(size):
            kernal[i, j] = -((i-s)**2+(j-s)**2)/(2*(dev**2))
    kernal = np.exp(kernal)/(2*np.pi*(dev**2))
    return kernal

def de_overlap_kernel(kernel:np.ndarray, stride:int):
    h_kernel, w_kernel = kernel.shape

    magnitude = np.ones_like(kernel)
    conv_map = np.zeros((2*stride + h_kernel, 2*stride + w_kernel))
    for i in range(3):
        for j in range(3):
            conv_map[i*stride : i*stride + h_kernel, j*stride : j*stride + w_kernel] += magnitude[:, :]
    magnitude /= conv_map[stride : stride+h_kernel, stride : stride+w_kernel]

    kernel *= magnitude
    return kernel

def transpose_conv(input:np.ndarray, kernel:np.ndarray, stride:int=1):
    h_in, w_in = input.shape
    h_kernel, w_kernel = kernel.shape

    output_height = (h_in - 1) * stride + h_kernel
    output_width = (w_in - 1) * stride + w_kernel
    output = np.zeros((output_height, output_width))

    for i in range(h_in):
        for j in range(w_in):
            output[i*stride:i*stride + h_kernel, j*stride:j*stride + w_kernel] += input[i, j] * kernel[:, :]

    output /= output.max()
    return output


if __name__ == "__main__":
    img = cv2.imread(PATH)
    print(f">> max: {np.max(img)}, min: {np.min(img)}")

    kernel = get_gauss_kernal(dev=1.0, size=KERNEL_SIZE)
    print(kernel)
    # kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE))
    # kernel = de_overlap_kernel(kernel, stride=STRIDE)

    new_img = np.stack((
        transpose_conv(img[:, :, 0], kernel, stride=STRIDE),
        transpose_conv(img[:, :, 1], kernel, stride=STRIDE),
        transpose_conv(img[:, :, 2], kernel, stride=STRIDE)),
        axis=-1
    )

    new_img2 = np.stack((
        transpose_conv(new_img[:, :, 0], kernel, stride=STRIDE),
        transpose_conv(new_img[:, :, 1], kernel, stride=STRIDE),
        transpose_conv(new_img[:, :, 2], kernel, stride=STRIDE)),
        axis=-1
    )

    print(f">> input size = {img.shape}, output size = {new_img.shape}")
    cv2.imshow("Origin Image", img)
    cv2.imshow("After TransposeConv Image", new_img)
    cv2.imshow("After TransposeConv 2 Image", new_img2)
    save_img = new_img2 * 255
    cv2.imwrite("output.jpg", save_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
