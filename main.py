import MySQLdb
import _pickle as cPickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pylab as pl
from IPython import display
threshold_key_frame = 1

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


def saving_video(URL,key_frame,buf_feature):
    picklekey = cPickle.dumps(key_frame)
    picklebuffer = cPickle.dumps(buf_feature)
    data = (URL, picklebuffer, picklekey)
    SQLstatement = "insert into Video (video_ref , mean , keyframes ) values (%s, %s,%s)"
    cur.execute(SQLstatement,data)
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


def compare(key1):
    result = []
    retrieve_video = retrieve_videos()
    for i in range(len(retrieve_video)):
        flag = is_similar(key1, retrieve_video[i][2], 0.5, 1)
        if  flag == True :
            result.append(retrieve_video[i][0])
    return result







path1 = 'C:/Users/PI/PycharmProjects/new/video2.mp4'
buf1 = capture(path1)
buf_feature1 = get_feature_vector(buf1)
key_f1 = get_key_frames(buf1,buf_feature1,threshold_key_frame)



#result = retrieve_videos()
#saving_video(path1,key_f1,buf_feature1)

urls = compare(key_f1)

print(urls)

