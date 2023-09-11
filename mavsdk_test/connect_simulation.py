from pymavlink import mavutil

# Start a connection listening on a UDP port (JMavSim)
connection = mavutil.mavlink_connection('udpin:localhost:14540')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))

# Once connected, use 'connection' to get and send messages
try:
    altitude = connection.messages['GPS_RAW_INT'].alt  # Note, you can access message fields as attributes!
    timestamp = connection.time_since('GPS_RAW_INT')
    print(f"Timestamp: {timestamp}\nAltitude: {altitude}")
except:
    print('No GPS_RAW_INT message received')

try:
    msg = connection.recv_match(type='SYS_STATUS',blocking=True)
    print(f"Status: {msg}\n")
except:
    print("No SYS_STATUS received.\n")
