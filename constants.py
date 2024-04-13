from pybricks.parameters import Port

WHEEL_DIAMETER = 68.8 #mm
TRACK_WIDTH = 153 #mm

LEFT_MOTOR_PORT = Port.A
RIGHT_MOTOR_PORT = Port.D

GYRO_PORT = Port.S2

TILE_LENGTH = 500 #mm

AXIS_DISTANCE = 57.15 #mm

STRAIGHT_SPEED = 2000 #mm/s
STRAIGHT_ACCEL = 10 #mm/s^2

SLOW_STRAIGHT_SPEED = 100 #mm/s
SLOW_STRAIGHT_ACCEL = 100 #mm/s^2
SLOW_STRAIGHT_SPEED_DISTANCE = 50 #mm

TURN_SPEED = 1000 #mm/s
TURN_ACCEL = 10000 #mm/s^2

SLOW_TURN_SPEED = 250 #mm/s
SLOW_TURN_ACCEL = 125 #mm/s^2

KP = 3
KI = 0
KD = 0.5

DKP = 2.5
DKI = 0
DKD = 0 

TOLERANCE = 0.5 #degrees

D_TOLERANCE = 5 #encoder ticks

ROBOT_LENGTH = 171 #mm
