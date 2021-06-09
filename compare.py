import numpy as np
import cv2
def get_hist(img):
    hist_b = cv2.calcHist([img],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([img],[1],None,[256],[0,256])
    hist_r = cv2.calcHist([img],[2],None,[256],[0,256])
    hist = np.stack((np.squeeze(hist_r),np.squeeze(hist_g),np.squeeze(hist_b)),axis = 1)
    return hist

def get_mean(img):
    mean = np.mean(img, axis=(0, 1))
    return mean

def compare_hist(img1,img2,threshold = 0.7):
    hist1 = get_hist(img1)
    hist2 = get_hist(img2)
    m = np.minimum(hist1,hist2)/np.sum(hist2)
    s = np.sum(m)
    if s > threshold:#similair
        return True
    else:
        return False

def compare_mean(img1,img2,threshold = 0.8):
    mean1 = get_mean(img1)
    mean2 = get_mean(img2)
    mean = (mean1+mean2)/(2*mean1)
    s = np.sum(mean)/3
    if s > threshold:#similair
        return True
    else:
        return False

