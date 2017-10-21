from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

class Boat():
    def __init__(self, Lmotor, Rmotor):
        mot = Adafruit_MotorHAT(addr=0x60)
        self.Lmotor = mot.getMotor(1)
        self.Rmotor = mot.getMotor(4)
        self.LmotorSpeed = 0
        self.RmotorSpeed = 0
        self.LmotorDirection = 0
        self.RmotorDirection = 0

    def forward(self, speed):
        self.LmotorDirection = speed
        for i in range (self.LmotorSpeed < 0):
            self.Lmotor.setSpeed
        self.Lmotor.run(Adafruit_MotorHAT.FORWARD)
        self.Rmotor.run(Adafruit_MotorHAT.FORWARD)

        for i in range(self.LmotorSpeed,speed,1):
            self.Lmotor.setSpeed(i)
        for i in range(self.RmotorSpeed, speed, 1):
            self.Rmotor.setSpeed(i)
        self.LmotorSpeed = speed
        self.RmotorSpeed = speed


    #def backwards(self, speed)

def main():
    SucksS = Boat()
    SucksS.forward(100)            
