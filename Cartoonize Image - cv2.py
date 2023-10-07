# import the packages
import cv2
import matplotlib.pyplot as plt

# Load the image using cv2
img = cv2.imread("C:\\Users\\Angel\\Pictures\\kinzy passport photo.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convert to grayscale and apply median blur to reduce image noise
grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayimg = cv2.medianBlur(grayimg, 7)

# Get the edges
edges = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)

# Convert to a cartoon version
color = cv2.bilateralFilter(img, 9, 250, 250)
cartoon = cv2.bitwise_and(color, color, mask=edges)

# Display original image
# plt.figure(figsize=(2, 2))
# plt.imshow(img)
# plt.axis("off")
# plt.title("Original Image")
# plt.show()

# Display cartoon image
plt.figure(figsize=(6, 6))
plt.imshow(cartoon, cmap='gray')
plt.axis("off")
plt.title("Cartoon Image")
plt.show()


