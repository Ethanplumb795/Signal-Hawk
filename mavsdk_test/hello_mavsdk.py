from mavsdk import System

# 
drone = System()

# Connect
async def connect_drone():
    await drone.connect(system_address="udp://:14540")

# Arm and takeoff
async def arm_and_takeoff():
    await drone.action.arm()
    await drone.action.takeoff()

connect_drone()
arm_and_takeoff()