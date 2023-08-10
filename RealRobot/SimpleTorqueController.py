import control


class SimpleTorqueController:
    def __init__(self):
        self.m = 7.57 + 2.916  # Mass calf + foot
        self.length = 0.4186
        self.g = 9.8
        self.A = [[0, 1], [self.g / self.length, 0]]
        self.B = [[0], [1 / (self.m * (self.length ** 2))]]
        self.C = [[1, 0], [0, 1]]
        self.D = [[0], [0]]
        self.poles = [-5, -10]

    def torque_linear_controller(self, currentPos, currentVec, desiredPos, desiredVec):
        K = control.place(self.A, self.B, self.poles)
        thetaMatrix = [[currentPos - desiredPos], [currentVec - desiredVec]]
        return -(K @ thetaMatrix) / 80
