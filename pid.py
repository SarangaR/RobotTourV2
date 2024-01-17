class PID:
    def __init__(self, kp, ki, kd, target, tolerance):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target = target
        self.tolerance = tolerance
        self.error = 0
        self.last_error = 0
        self.integral = 0
        self.derivative = 0
        self.output = 0
        
    def calculate(self, current):
        self.error = self.target - current
        self.integral += self.error
        self.derivative = self.error - self.last_error
        self.output = self.kp*self.error + self.ki*self.integral + self.kd*self.derivative
        self.last_error = self.error
        return self.output
    
    def reset(self):
        self.error = 0
        self.last_error = 0
        self.integral = 0
        self.derivative = 0
        self.output = 0
    
    def isDone(self):
        return abs(self.error) < self.tolerance
    
    def getError(self):
        return self.error
    
    def getOutput(self):
        return self.output
    
    def getTarget(self):
        return self.target
    
    def getTolerance(self):
        return self.tolerance
    
    def setTarget(self, target):
        self.target = target
        
    def setTolerance(self, tolerance):
        self.tolerance = tolerance
    
    def setKp(self, kp):
        self.kp = kp
        
    def setKi(self, ki):
        self.ki = ki
        
    def setKd(self, kd):
        self.kd = kd
        
    def getKp(self):
        return self.kp

    def getKi(self):
        return self.ki
    
    def getKd(self):
        return self.kd