import cv2
import time
import os

def createFolder(directory): # 폴더 없으면 생성 (날짜별 폴더 생성 위함)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createFolder('./images')

CAM_ID = 0

cam = cv2.VideoCapture(CAM_ID)
prevTime = 0

if cam.isOpened() == False:
    print('Can\'t open the CAM(%d)' % (CAM_ID))
    exit()

start_time = time.time()

while cam.isOpened():
    ret, frame = cam.read()

    cv2.imshow('CAM_window', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if time.time() - start_time >= 1:
        now = time.localtime()

        img_date = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
        img_time = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)

        img_dir = './images/'+img_date
        createFolder(img_dir)

        img_name = "/" + img_time +".png"
        cv2.imwrite(img_dir + img_name, frame)
        start_time = time.time()