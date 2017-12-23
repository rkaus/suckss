from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
#import rospy
#from std_msgs.msg import String
import time
import RPi.GPIO as GPIO

class Boat():
    def __init__(self):#, Lmotor, Rmotor):
        mot = Adafruit_MotorHAT(addr=0x60)
        self.Mmotor = mot.getMotor(3)
        self.Lmotor = mot.getMotor(1)
        self.Rmotor = mot.getMotor(4)
        self.status = None
    def cleanup(self):
        GPIO.cleanup()
    def forward(self, speed=150):
        self.stop()
        time.sleep(0.01)
        self.Lmotor.run(Adafruit_MotorHAT.FORWARD)
        self.Rmotor.run(Adafruit_MotorHAT.FORWARD)
        self.Mmotor.run(Adafruit_MotorHAT.FORWARD)
        for i in range(0,speed,1):
            self.Lmotor.setSpeed(i)
            self.Mmotor.setSpeed(i)
        for i in range(0, speed, 1):
            self.Rmotor.setSpeed(i+5)
        self.LmotorSpeed = speed
        self.RmotorSpeed = speed
        self.MmotorSpeed = speed
        self.status = 'forward'


    def backwards(self, speed=150):
        self.stop()
        time.sleep(0.01)
        self.Lmotor.run(Adafruit_MotorHAT.BACKWARD)
        self.Rmotor.run(Adafruit_MotorHAT.BACKWARD)
        self.Mmotor.run(Adafruit_MotorHAT.BACKWARD)
        for i in range(0,speed,1):
            self.Lmotor.setSpeed(i)
            self.Mmotor.setSpeed(i)
        for i in range(0, speed, 1):
            self.Rmotor.setSpeed(i+5)
        self.LmotorSpeed = speed
        self.RmotorSpeed = speed
        self.MmotorSpeed = speed
        self.status = 'backwards'

    def right(self, speed=100, times=0.1):
        self.stop()
        time.sleep(0.01)
        self.Lmotor.run(Adafruit_MotorHAT.FORWARD)
        self.Rmotor.run(Adafruit_MotorHAT.BACKWARD)
        for i in range(0,speed,1):
            self.Lmotor.setSpeed(i)
        for i in range(0,speed,1):
            self.Rmotor.setSpeed(i)
        time.sleep(times)
        self.status = 'right'
        #self.stop()

    def left(self, speed=100, times=0.1):
        self.stop()
        time.sleep(0.01)
        self.Rmotor.run(Adafruit_MotorHAT.FORWARD)
        self.Lmotor.run(Adafruit_MotorHAT.BACKWARD)
        for i in range(0,speed,1):
            self.Lmotor.setSpeed(i)
        for i in range(0,speed,1):
            self.Rmotor.setSpeed(i)
        time.sleep(times)
        self.status = 'left'
        #self.stop()

    
    def stop(self):
        self.Lmotor.run(Adafruit_MotorHAT.RELEASE)  
        self.Rmotor.run(Adafruit_MotorHAT.RELEASE) 
        self.Mmotor.run(Adafruit_MotorHAT.RELEASE) 
        self.status = 'stopped'


    def circle(self, side):
        for i in range(0,4):
            self.forward(100)
            time.sleep(10)
            if side == 'l':
                self.left(75, 5)
            if side == 'r':
                self.right(75, 5)
        self.backwards(50)
        time.sleep(10)
        self.stop()
    
def control(Boat):
    speed = 40
    input = raw_input('Control:')
    while(input != 'q'):
        if(input.isdigit()):
            if int(input) >= 0 and int(input) <= 5:
                speed = int(input)*40
                input = raw_input('Control:')
        if input == 'w':
            Boat.forward(speed)
            input = raw_input('Control[WASD]:')
        elif input == 's':
            Boat.backwards(speed)
            input = raw_input('Control[WASD]:')
        elif input == 'a':
            Boat.left(speed, 1)
            input = raw_input('Control[WASD]:')
        elif input == 'd':
            Boat.right(speed, 1)
            input = raw_input('Control[WASD]:')
        elif input == 'c':
            side = raw_input('[L]eft or [R]ight:')
            Boat.circle(side)
            input = raw_input('Control[WASD]:')
        else:
            Boat.stop()
            input = raw_input('Control[WASD]:')
        
        
    Boat.stop()

def talker():
     pub = rospy.Publisher('chatter', String, queue_size=10)
     rospy.init_node('talker', anonymous=True)
     rate = rospy.Rate(10) # 10hz
     while not rospy.is_shutdown():
         hello_str = "hello world %s" % rospy.get_time()
         rospy.loginfo(hello_str)
         pub.publish(hello_str)
         rate.sleep()
if __name__ == "__main__":
	SucksS = Boat()
	control(SucksS)
#main()
#talker()
