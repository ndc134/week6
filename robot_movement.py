import time

import pybullet as p
import pybullet_data


client = p.connect(p.GUI)

if client < 0:
    raise RuntimeError("Could not open the PyBullet GUI.")

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

plane_id = p.loadURDF("plane.urdf")

robot_position = [0, 0, 0.2]
robot_orientation = p.getQuaternionFromEuler([0, 0, 0])

robot_id = p.loadURDF(
    "husky/husky.urdf",
    robot_position,
    robot_orientation
)

print("Plane ID:", plane_id)
print("Robot ID:", robot_id)


number_of_joints = p.getNumJoints(robot_id)

print("Number of joints:", number_of_joints)

for joint_index in range(number_of_joints):
    joint_info = p.getJointInfo(robot_id, joint_index)
#index 1 is joint name according to pybullet documentation
    joint_name = joint_info[1].decode("utf-8")
#index 2 is joint type according to pybullet documentation.  index 0 is the joint index.
    joint_type = joint_info[2]

    print(
        "Joint index:",
        joint_index,
        "| Name:",
        joint_name,
        "| Type:",
        joint_type
    )

FRONT_LEFT_WHEEL = 2
FRONT_RIGHT_WHEEL =3
REAR_LEFT_WHEEL = 4
REAR_RIGHT_WHEEL = 5

LEFT_WHEELS = [FRONT_LEFT_WHEEL, REAR_LEFT_WHEEL]
RIGHT_WHEELS = [FRONT_RIGHT_WHEEL, REAR_RIGHT_WHEEL]

def set_wheel_speeds(robot_id, left_speed,right_speed):
    for wheel_joint in LEFT_WHEELS:
        p.setJointMotorControl2 (bodyIndex =robot_id, jointIndex = wheel_joint, controlMode = p.VELOCITY_CONTROL, 
                                 targetVelocity=left_speed, force=100)
    for wheel_joint in RIGHT_WHEELS:
                p.setJointMotorControl2 (bodyIndex=robot_id, jointIndex = wheel_joint, controlMode = p.VELOCITY_CONTROL, 
                                         targetVelocity=right_speed, force=100)
        

def stop_robot(robot_id):
     set_wheel_speeds(robot_id,0,0)

def run_for_duration(duration):
     start_time = time.perf_counter()

     while p.isConnected() and time.perf_counter() - start_time < duration:
          p.stepSimulation()
          time.sleep(1/240)



def move_forward (robot_id,speed,duration):
     print("moving forward")
     set_wheel_speeds(robot_id, left_speed= speed,right_speed= speed)

     run_for_duration(duration)
     stop_robot(robot_id)

def move_backward (robot_id,speed,duration):
     print("moving backward")
     set_wheel_speeds(robot_id, left_speed= -speed,right_speed= -speed)

     run_for_duration(duration)
     stop_robot(robot_id)

def turn_left (robot_id,speed,duration):
     print("turning left")
     set_wheel_speeds(robot_id, left_speed= -speed,right_speed= speed)

     run_for_duration(duration)
     stop_robot(robot_id)

def turn_right(robot_id,speed,duration):
     print("turning rihgt")
     set_wheel_speeds(robot_id, left_speed= speed,right_speed= -speed)

     run_for_duration(duration)
     stop_robot(robot_id)

move_forward(robot_id, 5, 2)
time.sleep(0.2)
turn_left(robot_id,5,3.5)
time.sleep(0.2)
move_forward(robot_id,10,2)
time.sleep(0.2)
move_backward(robot_id, 5, 2)
time.sleep(0.2)
turn_right(robot_id, 5,3.5)


while p.isConnected():
    p.stepSimulation()
    time.sleep(1 / 240)

