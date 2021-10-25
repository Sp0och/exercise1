from matplotlib import pyplot as plt
from scipy.ndimage.interpolation import rotate
from scipy.ndimage.filters import gaussian_filter1d, gaussian_filter
import numpy as np
import cv2


# Implement a function that performs non-maximum suppression. You can leave it for the end

def nonmax_suppression(harris_resp, thr, halfwidth=2):
    # Outputs:
    # 1) cornersy: list with row coordinates of identified corner pixels.
    # 2) cornersx: list with respective column coordinates of identified corner pixels.
    # Elements from the two lists with the same index must correspond to the same corner.

    h, w = im.shape
    cornersy = []
    cornersx = []
    for i in range(h):
        for j in range(w):
            max = True
            #even consider this pixel as maximum?
            if(harris_resp[i,j]>thr):
                #neighbour maximum suppression
                if(i > 0 and harris_resp[i-1,j] > harris_resp[i,j]):
                    max = False
                if(i < h-1 and harris_resp[i+1,j] > harris_resp[i,j]):
                    max = False
                if(j > 0 and harris_resp[i,j-1] > harris_resp[i,j]):
                    max = False
                if(j < w-1 and harris_resp[i,j+1] > harris_resp[i,j]):
                    max = False
            else:
                max = False
            if(max):
                cornersy.append(i)
                cornersx.append(j)
    
    

    return cornersy, cornersx


# Implement the main part of the exercise

# Define parameters
sigma_w = 2.0
sigma_d = 2.0
kappa = 0.04
rot_angle = 0
thresh = 800

# Read the image
im = cv2.imread('../images/CircleLineRect.png', 0)
im = im.astype('float')

# Rotation of the image
if rot_angle != 0:
    im = rotate(im, rot_angle)

w,h = im.shape

# TODO: Implement Harris corners
# Useful functions: gaussian_filter1d, gaussian_filter



I_x = gaussian_filter1d(im,sigma_d,-1,1)
I_y = gaussian_filter1d(im,sigma_d,0,1)
I_x2 = np.matmul(I_x,I_x)
I_y2 = np.matmul(I_y,I_y)
I_xy = np.matmul(I_x,I_y)

I_x2_s = gaussian_filter(im,sigma_w)
I_y2_s = gaussian_filter(im,sigma_w)
I_xy_s = gaussian_filter(I_xy,sigma_w)

#define individual A
def build_H_ij(I_x2_s,I_y2_s,I_xy_s,i,j):
    Aij = [[I_x2_s[i,j],I_xy_s[i,j]],[I_xy_s[i,j],I_y2_s[i,j]]]
    return np.linalg.det(Aij) - kappa*np.trace(Aij)**2

H = np.ndarray([h,w])
for i in range(h):
    for j in range (w):
        H[i,j] = build_H_ij(I_x2_s,I_y2_s,I_xy_s,i,j)

corn = nonmax_suppression(H,thresh,2)


# Visualization of the results

# Plotting of results
# No need to change it
plt.close("all")
plt.ion()
f, ax_arr = plt.subplots(1, 3, figsize=(18, 16))
ax_arr[0].set_title("Input Image")
ax_arr[1].set_title("Harris Response")
ax_arr[2].set_title("Detections")
ax_arr[0].imshow(im, cmap='gray')
ax_arr[1].imshow(H, cmap='gray')
ax_arr[2].imshow(im, cmap='gray')
ax_arr[2].scatter(x=corn[1], y=corn[0], c='r', s=10)
plt.show()
plt.pause(15)



