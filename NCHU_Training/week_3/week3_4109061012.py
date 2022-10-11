# 4109061012 陳柏翔
import cv2
import matplotlib.pyplot as plt


class node():
    def __init__(self, freq, value=None, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.value = value
        self.huffman = ""
    
    def traversal(self, array, dict):
        if self.value:
            dict[self.value] = self.huffman

        if self.left:
            self.left.huffman = self.huffman+"0"
            self.left.traversal(array, dict)
        if self.right:
            self.right.huffman = self.huffman+"1"
            self.right.traversal(array, dict)


def get_distinct_intensity(img):
    """
    從黑白的圖片img中, 讀出不同亮度的出現次數
    """
    l, w = img.shape
    dict = {}
    for i in range(l):
        for j in range(w):
            if img[i, j] in dict:
                dict[img[i, j]] += 1
            else:
                dict[img[i, j]] = 1
    List = sorted(dict.items(), key=lambda x: x[1])
    return List


if __name__ == "__main__":
    PATH = "week_3\lena.bmp"
    img = cv2.imread(PATH, 0)
    pix_freq = get_distinct_intensity(img)  # pix_freq = [(亮度value, 出現次數freq), (亮度value, 出現次數freq), ...]

    Nodes = []  # 創建初始節點 (每一格都是node())
    for i in range(len(pix_freq)):
        Nodes.append(node(pix_freq[i][1], pix_freq[i][0]))

    sum = []  # 創建相加後的節點 (每一格都是node())
    for i in range(len(pix_freq)-1):
        sum.append(node(0, 0))

    # Huffman Tree
    x = 0
    while len(Nodes) > 1:
        sum[x].freq = Nodes[0].freq + Nodes[1].freq
        sum[x].left = Nodes[0]
        sum[x].right = Nodes[1]
        del Nodes[0:2]
        
        Nodes.append(sum[x])
        Nodes = sorted(Nodes, key=lambda x: x.freq)
        x += 1
    
    # Result
    result = {}
    Nodes[0].traversal(pix_freq, result)
    nums = []
    for i in range(len(pix_freq)):
        nums.append(pix_freq[i][0])
    nums = sorted(nums)

    print("\n>> Result:\n")
    for i in nums:
        print('"'+str(i)+'": "'+str(result[i])+'"')

    # Plot
    x = []
    y = []
    for i in range(len(pix_freq)):
        x.append(pix_freq[i][0])
        y.append(pix_freq[i][1])
    plt.subplot(1, 2, 1)
    plt.xlabel("Brightness(0~255)")
    plt.ylabel("Frequency")
    plt.bar(x, y)
    x = []
    y = []
    for i in range(len(nums)):
        x.append(nums[i])
        y.append(len(result[nums[i]]))
    plt.subplot(1, 2, 2)
    plt.xlabel("Brightness(0~255)")
    plt.ylabel("Bits Length")
    plt.bar(x, y)
    plt.show()
