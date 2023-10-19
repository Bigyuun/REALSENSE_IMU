import cv2
import os, glob
# 이미지 프레임 리스트 (이미지 파일명 또는 이미지 배열로 대체하세요)
image_frames = ['frame1.jpg', 'frame2.jpg', 'frame3.jpg', 'frame4.jpg']
dir_path = os.path.join('capture', 'video_image_2')
images = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
images.sort()

# 영상 파일 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정
out = cv2.VideoWriter('output2.avi', fourcc, 20.0, (640,480))  # 출력 파일명, 코덱, 프레임 속도, 해상도 설정

# 이미지 프레임을 영상에 추가
for frame in images:
    image = cv2.imread(os.path.join(dir_path, frame))
    out.write(image)

# 영상 저장을 마무리
out.release()
