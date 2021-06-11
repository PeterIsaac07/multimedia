import MySQLdb
import _pickle as cPickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pylab as pl
from IPython import display
import math


#threshold_key_frame = 1

db = MySQLdb.connect(host="localhost",   # your host, usually localhost
                     user="root",        # your username
                     passwd="root",      # your password
                     db="test")          # name of the data base
cur = db.cursor()


def capture(path):
    cap = cv2.VideoCapture(path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    fc = 0
    ret = True
    while (fc < frameCount  and ret):
        ret, buf[fc] = cap.read()
        fc += 1
    cap.release()
    return buf

def get_feature_vector(buf):
    feature_buf = []
    for i  in range(len(buf)):
      feature_buf.append(buf[i].mean(axis=0).mean(axis=0))
    return feature_buf

def get_key_frames(buf,feature_buf,threshold):
    key_frame = []
    key_frame.append(buf[0])
    i = 0
    while i < (len(buf)):
        for j in range(i+1,len(buf)):
            mse = np.mean((feature_buf[i] - feature_buf[j])**2)
            if mse > threshold:
                key_frame.append(buf[j])
                i = j
                break
        i = i+1
    return key_frame

def visualizer(video_array):
    plt.ion()
    for i in range(len(video_array)):
        plt.imshow(cv2.cvtColor(video_array[i], cv2.COLOR_BGR2RGB))
        #plt.show()
        display.clear_output(wait=True)
        display.display(pl.gcf())
    return

def is_similar(key_f_input, key_f_existing,threshold_match, threshold_compare):  # threshold_match :: ratio threthold
    # threshold_compare :: feature compare threshold
    feature_buf_input = get_feature_vector(key_f_input)
    feature_buf_existing = get_feature_vector(key_f_existing)
    match_flag = False
    counter = 0
    for i in range(len(key_f_input)):  # elli bn3ml 3leh retrieval
        for j in range(len(key_f_existing)):  # wa7ed mn el database
            mse = np.mean((feature_buf_existing[i] - feature_buf_input[j]) ** 2)
            if mse < threshold_compare:
                counter = counter + 1
                break
    ratio_input = counter / len(key_f_input)  # ratio of input video key frames to counter
    ratio_existing = counter / len(key_f_existing)  # ratio of existing video key frames to counter
    ratio_maximum = max(ratio_input, ratio_existing)  # the highest ratio
    if ratio_maximum >= threshold_match:
        match_flag = True
    return match_flag

#call this function to save video

def saving_video(URL,threshold_key_frame=1):
    buf1 = capture(URL)
    buf_feature1 = get_feature_vector(buf1)
    key_frame = get_key_frames(buf1,buf_feature1,threshold_key_frame)

    picklekey = cPickle.dumps(key_frame)
    picklebuffer = cPickle.dumps(buf_feature1)
    data = (URL, picklebuffer, picklekey)
    SQLstatement = "insert into Video (video_ref , mean , keyframes ) values (%s, %s,%s)"
    cur.execute(SQLstatement,data)
    db.commit()


#call this function to save image
def saving_image(URL):
    img = cv2.imread(URL)
    hist = get_hist(img)
    mean = get_mean(img)
    grid_hist = get_hist_grid(img)
    saved_hist = cPickle.dumps(hist)
    saved_mean = cPickle.dumps(mean)
    saved_grid_hist = cPickle.dumps(grid_hist)
    data = (URL,saved_hist,saved_mean,saved_grid_hist)
    SQLstatement = "INSERT INTO image (img_ref,hist,mean,grid_hist) VALUES (%s,%s,%s,%s)"
    cur.execute(SQLstatement, data)
    db.commit()
def retrieve_videos ():
    result = []
    cur.execute("SELECT * FROM video")
    retrieved = cur.fetchall()

    for i in range(len(retrieved)):
        temp1 = cPickle.loads(retrieved[i][1])
        temp2 = cPickle.loads(retrieved[i][2])
        result.append([retrieved[i][0],temp1,temp2])
    return result
def retrieve_images():
    retrieved_data = []
    SQLstatement = "SELECT * FROM image"
    cur.execute(SQLstatement)
    ret = cur.fetchall()

    for i in range(len(ret)):
        retrieved_hist = cPickle.loads(ret[i][1])
        retrieved_mean = cPickle.loads(ret[i][2])
        retrieved_grid_hist = cPickle.loads(ret[i][3])
        retrieved_data.append([ret[i][0],retrieved_hist,retrieved_mean,retrieved_grid_hist])

    return retrieved_data
def get_hist(img):
    hist_b = cv2.calcHist([img],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([img],[1],None,[256],[0,256])
    hist_r = cv2.calcHist([img],[2],None,[256],[0,256])
    hist = np.stack((np.squeeze(hist_r),np.squeeze(hist_g),np.squeeze(hist_b)),axis = 1)
    return hist

def get_mean(img):
    mean = np.mean(img, axis=(0, 1))
    return mean


#used to compare videos , pass the url of the video
def compare_video(URL,threshold_key_frame = 1):
    result = []
    retrieve_video = retrieve_videos()
    buf1 = capture(URL)
    buf_feature1 = get_feature_vector(buf1)
    key1 = get_key_frames(buf1, buf_feature1, threshold_key_frame)
    for i in range(len(retrieve_video)):
        flag = is_similar(key1, retrieve_video[i][2], 0.5, 1)
        if  flag == True :
            result.append(retrieve_video[i][0])
    return result


def compare_hist(hist1,hist2,threshold = 0.7):
     m = np.minimum(hist1,hist2)/np.sum(hist2)
     s = np.sum(m)
     if s > threshold:#similair
         return True
     else:
         return False



#used to compare videos , pass the url of the image
def compare_mean(mean1,mean2,threshold = 0.8):
    mean = (mean1+mean2)/(2*mean1)
    s = np.sum(mean)/3
    if s > threshold:#similair
        return True
    else:
        return False


#used to compare videos , pass the url of the image
def compare_img_hist(img):
    img = cv2.imread(img)

    hist = get_hist(img)
    retrieve_image = retrieve_images()
    result = []
    for i in range(len(retrieve_image)):
        flag = compare_hist(hist,retrieve_image[i][1])
        if  flag == True :
            result.append(retrieve_image[i][0])
    return result


def compare_img_mean(img):
    img = cv2.imread(img)
    mean = get_mean(img)
    retrieve_image = retrieve_images()
    result = []
    for i in range(len(retrieve_image)):
        flag = compare_mean(mean,retrieve_image[i][2])
        if  flag == True :
            result.append(retrieve_image[i][0])
    return result


def grid_slice_img(img):
    slices = []
    x_grid =math.ceil(img.shape[0]/6)
    y_grid = math.ceil(img.shape[1]/6)
    for r in range(0,img.shape[0],x_grid):
        for c in range(0,img.shape[1],y_grid):
            sliced = img[r:r+x_grid, c:c+y_grid,:]
            slices.append(sliced)
    return slices



def get_hist_grid(img):
    slices = grid_slice_img(img)
    hists = []
    for s in slices:
        hist = get_hist(s)
        hists.append(hist)
    return hists





def compare_hist_grid(hists1,hists2):
    matching = 0
    unmatching = 0
    for h1,h2 in zip(hists1,hists2):
        if (compare_hist(h1,h2)):
            matching +=1
        else:
            unmatching +=1
    score = int(matching/(matching+unmatching)*100)
    if score >= 90:
        return True
    else:
        return False

def compare_grid_hist(img):
    test = get_hist_grid(img)
    retrieve_image = retrieve_images()
    result = []
    for i in range(len(retrieve_image)):
        flag = compare_hist_grid(test, retrieve_image[i][3])
        if flag == True:
            result.append(retrieve_image[i][0])
    return result





