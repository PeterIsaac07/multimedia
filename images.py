def saving_image(URL,hist,mean):
    saved_hist = cPickle.dumps(hist)
    saved_mean = cPickle.dumps(mean)
    data = (URL,saved_hist,saved_mean)
    SQLstatement = "INSERT INTO Images (URL,saved_hist,saved_mean) VALUES (%s,%s,%s)"
    cur.execute(SQLstatement, data)
    db.commit()

def retrieve_images():
    retrieved_data = []
    SQLstatement = "SELECT * FROM Images"
    cur.execute(SQLstatement)
    ret = cur.fetchall()

    for i in range(len(ret)):
        retrieved_hist = cPickle.loads(ret[i][1])
        retrieved_mean = cPickle.loads(ret[i][2])
        retrieved_data.append([ret[i][0],retrieved_hist,retrieved_mean])

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

img1 = cv2.imread('URL1')
img2 = cv2.imread('URL2')
img3 = cv2.imread('URL3')

saving_image('URL1', get_hist(img1), get_mean(img1))
saving_image('URL2', get_hist(img2), get_mean(img2))
saving_image('URL3', get_hist(img3), get_mean(img3))

retrieve_images()
