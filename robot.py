import constants as Constants
import path as Path
from pybricks.parameters import Direction
from pybricks.robotics import *
from pybricks.ev3devices import *
from pybricks.tools import StopWatch, DataLog
from pid import PID
import time

class Robot:
    def __init__(self):
        
        self.left = Motor(Constants.LEFT_MOTOR_PORT)
        self.right = Motor(Constants.RIGHT_MOTOR_PORT)

        print(Constants.WHEEL_DIAMETER)
        print(Constants.TRACK_WIDTH)

        self.drive = DriveBase(self.left, self.right, Constants.WHEEL_DIAMETER, Constants.TRACK_WIDTH)
        self.drive.settings(Constants.STRAIGHT_SPEED, Constants.STRAIGHT_ACCEL, Constants.TURN_SPEED, Constants.TURN_ACCEL)
        
        self.gyro = GyroSensor(Constants.GYRO_PORT, Direction.CLOCKWISE)
        self.gyro.reset_angle(0)

        self.timer = StopWatch()
        self.timer.reset()

        self.first = True
        
        self.pid = PID(Constants.KP, Constants.KI, Constants.KD, 0, Constants.TOLERANCE)
        
        self.e_pid = PID(1, 0, 0, 0, 5)

    def resetAll(self):
        self.drive.reset()
        self.gyro.reset_angle(0)

    def reset(self):
        self.drive.reset()

    def driveTiles(self, tiles):
        if self.first:
            self.gyroDriveStraightPID((tiles * Constants.TILE_LENGTH) - Constants.TILE_LENGTH/2 + Constants.ROBOT_LENGTH/2)
            self.first = False
        else:
            self.gyroDriveStraightPID(tiles * Constants.TILE_LENGTH + Constants.ROBOT_LENGTH/2)
            
    def gyroReset(self):
        self.gyro.reset_angle(0)
        time.sleep(0.1)

    def turn(self, degrees):
        self.pid.reset()
        
        self.pid.setKp(Constants.KP)
        self.pid.setKi(Constants.KI)
        self.pid.setKd(Constants.KD)
        
        self.pid.setTarget(degrees)
        self.pid.setTolerance(2)
        
        self.drive.stop()
        self.drive.settings(Constants.STRAIGHT_SPEED, Constants.STRAIGHT_ACCEL, Constants.TURN_SPEED, Constants.TURN_ACCEL)
        
        done = False
        while not done:
            calc = self.pid.calculate(self.gyro.angle())
            self.drive.drive(0, calc)
            done = self.pid.isDone()
            
        self.drive.stop()
        
        self.gyro.reset_angle(0)
        
        time.sleep(0.1)
        
    def turnLeft90(self):
        self.turn(-90)
        
    def turnRight90(self):
        self.turn(90)
        
    def turnLeft45(self):
        self.turn(-45)
    
    def turnRight45(self):
        self.turn(45)

    def driveStraight(self, distance):
        self.gyroDriveStraightPID(distance)
        
    def gyroDriveStraightPID(self, d):
        self.pid.reset()
        
        self.pid.setKp(2)
        self.pid.setKi(0)
        self.pid.setKd(0)
        
        self.e_pid.reset()
        
        self.e_pid.setKp(2)
        self.e_pid.setKi(0)
        self.e_pid.setKd(0)
        
        self.gyro.reset_angle(0)
        
        self.pid.setTarget(0)
        self.pid.setTolerance(2)
        
        self.e_pid.setTolerance(5)
        
        self.drive.stop()
        self.drive.settings(Constants.STRAIGHT_SPEED, Constants.STRAIGHT_ACCEL, Constants.TURN_SPEED, Constants.TURN_ACCEL)
        
        speed = 0
        
        distance = d
        
        print("Distance" + str(distance))
        
        
        if distance < 0:
            speed = -Constants.STRAIGHT_SPEED
        else:
            speed = Constants.STRAIGHT_SPEED
            
        distance = abs(distance)
        
        self.e_pid.setTarget(self.drive.distance() + distance)
        
        done = False
        while not done:
            calc = self.pid.calculate(self.gyro.angle())
            speed_calc = self.e_pid.calculate(self.drive.distance())
            if self.pid.isDone():
                self.drive.drive(speed_calc, 0)
            elif self.e_pid.isDone():
                self.drive.drive(0, calc)
            else:
                self.drive.drive(speed_calc, calc)
                
            done = self.pid.isDone() and self.e_pid.isDone()
        
        self.drive.stop()
        self.turn(0)
        time.sleep(0.1)

    def stop(self):
        self.drive.stop()
                
            
            


    


