from __future__ import division
import cwiid
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from boat import *
import time

wiimote = cwiid.Wiimote()
while not wiimote: 
    wiimote = cwiid.Wiimote()
print ("Connection established!")
wiimote.rpt_mode = cwiid.RPT_ACC
#wiimote.rpt_mode = cwiid.RPT_IR
wiimote.enable(cwiid.FLAG_MOTIONPLUS)


try:

      sucksS = Boat()
      time.sleep(1)
      baseline_x= ( wiimote.state['acc'][cwiid.X] - 116)
      baseline_y= ( wiimote.state['acc'][cwiid.Y] - 120)
      while (baseline_x<0):
          baseline_x= ( wiimote.state['acc'][cwiid.X] - 116)

      vx = 0
      vy = 0
      ax = 0
      ay = 0
      dt = 0.01
      t = 0
      accelList = []
      velocityList = []
      sucksS.forward(200)
      time.sleep(0.01)
      while (True):
         ax_n= (wiimote.state['acc'][cwiid.X] - 116)
         ay_n= (wiimote.state['acc'][cwiid.Y] - 120)
         diffX = ax_n - baseline_x
         diffY = ay_n - baseline_y
         if (diffX == 0):
             print ("if", t)
             #sucksS.backwards(100)
             sucksS.stop()
 	     time.sleep(.5)
             #sucksS.left(100, 1)
             sucksS.forward(200)
             #time.sleep(1)
             t = 0
         ax_n= (wiimote.state['acc'][cwiid.X] - 116)
         diffX = baseline_x - ax_n
             
         while (diffX <= -1):
             print ("elif", t)
             sucksS.backwards(200)
             time.sleep(2)
             sucksS.left(200, 1)
             sucksS.forward(200)
             #t = 0
	     time.sleep(3)
             ax_n= (wiimote.state['acc'][cwiid.X] - 116)
             diffX = baseline_x - ax_n

         vx += ax_n
         vy += ay_n
         time.sleep(dt)
         t += dt
         plt.scatter(ax_n, ay_n, marker ='.')
         plt.scatter(vx, vy, marker ='o')
         accelList.append((ax_n,ay_n))
         velocityList.append((vx,vy))
         print state
  #f = lambda x : (ax_n/dt)*x
  #vx_n, err = scipy.integrate.quad(f, t, t + dt)
  #f = lambda y : (ay_n/dt)*y
  #vy_n, err = scipy.integrate.quad(f, t, t + dt)
          
          #print ("Acc:", ax_n, ay_n, "Vel:", vx, vy, "Pos:", x, y)

          
      
except KeyboardInterrupt:
    plt.ion()
    sucksS.stop()
    plt.savefig('tmp.png')
    wiimote.close()
    print("Wiimote closed")
    c=0
    with open('/home/pi/suckss/log/counter.txt','a+') as counterFile:
        c = counterFile.readline().strip()
    c= int(c)
    c = c+1 
    with open('/home/pi/suckss/log/accellog' + str(c) + '.txt','w') as accellog:
        for item in accelList:
            accellog.write("X:%f  Y:%f \n" % (item[0],item[1]))
    with open('/home/pi/suckss/log/vellog' + str(c) + '.txt','w') as vellog:
        for item in velocityList:
            vellog.write("X:%f  Y:%f \n" % (item[0],item[1]))
        
    
    with open('/home/pi/suckss/log/counter.txt','w') as counterFile:
        counterFile.write(str(c))     
        
