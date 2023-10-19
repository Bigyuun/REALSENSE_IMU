import cv2
import numpy as np
import time
# 카메라 매트릭스와 왜곡 계수 (카메라 캘리브레이션 결과에서 얻은 값으로 대체하세요)
# rms = 0.575244
P480 = {'fx': 528.471687,
        'fy': 528.471687,
        'cx': 320.000000,
        'cy': 240.000000,
        'k1': -0.352193,
        'k2': 0.078302,
        'k3': 0,
        'p1': -0.002398,
        'p2': -0.000378
        }

P720 = {'fx': 790.40908924,
        'fy': 793.54098454,
        'cx': 640.000000,
        'cy': 360.000000,
        'k1': -0.35513963,
        'k2': 0.09214795,
        'k3': -0.00436943,
        'p1': -0.00315365,
        'p2': -0.00139974,
        'roi': [640, 480],
        'xyxy': [320, 113, 960, 593],
        'xyxy2': [140, 113, 1140, 593]
        }

# camera_matrix = np.array([[528.471687, 0.,           364.74696965],
#                           [0.,           528.471687, 269.63956264],
#                           [0.,           0.,           1.]])
fx = P720.get('fx')
fy = P720.get('fy')
cx = P720.get('cx')
cy = P720.get('cy')
k1 = P720.get('k1')
k2 = P720.get('k2')
k3 = P720.get('k3')
p1 = P720.get('p1')
p2 = P720.get('p2')
xyxy = P720.get('xyxy')
xyxy2 = P720.get('xyxy2')

camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
distortion_coefficients = np.array([k1, k2, p1, p2, k3])

# distortion_coefficients = np.array([-0.28719757,
#                                     -0.3227997,
#                                     -0.00775333,
#                                     -0.00456767,
#                                     0.77397433])

# 카메라 열기
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 카메라 장치 번호 또는 비디오 파일 경로를 지정하세요
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FOURCC, 0x32595559)
cap.set(cv2.CAP_PROP_FPS, 60)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(width, height, fps)


COUNT_SAVE = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # 왜곡 보정
    h, w = frame.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))

    # 왜곡 보정된 프레임
    undistorted_frame = cv2.undistort(frame, camera_matrix, distortion_coefficients, None, new_camera_matrix)
    roi_undistorted_frame = undistorted_frame[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]]
    roi_undistorted_frame2 = undistorted_frame[xyxy2[1]:xyxy2[3], xyxy2[0]:xyxy2[2]]
    # 프레임 표시
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Undistorted Frame', undistorted_frame)
    cv2.imshow('ROI Undistorted Frame', roi_undistorted_frame)
    cv2.imshow('ROI Undistorted Frame2', roi_undistorted_frame2)

    time_str = time.strftime("%Y%m%d-%H%M%S")
    cv2.imwrite('capture/640x480' + '/' + time_str + '_' + str(COUNT_SAVE) + '.png', roi_undistorted_frame)
    cv2.imwrite('capture/1000x480' + '/' + time_str + '_' + str(COUNT_SAVE) + '.png', roi_undistorted_frame2)
    COUNT_SAVE += 1
    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' 키를 누르면 종료
        break

# 종료
cap.release()
cv2.destroyAllWindows()
