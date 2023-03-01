from mavsdk import System

# 
drone = System()

# Connect
await drone.connect(system_address="udp://:14540")

# Arm and takeoff
await drone.action.arm()
await drone.action.takeoff()
