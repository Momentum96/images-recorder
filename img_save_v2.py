import cv2
import time
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createFolder('./images')

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=120,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    prevTime = 0

    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        start_time = time.time()

        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()
            img = cv2.rotate(img, cv2.ROTATE_180) #
            cv2.imshow("CSI Camera", img)
            keyCode = cv2.waitKey(30) & 0xFF # ESC
            if keyCode == 27:
                break
            if time.time() - start_time >= 1:
              now = time.localtime()

              img_date = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
              img_time = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)

              img_dir = './images/'+img_date
              createFolder(img_dir)

              img_name = "/" + img_time +".png"
              cv2.imwrite(img_dir + img_name, img)
              print(img_name + " writted.")
              start_time = time.time()

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
