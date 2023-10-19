import glob
import os

import numpy as np
import cv2

# 체스보드 패턴의 가로 및 세로 내부 코너 수
# 체스보드 패턴에 맞게 조정하세요.
width = 7  # 가로 내부 코너 수
height = 4  # 세로 내부 코너 수

# 체스보드 패턴을 찾기 위한 체스보드 이미지 촬영
# 체스보드 패턴 이미지를 사용하여 내부 코너의 3D 좌표와 2D 이미지 좌표를 측정합니다.
# 이 작업을 여러 이미지에 대해 수행하여 캘리브레이션 데이터를 얻어야 합니다.

# 3D 객체 포인트 (실제 체스보드의 내부 코너 좌표)
object_points = []
for i in range(height):
    for j in range(width):
        object_points.append([j, i, 0])

object_points = np.array(object_points, dtype=np.float32)

# 이미지에서 2D 이미지 포인트 찾기
image_points = []
dir_path = os.path.join('calibration_sample', 'endoscope_image', '720p')
images = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
images.sort()

for image_path in images:
    image = cv2.imread(os.path.join(dir_path, image_path))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 체스보드 패턴 검출
    ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

    if ret:
        image_points.append(corners)

# 카메라 캘리브레이션
ret, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(
    [object_points] * len(image_points), image_points, gray.shape[::-1], None, None
)

# 결과 출력
print("카메라 매트릭스:\n", camera_matrix)
print("왜곡 계수:\n", distortion_coefficients)
