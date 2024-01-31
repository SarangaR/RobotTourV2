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
        
        self.turn_pid = PID(Constants.KP, Constants.KI, Constants.KD, 0, Constants.TOLERANCE)
        
        self.drive_pid = PID(Constants.DKP, Constants.DKI, Constants.DKD, 0, Constants.D_TOLERANCE)

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
        self.turn_pid.reset()
        
        self.turn_pid.setKp(Constants.KP)
        self.turn_pid.setKi(Constants.KI)
        self.turn_pid.setKd(Constants.KD)
        
        self.turn_pid.setTarget(degrees)
        self.turn_pid.setTolerance(2)
        
        self.drive.stop()
        self.drive.settings(Constants.STRAIGHT_SPEED, Constants.STRAIGHT_ACCEL, Constants.TURN_SPEED, Constants.TURN_ACCEL)
        
        done = False
        while not done:
            calc = self.turn_pid.calculate(self.gyro.angle())
            self.drive.drive(0, calc)
            done = self.turn_pid.isDone()
            
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
        self.turn_pid.reset()
        
        self.turn_pid.setKp(3)
        self.turn_pid.setKi(0.00001)
        self.turn_pid.setKd(0)
        
        self.drive_pid.reset()
        
        # self.drive_pid.setKp(2)
        # self.drive_pid.setKi(0)
        # self.drive_pid.setKd(0)
        
        self.gyro.reset_angle(0)
        
        self.turn_pid.setTarget(0)
        self.turn_pid.setTolerance(2)
        
        self.drive_pid.setTolerance(5)
        
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
        
        self.drive_pid.setTarget(self.drive.distance() + distance)
        
        done = False
        while not done:
            calc = self.turn_pid.calculate(self.gyro.angle())
            speed_calc = self.drive_pid.calculate(self.drive.distance())
            if self.turn_pid.isDone():
                self.drive.drive(speed_calc, 0)
            else:
            # elif self.drive_pid.isDone():
                self.drive.drive(speed_calc, calc)
            # else:
            #     self.drive.drive(speed_calc, calc)
            # done = self.drive_pid.isDone()
            done = self.turn_pid.isDone() and self.drive_pid.isDone()
        
        self.drive.stop()
        self.turn(0)
        time.sleep(0.1)

    def stop(self):
        self.drive.stop()
                
            
            


    


