from Motor import Motor
from ODriveController import ODriveController
from odrive.enums import InputMode, ControlMode


class PositionMotor(Motor):
    """
    Initialization to start reading the motor
    """

    def __init__(self, odrive: ODriveController):
        # Init CAN port and store database
        self._current_limit = None
        self._velocity_limit = None
        self._desired_value = 0
        self._odrive = odrive

    def configure(self, *args, **kwargs) -> bool:
        """Configure torque motor.

        Parameters:
        velocity_limit (float)
        current_limit (float)
        """
        self._velocity_limit = kwargs['velocity_limit']
        self._current_limit = kwargs['current_limit']

        self._odrive.configure(
            velocity_limit=self._velocity_limit,
            current_limit=self._current_limit,
            input_mode=InputMode.PASSTHROUGH,
            control_mode=ControlMode.TORQUE_CONTROL)

        return True

    def set_up(self, *args, **kwargs) -> None:
        self._odrive.set_up()

    def move_motor(self, goal: float) -> bool:
        print(f"Motor {self._odrive.can_id}: Setting torque to {goal}")
        self._desired_value = goal
        self._odrive.send_cmd("Set_Input_Pos", {'Input_Pos': goal})
        return True

    def stop_motor(self) -> bool:
        print(f"Motor {self._odrive.can_id}: Stopped")
        return self.move_motor(0)

    """
    Returns true if the motor reaches the desired value by positions
    """

    def reach_goal(self, print_value) -> bool:
        threshold = 0.6
        msg = self.bus.recv()
        arbID = ((self.axis << 5) | self.db.get_message_by_name(
            'Get_Encoder_Estimates').frame_id)
        if msg.arbitration_id == arbID:
            pos = self.db.decode_message('Get_Encoder_Estimates', msg.data)[
                'Pos_Estimate']
            if (self.axis > -1) and print_value:
                print("Axis")
                print(self.axis)
                print("Desired Position")
                print(self.desired_pos)
                print("Current Pos")
                print(pos)
                print("Error")
                print(abs(pos - self.desired_pos))
                print("")
            return abs(pos - self.desired_pos) <= threshold
        return False
