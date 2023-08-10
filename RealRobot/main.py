import framework
from ODriveController import ODriveController
from Robot import Robot
from Joint import JointTypes
from HURONJoint import HURONJoint
from TorqueMotor import TorqueMotor
from HURONEncoder import HURONEncoder
from SimpleTorqueController import SimpleTorqueController
import time
import math

if __name__ == '__main__':
    # Parameters
    velocity_limit = 15.0
    current_limit = 70.0
    gear_ratio_1 = 2.0
    gear_ratio_2 = 40.0

    # ODrives
    left_hip_pitch_od = ODriveController("can0", 0x1)
    left_knee_pitch_od = ODriveController("can0", 0x0)
    right_hip_pitch_od = ODriveController("can1", 0x7)
    right_knee_pitch_od = ODriveController("can1", 0x6)

    # Motors
    left_hip_pitch_motor = TorqueMotor(left_hip_pitch_od)
    left_knee_pitch_motor = TorqueMotor(left_knee_pitch_od)
    right_hip_pitch_motor = TorqueMotor(right_hip_pitch_od)
    right_knee_pitch_motor = TorqueMotor(right_knee_pitch_od)

    left_hip_pitch_motor.configure(
        velocity_limit=velocity_limit, current_limit=current_limit)
    left_knee_pitch_motor.configure(
        velocity_limit=velocity_limit, current_limit=current_limit)
    right_hip_pitch_motor.configure(
        velocity_limit=velocity_limit, current_limit=current_limit)
    right_knee_pitch_motor.configure(
        velocity_limit=velocity_limit, current_limit=current_limit)

    # Encoders
    left_hip_pitch_enc = HURONEncoder(left_hip_pitch_od)
    left_knee_pitch_enc = HURONEncoder(left_knee_pitch_od)
    right_hip_pitch_enc = HURONEncoder(right_hip_pitch_od)
    right_knee_pitch_enc = HURONEncoder(right_knee_pitch_od)

    # Joints
    left_hip_pitch_joint = HURONJoint(
        JointTypes.REVOLUTE,
        left_hip_pitch_motor,
        encoder=left_hip_pitch_enc,
        gear_ratio_1=gear_ratio_1,
        gear_ratio_2=gear_ratio_2)
    left_knee_pitch_joint = HURONJoint(
        JointTypes.REVOLUTE,
        left_knee_pitch_motor,
        encoder=left_knee_pitch_enc,
        gear_ratio_1=gear_ratio_1,
        gear_ratio_2=gear_ratio_2)
    right_hip_pitch_joint = HURONJoint(
        JointTypes.REVOLUTE,
        right_hip_pitch_motor,
        encoder=right_hip_pitch_enc,
        gear_ratio_1=gear_ratio_1,
        gear_ratio_2=gear_ratio_2)
    right_knee_pitch_joint = HURONJoint(
        JointTypes.REVOLUTE,
        right_knee_pitch_motor,
        encoder=right_knee_pitch_enc,
        gear_ratio_1=gear_ratio_1,
        gear_ratio_2=gear_ratio_2)

    # Calibrate ODrives
    print("Calibrating...")
    # left_hip_pitch_od.calibrate()
    # right_hip_pitch_od.calibrate()
    # time.sleep(25)
    right_knee_pitch_od.calibrate()
    # left_knee_pitch_od.calibrate()
    time.sleep(25)

    print("Setting up...")
    # left_hip_pitch_od.set_up()
    # left_knee_pitch_od.set_up()
    # right_hip_pitch_od.set_up()
    right_knee_pitch_od.set_up()

    # robot = Robot()
    # robot.setup()

    # Move right knee
    print(f"Initial Right knee: {left_knee_pitch_joint.get_position()} rad")
    print()

    knee_control = SimpleTorqueController
    desiredPos = 30
    desiredVec = 10

    print("Moving knee joint by torque control...")
    # right_knee_pitch_joint.move(knee_control.torque_linear_controller(right_knee_pitch_joint.get_position(),
    #                                                                   desiredPos,
    #                                                                   right_knee_pitch_joint.get_velocity(),
    #

    start_time = time.time()

    while time.time() - start_time < 4:  # seconds

        torque = knee_control.torque_linear_controller(right_knee_pitch_joint.get_position(),
                                                       desiredPos,
                                                       right_knee_pitch_joint.get_velocity(),
                                                       desiredVec)
        print(torque)
        # rpos = math.degrees(right_knee_pitch_joint.get_position())
        # rvel = math.degrees(right_knee_pitch_joint.get_velocity())
        # print(f"[Right knee]: trpos: {rpos} deg\trvel: {rvel} deg/s")

    print("Stopping joints...")
    # left_knee_pitch_joint.stop()
    right_knee_pitch_joint.stop()
    # left_hip_pitch_joint.stop()
    # right_hip_pitch_joint.stop()

    while time.time() - start_time < 1:  # seconds
        rpos = math.degrees(right_knee_pitch_joint.get_position())
        rvel = math.degrees(right_knee_pitch_joint.get_velocity())
        print(f"[Right knee]: trpos: {rpos} deg\trvel: {rvel} deg/s")

    print("Terminating joint...")
    # left_hip_pitch_od.terminate()
    # left_knee_pitch_od.terminate()
    # right_hip_pitch_od.terminate()
    right_knee_pitch_od.terminate()

    framework.loop()

    framework.terminate()
