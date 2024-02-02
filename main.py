#!/usr/bin/env pybricks-micropython
from robot import Robot
from inspect import getsource
import numbers
import constants as Constants
import pathfinding as Pathfinding

path = Pathfinding.shortestPath()
# 
# path = ['left', 'left', 'left', 'left']

robot = Robot()

# path = Path.PATH

robot.stop()
robot.resetAll()

curr = 0

for step in path:
    split = step.split(" ")
    if split[0] == "tile":
        if curr == len(path) - 1:  
            for i in range(int(split[1]) - 1):
                robot.driveTiles(1)
            robot.driveLess(1)
        else:
            for i in range(int(split[1])):
                robot.driveTiles(1)
        
        # robot.driveTiles(float(split[1]))
    elif split[0] == "turn":
        robot.turn(int(split[1]))
    elif split[0] == "left" and len(split) == 2:
        robot.turn(int)
        robot.driveTiles(int(split[1]))
    elif split[0] == "left":
        robot.turnLeft90()
    elif split[0] == "right" and len(split) == 2:
        robot.turnRight90()
        robot.driveTiles(int(split[1]))
    elif split[0] == "right":
        robot.turnRight90()
    elif split[0] == "left45":
        robot.turnLeft45()
    elif split[0] == "right45":
        robot.turnRight45()
    elif split[0] == "straight":
        try:
            value = int(split[1])
            robot.driveStraight(value)
        except ValueError:
            if split[1] == "len":
                value = Constants.ROBOT_LENGTH
                robot.driveStraight(value)
            elif split[1] == "-len":
                value = -Constants.ROBOT_LENGTH
                robot.driveStraight(value)
    elif split[0] == "waiting":
        robot.waiting()
    elif split[0] == "stop":
        robot.stop()
    elif split[0] == "reset":
        robot.resetAll()
    # print(step)
    curr += 1
    
path.PATH = []
