import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (12, 6)
# load the image
img = cv2.imread('D:\\Test Data\\01.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(6, 6))
plt.imshow(img, cmap='gray')
plt.axis("off")
plt.title("Original Image")
plt.show()

# edge mask generation
line_size = 7
blur_value = 7

gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray_blur = cv2.medianBlur(gray_img, blur_value)
edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 3)

plt.figure(figsize=(6, 6))
plt.imshow(edges, cmap='gray')
plt.axis("off")
plt.title("Edges Image")
plt.show()

# Color quantization with KMeans clustering
from sklearn.cluster import KMeans

k = 7
data = img.reshape(-1, 3)

kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto').fit(data)
img_reduced = kmeans.cluster_centers_[kmeans.labels_]
img_reduced = img_reduced.reshape(img.shape)
img_reduced = img_reduced.astype(np.uint8)

plt.figure(figsize=(6, 6))
plt.imshow(img_reduced)
plt.axis("off")
plt.title("Reduced Image")
plt.show()

# Bilateral Filter

blurred = cv2.bilateralFilter(img_reduced, d=7, sigmaColor=200, sigmaSpace=200)
# blurred = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
# cartoon = cv2.cvtColor(cartoon, cv2.COLOR_RGB2GRAY)

plt.figure(figsize=(6, 6))
plt.imshow(cartoon, cmap='gray')
plt.axis("off")
plt.title("Cartoon Image")
plt.show()

# export cartoon to a jpg file
# cartoon_ = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
# cv2.imwrite('C:\\Users\\Angel\\Pictures\\IMG_20201225_150545-cartoon.jpg', cartoon_)
