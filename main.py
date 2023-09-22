import camera_open
import imu_read

import time
import os
import pandas as pd
import cv2
import threading
import keyboard

# RealSense Camera init
camera = camera_open.RealSense()
camera.camera_init()

# IMU sensor (E2box Co.) init
imu = imu_read.IMURead()
imu.E2boxStart()
imu.IMUSetzero()

def camera_read():
    while True:
        try:
            camera.read_once()

        except KeyboardInterrupt:
            print("Keyboard Interrupt: Exiting...")
            thread_camera.join()

def euler_read():
    while True:
        try:
            imu.get_euler()
        except KeyboardInterrupt:
            print("Keyboard Interrupt: Exiting...")
            thread_imu.join()

# Build the threads
thread_imu = threading.Thread(target=euler_read)
thread_imu.start()
thread_camera = threading.Thread(target=camera_read)
thread_camera.start()

# Declare path for save files
def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

IMAGE_DIR = 'datasets/images'
CSV_DIR = 'datasets'
create_directory(IMAGE_DIR)

# Saveing image(.jpg) and IMU(.csv)
KEY_COMMAND = ''
COUNT_SAVE = 0

df_imu = pd.DataFrame({'file name':[], 'roll':[], 'pitch':[], 'yaw':[]})
# df_imu.to_csv(CSV_DIR + '/data.csv', index=False)
while True:

    # if KEY_COMMAND == 'r':
    try:
        cv2.imwrite(IMAGE_DIR + '/' + str(COUNT_SAVE) + '.png', camera.color_image)
        df_imu.loc[COUNT_SAVE] = [str(COUNT_SAVE)+'.png', imu.roll_str, imu.pitch_str, imu.yaw_str]
        COUNT_SAVE += 1
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Save and Exiting...")
        df_imu.to_csv(CSV_DIR + '/data.csv', index=False)






























