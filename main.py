import MySQLdb
import  cv2
import _pickle as cPickle
import math as m
import binascii
#db = MySQLdb.connect(host="localhost",   # your host, usually localhost
   #                  user="root",        # your username
  #                   passwd="root",      # your password
 #                    db="test")          # name of the data base
#cur = db.cursor()


#cur.execute("SELECT * FROM student")
#img = cv2.imread('new.jpg') #reads image data

# calculate frequency of pixels in range 0-255
#histg = cv2.calcHist([img],[0],None,[256],[0,256])
#pickledList = cPickle.dumps(img)


#print(type(histg))
#data = ("just an image",pickledList)
#SQLstatement = "insert into student (s_name , files ) values (%s, %s)"
#cur.execute(SQLstatement,data)

#SQLstatement = "SELECT * FROM student "
#cur.execute(SQLstatement)
#result = cur.fetchall()
#print(result[0][1])
#histg = pickle.load(result[3][1])
#histg =cPickle.loads(result[4][1])
#print(type(histg))
#print(histg)
#print(len(result[2][1]))
#image = cv2.imread(img)
#cv2.imshow(result[0][1])
#img = cPickle.loads(result[0][1])
#window_name = 'image'
#cv2.imshow(window_name, img )
#cv2.waitKey(0)

#db.commit()
#for row in cur.fetchall():
 #   print(row)
buf = (binascii.crc32(bytearray(0xAB)) )
print(hex(buf))

