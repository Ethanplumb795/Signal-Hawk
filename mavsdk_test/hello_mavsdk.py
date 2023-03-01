from mavsdk import System

drone = System()
await drone.connect(system_address="udp://:14540")
