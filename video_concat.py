import numpy as np
import cv2
import os


def concat_video(file1, file2, horizontal=True):
    cap1 = cv2.VideoCapture(file1)
    cap2 = cv2.VideoCapture(file2)
    if not cap1.isOpened() or not cap2.isOpened():
        print('error opening video')
    w = int(cap1.get(3))
    h = int(cap1.get(4))
    if horizontal:
        w <<= 1
        axis = 1
    else:
        h <<= 1
        axis = 0
    out = cv2.VideoWriter("concat.mp4", cv2.VideoWriter_fourcc('F','M','P', '4'), 25, (w, h))

    while(True):
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        if frame1 is None or frame2 is None:
            break
        frame_con = np.concatenate((frame1, frame2), axis=axis)
        cv2.imshow('frame_con', frame_con)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        out.write(frame_con)

    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    concat_video("test1.avi", "test2.avi", True)