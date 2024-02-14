# Magnetometer calibration

# heading = -1 * np.arctan(my/mx) * (180/pi)

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import matplotlib.dates as mdates
from collections import deque
import serial
import re

PORT = "COM5"

# How many sensor samples we want to store
HISTORY_SIZE = 2500

# Pause re-sampling the sensor and drawing for INTERVAL seconds
INTERVAL = 0.01

# ---serial data
ser = serial.Serial('COM5', 115200)
print ("Successfully opened " + ser.portstr)
ser.flushInput()

def Update_Values():
    VarLength = 0
    while VarLength != 11:
        s = ser.readline()
        v=s.decode()
        if s != "":
            row =  [x for x in v.split(',')]
            r1 = [float(x) for x in row]
            r1[0] = r1[0]*0.15
            r1[1] = r1[1]*0.15
            r1[2] = r1[2]*0.15
            r1 = [round(x,4) for x in r1]
            #print(time.time());
            print(r1);
            VarLength = len(row)    
    return r1
# row[AK_HX, AK_HY, AK_HZ, IMU_accX, IMU_accY, IMU_accZ, IMU_gyrX, IMU_gyrY, IMU_gyrZ, IMU_temp, Samplecounter]

HISTORY_SIZE = 3000
INTERVAL = 0.01
# Deque for axes
mag_x = deque(maxlen=HISTORY_SIZE)
mag_y = deque(maxlen=HISTORY_SIZE)
mag_z = deque(maxlen=HISTORY_SIZE)

fig1, ax1 = plt.subplots()

magx = []
magy = []
magz = []
fig1 = plt.figure(figsize=(6,8))
start_t = time.time()
del_t = 0

while(del_t<30):
    imu_ret = Update_Values()
    x,y,z = imu_ret[0:3]
    magx.append(x)
    magy.append(y)
    magz.append(z)
    
    ax1.scatter(magx,magy,color='r',s=20)
    ax1.scatter(magy,magz,color='g',s=20)
    ax1.scatter(magz,magx,color='b',s=20)
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlabel('(mico-Tesla)')
    ax1.set_ylabel('(micro-Tesla)')
    ax1.set_title('Uncalibrated magnetometer')
    ax1.legend(['X-Y','Y-Z','Z-X'])
    #ax1.show()
    end_t = time.time()
    del_t = end_t - start_t
    
ser.close()
print ("Port Closed Successfully")

# Hard iron calibration    
min_x = min(magx)
max_x = max(magx)
min_y = min(magy)
max_y = max(magy)
min_z = min(magz)
max_z = max(magz)

print("X range: ", min_x, max_x)
print("Y range: ", min_y, max_y)
print("Z range: ", min_z, max_z)

mag_calb = [ (max_x + min_x) / 2, (max_y + min_y) / 2, (max_z + min_z) / 2]
print("Final calibration in uTesla:", mag_calb)
# mag_calb = [-1.875, 2.1, 23.775] # Mag calibration values

cal_mag_x = [x - mag_calb[0] for x in magx]
cal_mag_y = [y - mag_calb[1] for y in magy]
cal_mag_z = [z - mag_calb[2] for z in magz]

fig2, ax2 = plt.subplots()
#ax.set_aspect(1)

# Clear all axis
ax2.cla()

# Display the now calibrated data
ax2.scatter(cal_mag_x, cal_mag_y, color='r',s=20)
ax2.scatter(cal_mag_y, cal_mag_z, color='g',s=20)
ax2.scatter(cal_mag_z, cal_mag_x, color='b',s=20)
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlabel('(mico-Tesla)')
ax2.set_ylabel('(micro-Tesla)')
ax2.set_title('Calibrated magnetometer')
ax2.legend(['X-Y','Y-Z','Z-X'])
fig2.show()

# Soft iron calibration - not required