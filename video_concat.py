import numpy as np
import cv2
import os


def concat_video(file1, file2, horizontal=True):
    cap1 = cv2.VideoCapture(file1)
    cap2 = cv2.VideoCapture(file2)
    if not cap1.isOpened() or not cap2.isOpened():
        print('error opening video')
    # frm_cnt = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if horizontal:
        w <<= 1
        axis = 1
    else:
        h <<= 1
        axis = 0
    # out = cv2.VideoWriter("concat.mp4", cv2.VideoWriter_fourcc(*'MP4V'), 25, (w, h))
    out = cv2.VideoWriter("concat.avi", cv2.VideoWriter_fourcc(*'XVID'), 25, (w, h))

    while(True):
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
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
    concat_video("test1.avi", "test2.avi", horizontal=True)