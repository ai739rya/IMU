# Gyroscope calibration

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

path = "C:\\Users\\ai739\\22\\INTP\\codes\\raw_xyz\\23-3-23\\"
g = 9.81

# --- --- --- ACLN
#rd = pd.read_excel(path + 'all_GYR_9-3-23ii.xlsx')
rd = pd.read_excel(path + 'all_gyr_23-3-23.xlsx')
rd_xi = pd.read_excel(path + 'x_in_23-3-23.xlsx')
rd_xo = pd.read_excel(path + 'x_out_23-3-23.xlsx')
rd_yi = pd.read_excel(path + 'y_in_23-3-23.xlsx')
rd_yo = pd.read_excel(path + 'y_out_23-3-23.xlsx')
rd_zi = pd.read_excel(path + 'z_in_23-3-23.xlsx')
rd_zo = pd.read_excel(path + 'z_out_23-3-23.xlsx')

rd_xi = rd_xi[51:351]
rd_xo = rd_xo[51:351]
rd_yi = rd_yi[51:351]
rd_yo = rd_yo[51:351]
rd_zi = rd_zi[51:351]
rd_zo = rd_zo[51:351]

N = len(rd)
fs=10 # sampling frequency
tT = N/fs
t1 = np.linspace(0,tT,N)

fig1, ax1 = plt.subplots()
fig1 = plt.figure(figsize=(6,8))
ax1.cla()
ax1.plot(t1,rd.IMU_gyrX,'r-')
ax1.plot(t1,rd.IMU_gyrY,'g-')
ax1.plot(t1,rd.IMU_gyrZ,'b-')
ax1.grid()
ax1.set_xlabel('time (s)')
ax1.set_ylabel('$\omega$ ($^\circ$/s)')
ax1.set_title('Raw gyroscope data')
ax1.legend(['$\omega_x$ (raw)','$\omega_y$ (raw)','$\omega_z$ (raw)'])
fig1.show()

g = 9.81
wE = 0.00417808
phi = np.deg2rad(52.19)
k = 2*wE*np.sin(phi)

o3 = [[0.5*(np.mean(rd_xi.IMU_gyrX) + np.mean(rd_xo.IMU_gyrX))],
      [0.5*(np.mean(rd_yi.IMU_gyrY) + np.mean(rd_yo.IMU_gyrY))],
      [0.5*(np.mean(rd_zi.IMU_gyrZ) + np.mean(rd_zo.IMU_gyrZ))]]

s3 = [[(np.mean(rd_xi.IMU_gyrX) - np.mean(rd_xo.IMU_gyrX) -k)/k],
      [(np.mean(rd_yi.IMU_gyrY) - np.mean(rd_yo.IMU_gyrY) -k)/k],
      [(np.mean(rd_zi.IMU_gyrZ) - np.mean(rd_zo.IMU_gyrZ) -k)/k]]

cg = np.ones((N,3))

rdn = rd.to_numpy()
    
bx = -1 if s3[0][0]<0 else 1
by = -1 if s3[1][0]<0 else 1
bz = -1 if s3[2][0]<0 else 1
#calibrated values
for i in range(0,N):
    kl = (bx*s3[0][0]*rdn[i,0]) - o3[0]
    kkx = kl[0]
    kl = (by*s3[1][0]*rdn[i,1]) - o3[1]
    kky = kl
    kl = (bz*s3[2][0]*rdn[i,2]) - o3[2]
    kkz = kl
    cg[i,:] = [kkx,kky,kkz]
  
del kkx,kky,kkz,kl, bx,by,bz

fig2, ax2 = plt.subplots()
fig2 = plt.figure(figsize=(6,8))
ax2.cla()
ax2.plot(t1,cg[:,0],'r-')
ax2.plot(t1,cg[:,1],'g-')
ax2.plot(t1,cg[:,2],'b-')
ax2.grid()
ax2.set_xlabel('time (s)')
ax2.set_title('Calibrated gyroscope data')
ax2.set_ylabel('$\omega$ ($^\circ$/s)')
ax2.set_title('Raw gyroscope data')
ax2.legend(['$\omega_x$ (cal)','$\omega_y$ (cal)','$\omega_z$ (cal)'])
fig2.show()

fig3, ax3 = plt.subplots(3)
#fig3 = plt.figure(figsize=(6,8))
ax3[0].plot(t1,rd.IMU_gyrX,'b-')
ax3[0].plot(t1,cg[:,0],'r-')
ax3[1].plot(t1,rd.IMU_gyrY,'b-')
ax3[1].plot(t1,cg[:,1],'r-')
ax3[2].plot(t1,rd.IMU_gyrZ,'b-')
ax3[2].plot(t1,cg[:,2],'r-')
ax3[0].grid()
ax3[1].grid()
ax3[2].grid()
# ax3.set_xlabel('time (s)')
# ax3.set_ylabel('g (m/s^2)')
# ax3.set_title('accelerometer data')
# ax3.legend(['Raw','Calibrated'])
fig3.show()

fig4, ax4 = plt.subplots()
ax4.scatter(rd.IMU_gyrX, rd.IMU_gyrY,color='b')
ax4.scatter(cg[:,0],cg[:,1],color='r')
ax4.grid()
ax4.legend(['Raw','Calibrated'])
ax4.set_xlabel('$\omega_x$ ($^\circ$/s)')
ax4.set_ylabel('$\omega_y$ ($^\circ$/s)')
fig4.show()

fig5, ax5 = plt.subplots()
ax5.scatter(rd.IMU_gyrY, rd.IMU_gyrZ,color='b')
ax5.scatter(cg[:,1],cg[:,2],color='r')
ax5.grid()
ax5.legend(['Raw','Calibrated'])
ax5.set_xlabel('$\omega_y$ ($^\circ$/s)')
ax5.set_ylabel('$\omega_z$ ($^\circ$/s)')
fig5.show()

fig6, ax6 = plt.subplots()
ax6.scatter(rd.IMU_gyrZ, rd.IMU_gyrX,color='b')
ax6.scatter(cg[:,2],cg[:,0],color='r')
ax6.grid()
ax6.legend(['Raw','Calibrated'])
ax6.set_xlabel('$\omega_z$ ($^\circ$/s)')
ax6.set_ylabel('$\omega_x$ ($^\circ$/s)')
fig6.show()