# import cv2
# import numpy as np
#
# # 이미지 불러오기
# # image = cv2.imread('20231006-173739_372.png')
# # image = cv2.imread('20231006-173801_574.png')
# image = cv2.imread('20231006-173901_1130.png')
#
# # 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # Canny 엣지 검출
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
#
# # 검출된 엣지를 활용하여 곡선 검출
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=60, minLineLength=80, maxLineGap=20)
#
# # 검출된 곡선 그리기
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
#
# # 결과 이미지 출력
# cv2.imshow('Hough Lines', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#####################################################################################
# import cv2
# import numpy as np
#
# # 이미지 불러오기
# image = cv2.imread('20231006-173801_574.png')
# image = cv2.imread('20231006-173901_1130.png')
#
# # 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # # Gaussian 블러 적용 (잡음 제거)
# # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#
# # 코너 검출 (Shi-Tomasi 코너 검출기 사용)
# corners = cv2.goodFeaturesToTrack(gray, maxCorners=10, qualityLevel=0.3, minDistance=10)
#
# # 코너를 정수로 변환
# corners = np.int0(corners)
#
# # 코너를 원으로 그리기
# for corner in corners:
#     x, y = corner.ravel()
#     cv2.circle(image, (x, y), 3, 255, -1)
#
# # 결과 이미지 출력
# cv2.imshow('Corners', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#####################################################################################
# import cv2
#
# src = cv2.imread("20231006-173739_372.png", cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#
# sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 3)
# laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
# canny = cv2.Canny(src, 60, 120)
#
# cv2.imshow("sobel", sobel)
# cv2.imshow("laplacian", laplacian)
# cv2.imshow("canny", canny)
# cv2.waitKey()
# cv2.destroyAllWindows()

#####################################################################################
import cv2
import numpy as np

# 이미지 읽기
image = cv2.imread('20231006-173739_372.png')

# 이미지를 그레이스케일로 변환
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 에지 검출을 위해 가우시안 블러 적용
blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

# 소벨 필터 커널 정의
sobel_kernel_x = np.array([[-1, 0, 1],
                          [-2, 0, 2],
                          [-1, 0, 1]], dtype=np.float32)

sobel_kernel_y = np.array([[-1, -2, -1],
                          [0, 0, 0],
                          [1, 2, 1]], dtype=np.float32)

# 수평 방향과 수직 방향으로 소벨 필터 적용
sobel_x = cv2.filter2D(blurred_image, -1, sobel_kernel_x)
sobel_y = cv2.filter2D(blurred_image, -1, sobel_kernel_y)

# 에지를 강화한 이미지 생성
edge_enhanced_image = cv2.addWeighted(sobel_x, 0.8, sobel_y, 0.5, 0)

# 결과 이미지 출력
cv2.imshow('Edge Enhanced Image', edge_enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
