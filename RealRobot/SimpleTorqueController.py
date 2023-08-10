import control


class SimpleTorqueController:
    def __init__(self):
        self.m = 7.57
        self.length = 41.86
        self.g = 9.8
        self.A = [[0, 1], [self.g / self.length, 0]]
        self.B = [[0], [1 / (self.m * (self.length ** 2))]]
        self.C = [[1, 0], [0, 1]]
        self.D = [[0], [0]]
        self.poles = [-10, -20]

    def torque_linear_controller(self, currentPos, currentVec, desiredPos, desiredVec):
        K = control.place(self.A, self.B, self.poles)
        thetaMatrix = [[currentPos - desiredPos], [currentVec - desiredVec]]
        return -K * thetaMatrix
