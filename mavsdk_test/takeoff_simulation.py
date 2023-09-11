from pymavlink import mavutil

# Start a connection listening on a UDP port (JMavSim)
the_connection = mavutil.mavlink_connection('udpin:localhost:14540')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Once connected, use 'the_connection' to get and send messages
try:
    altitude = the_connection.messages['GPS_RAW_INT'].alt  # Note, you can access message fields as attributes!
    timestamp = the_connection.time_since('GPS_RAW_INT')
    print(f"Timestamp: {timestamp}\nAltitude: {altitude}")
except:
    print('No GPS_RAW_INT message received')

try:
    msg = the_connection.recv_match(type='SYS_STATUS',blocking=True)
    print(f"Status: {msg}\n")
except:
    print("No SYS_STATUS received.\n")

# Takeoff
# Before running these commands enter the following
# module load message
# GUIDED
# arm throttle
# takeoff 10

# Then, move the drone
try:
    msg = the_connection.mav.command_long_encode(
            the_connection.target_system, # Target system ID
            connection.target_component, # Target component ID
            mavutil.mavlink.SET_POSITION_TARGET_LOCAL_NED, # ID of command to send
            0,      # System Time since boot (ms)
            0,      # System ID of vehicle
            0,      # Target Component (Can also be component ID of flight controller)
            1,      # Coordinate Frame
            3576,   # Type Mask (Use Position)
            100,    # 100m north of NED
            0,      # 0m east of NED
            0,      # 0m down of NED
            0,      # vx
            0,      # vy
            0,      # vz
            0,      # afx
            0,      # afy
            0,      # afz
            )
    connection.mav.send(msg)
    response = connection.recv_match(type="COMMANND_ACK", blocking=True)
    if response:
        print("Command accepted: " + response)
    else:
        print("Command not accepted.")
except:
    print("[ERROR] ") # look up exceptions in Python
