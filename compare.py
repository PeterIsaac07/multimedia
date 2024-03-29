import cv2
import numpy as np
from math import ceil

def get_hist(img):
    hist_b = cv2.calcHist([img],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([img],[1],None,[256],[0,256])
    hist_r = cv2.calcHist([img],[2],None,[256],[0,256])
    hist = np.stack((np.squeeze(hist_r),np.squeeze(hist_g),np.squeeze(hist_b)),axis = 1)
    return hist

def get_mean(img):
    mean = np.mean(img, axis=(0, 1))
    return mean

def compare_hist(hist1,hist2,threshold = 0.4,factor = 1):
    m = np.minimum(hist1,hist2)*factor/np.sum(hist1)
    s = np.sum(m)
    if s > threshold:#similair
        return True
    else:
        return False

def compare_mean(mean1,mean2,threshold = 1.2,factor = 1):
    mean = (mean1-mean2)*factor/mean1
    mean = np.abs(mean)
    s = np.sum(mean)
    if s < threshold:#similair
        return True
    else:
        return False


def grid_slice_img(img):
    img = cv2.resize(img,(600,600))
    slices = []
    x_grid = ceil(img.shape[0]/6)
    y_grid = ceil(img.shape[1]/6)
    for r in range(0,img.shape[0],x_grid):
        for c in range(0,img.shape[1],y_grid):
            sliced = img[r:r+x_grid, c:c+y_grid,:]
            slices.append(sliced)
    return slices

def get_mean_grid(img):
    slices = grid_slice_img(img)
    means = []
    for s in slices:
        mean = get_mean(s)
        means.append(mean)
    return means
def get_hist_grid(img):
    slices = grid_slice_img(img)
    hists = []
    for s in slices:
        hist = get_hist(s)
        hists.append(hist)
    return hists

def compare_mean_grid(means1,means2):
    matching = 0
    unmatching = 0
    for m1,m2 in zip(means1,means2):
        if (compare_mean(m1,m2,threshold=1.5)):
            matching +=1
        else:
            unmatching +=1
    score = int(matching/(matching+unmatching)*100)
    if score >= 80:
        return True
    else:
        return False

def compare_hist_grid(hists1,hists2):
    matching = 0
    unmatching = 0
    for h1,h2 in zip(hists1,hists2):
        if (compare_hist(h1,h2)):
            matching +=1
        else:
            unmatching +=1
    score = int(matching/(matching+unmatching)*100)
    print(score)
    if score >= 70:
        return True
    else:
        return False



def compare_hist_grid_layout(hists1,hists2):
    matching = 0
    unmatching = 0
    for h1,h2 in zip(hists1,hists2):
        if (compare_hist_layout(h1,h2,threshold = 0.7,factor = 1000)):
            matching +=1
        else:
            unmatching +=1
    score = int(matching/(matching+unmatching)*100)
    if score >= 90:
        return True
    else:
        return False

def compare_hist_layout(hist1,hist2,threshold = 0.7,factor = 1):
    m = np.minimum(hist1,hist2)*factor/np.sum(hist2)
    s = np.sum(m)
    if s > threshold:#similair
        return True
    else:
        return False