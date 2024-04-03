import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint

import cv2
import PIL.Image
from PIL import Image

rdate="11-03-2023"
name="Rajan"
regno="342333"
gender="Male"
dob="1999-04-16"
year="2020-2023"
dept="MCA"
    

fn="C2.jpg"
image = cv2.imread('static/img/cert2.jpg',cv2.IMREAD_UNCHANGED)


position = (330,720)
cv2.putText(image, name, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (620,720)
cv2.putText(image, regno, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (530,790)
cv2.putText(image, dept, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)




'''position = (330,610)
cv2.putText(image, name, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (620,610)
cv2.putText(image, regno, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (720,560)
cv2.putText(image, rdate, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)


position = (450,650)
cv2.putText(image, dept, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)

position = (160,690)
cv2.putText(image, year, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)


position = (120,730)
cv2.putText(image, dob, position, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1) 
cv2.imwrite("static/upload/"+fn, image)'''



