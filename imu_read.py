import serial
import time
class IMURead:

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.roll_str = str(self.roll)
        self.pitch_str = str(self.pitch)
        self.yaw_str = str(self.yaw)
        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0
        self.serial = serial.Serial('COM5', 921600)
        self.E2boxCommand = {'start': '<start>'.encode(),
                             'stop': '<stop>'.encode()}

    def E2boxStart(self):
        self.serial.reset_input_buffer()
        self.serial.write(self.E2boxCommand['start'])

    def IMUSetzero(self):
        time.sleep(1)
        try:
            temp = b''
            buf = b''
            while temp == b'<ok>':
                temp = self.serial.read(1)  # temp = ser3.read(1)
            while temp != b'\r' or len(buf) < 20:
                # while temp !=len(buf)<100 :
                # while temp !=len(buf)<100:
                temp = self.serial.read(1)  # temp = ser3.read(1)
                buf += temp
            sensor_data = buf.decode()
            eular = sensor_data.split(',')  # list
            self.offset_x = float(eular[1])
            self.offset_y = float(eular[2])
            self.offset_z = float(eular[3])

            print('Init pos : ', self.offset_x, '/', self.offset_y, '/', self.offset_z)

        except KeyboardInterrupt:
            self.serial.write(self.E2boxCommand['stop'])  # ser3.write(sensor_stop)
            SystemExit
    def ImuRead(self, buf=b''):
        while True:
            try:
                temp = b''
                buf = b''
                while temp == b'<ok>':
                    temp = self.serial.read(1)  # temp = ser3.read(1)
                while temp != b'\r' or len(buf) < 20:
                    # while temp !=len(buf)<100 :
                    # while temp !=len(buf)<100:
                    temp = self.serial.read(1)  # temp = ser3.read(1)
                    buf += temp
                sensor_data = buf.decode()
                eular = sensor_data.split(',')
                self.roll = float(eular[1]) - self.offset_x
                self.pitch = float(eular[2]) - self.offset_y
                self.yaw = float(eular[3]) - self.offset_z
                self.roll_str = str(self.roll)
                self.pitch_str = str(self.pitch)
                self.yaw_str = str(self.yaw)
                print(round(self.roll, 2), '/', round(self.pitch, 2), '/', round(self.yaw, 2))
            except KeyboardInterrupt:
                self.serial.write(self.E2boxCommand['stop']) # ser3.write(sensor_stop)
                self.serial.close()

    def get_euler(self, buf=b''):
        try:
            temp = b''
            buf = b''
            while temp == b'<ok>':
                temp = self.serial.read(1)  # temp = ser3.read(1)
            while temp != b'\r' or len(buf) < 20:
                # while temp !=len(buf)<100 :
                # while temp !=len(buf)<100:
                temp = self.serial.read(1)  # temp = ser3.read(1)
                buf += temp
            sensor_data = buf.decode()
            eular = sensor_data.split(',')
            self.roll = float(eular[1]) - self.offset_x
            self.pitch = float(eular[2]) - self.offset_y
            self.yaw = float(eular[3]) - self.offset_z
            self.roll_str = str(self.roll)
            self.pitch_str = str(self.pitch)
            self.yaw_str = str(self.yaw)
            # print(round(self.roll, 2), '/', round(self.pitch, 2), '/', round(self.yaw, 2))
        except KeyboardInterrupt:
            self.serial.write(self.E2boxCommand['stop']) # ser3.write(sensor_stop)
            self.serial.close()

if __name__ == '__main__':
    imu = IMURead()
    imu.E2boxStart()
    imu.IMUSetzero()
    imu.ImuRead()
    # E2boxsensor(ser3)