import math

class State:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

class Constraints:
    def __init__(self, max_velocity, max_acceleration):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration

class TrapezoidProfile:
    def __init__(self, constraints, initial, goal):
        self.m_constraints = constraints
        self.m_initial = initial
        self.m_goal = goal
        self.m_direction = 1 if initial.position < goal.position else -1
        self.m_endAccel = self.time_to_max_velocity()
        self.m_endFullSpeed = self.distance_to_max_velocity() / self.m_constraints.max_velocity
        self.m_endDeccel = self.m_endFullSpeed + self.m_endAccel

    def time_to_max_velocity(self):
        # Calculate time to reach max velocity
        return (self.m_constraints.max_velocity - self.m_initial.velocity) / self.m_constraints.maxAcceleration

    def distance_to_max_velocity(self):
        # Calculate distance to reach max velocity
        return (self.m_constraints.max_velocity**2 - self.m_initial.velocity**2) / (2 * self.m_constraints.maxAcceleration)

    def total_time(self):
        # Returns the total time the profile takes to reach the goal
        return self.m_endDeccel

    def is_finished(self, t):
        # Returns true if the profile has reached the goal
        return t >= self.total_time()

    @staticmethod
    def should_flip_acceleration(initial, goal):
        # Returns true if the profile inverted
        return initial.position > goal.position

    def direct(self, in_state):
        # Flip the sign of the velocity and position if the profile is inverted
        result = State(in_state.position, in_state.velocity)
        result.position *= self.m_direction
        result.velocity *= self.m_direction
        return result