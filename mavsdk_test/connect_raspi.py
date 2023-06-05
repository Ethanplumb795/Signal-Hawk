from pymavlink import mavutil

# Set BAUD rate:


# Start a connection listening on via USB port (rpi4b)
print("Creating a connection...")
the_connection = mavutil.mavlink_connection('udpin:localhost:14540')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
print("Waiting for heartbeat...")
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Once connected, use 'the_connection' to get and send messages
