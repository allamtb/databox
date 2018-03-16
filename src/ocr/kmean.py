import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np

##############################################################################
# Binarize image data
im = cv2.imread('test.jpg')
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imshow("",im)
# im =im[18:,40:]
rows, cols = im.shape
X=[(row, col) for row in range(rows) for col in range (cols) if im[row][col] < 200]
X = np.array(X)
n_clusters = 4

##############################################################################
# Compute clustering with KMeans

k_means = KMeans(init='k-means++', n_clusters=n_clusters)
k_means.fit(X)
k_means_labels = k_means.labels_
k_means_cluster_centers = k_means.cluster_centers_
k_means_labels_unique = np.unique(k_means_labels)

##############################################################################
# Plot result

colors = ['#4EACC5', '#FF9C34', '#4E9A06', '#FF3300']
for k, color in zip(range(n_clusters), colors):
    # 当前label的真值表
    my_members = k_means_labels == k
    cluster_center = k_means_cluster_centers[k]
    # 列值，展示在X轴
    col_scatter = X[my_members, 1]
    # 行值，展示在Y轴
    row_scatter = X[my_members, 0]
    # 因为图片的原点（0,0）在左上角，与普通坐标系的原点左下角，以X轴对称。
    # 故在展示的时候，用 rows(行高)来减去当前值来取反。
    coordinateY = rows - np.array(row_scatter)
    plt.plot(col_scatter, coordinateY, 'w',
             markerfacecolor=color, marker='X',markersize=6)
    plt.plot(cluster_center[1], cluster_center[0], 'o', markerfacecolor=color,
             markeredgecolor='k', markersize=10)
plt.title('KMeans')
plt.show()
