import cv2 as cv
import numpy as np
import time
import datetime
thresh = 10 #픽셀 차
max_diff = 5

a, b, c = None, None, None

cap = cv.VideoCapture(0)

def imag():
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    cv.imwrite( filename+'.png', stacked)
    time.sleep(1)
    

if cap.isOpened():
    ret, a = cap.read()#프레임 읽기
    ret, b = cap.read()#프레임 읽기
    while ret:
        ret, c = cap.read()
        draw = c.copy()
        if not ret:
            break
            #3개의 영상을 그레이스케일로 변경
        a_gray = cv.cvtColor(a, cv.COLOR_BGR2GRAY)
        b_gray = cv.cvtColor(b, cv.COLOR_BGR2GRAY)
        c_gray = cv.cvtColor(c, cv.COLOR_BGR2GRAY)
        #a-b, b-c 절대값 차 구하기
        diff1 = cv.absdiff(a_gray, b_gray)
        diff2 = cv.absdiff(b_gray, c_gray)
        #스레시홀드로 기준치 이내의 차이는 무시
        ret, diff1_t = cv.threshold(diff1, thresh, 255, cv.THRESH_BINARY)
        ret, diff2_t = cv.threshold(diff2, thresh, 255, cv.THRESH_BINARY)
        #두 차이에 대해서 AND연산
        diff = cv.bitwise_and(diff1_t, diff2_t)
        #열림연산으로 노이즈 제거
        k = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
        diff = cv.morphologyEx(diff, cv.MORPH_OPEN, k)
        #사각형 그리기
        diff_cnt = cv.countNonZero(diff)
        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)#0이 아닌곳의 좌표 받기
            cv.rectangle(draw, (min(nzero[1]), min(nzero[0])), (max(
                nzero[1]), max(nzero[0])), (0, 255, 0), 2)

            cv.putText(draw, "Motion detected!", (10, 30),
                       cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
        
        stacked = np.hstack((draw, cv.cvtColor(diff, cv.COLOR_GRAY2BGR)))
        cv.imshow('motion', stacked)
        key1=cv.waitKey(32)
        
        if diff_cnt>0:
            imag()


        # 다음비교를 위해 순서 변환
        a = b
        b = c

        if cv.waitKey(1) & 0xFF == 27:
            break


