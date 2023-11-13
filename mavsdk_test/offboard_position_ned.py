"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():

    print("Starting...")

    drone = System()
    await drone.connect()

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, -5m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -45.0, 0.0))
    await asyncio.sleep(20)

    print("-- Go 5m North, 0m East, -5m Down \
            within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(
            PositionNedYaw(2.0, 0.0, -2.0, 90.0))
    await asyncio.sleep(10)

    print("-- Go 5m North, 10m East, -5m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(2.0, 5.0, -10.0, 90.0))
    await asyncio.sleep(15)

    print("-- Go 0m North, 10m East, 0m Down \
            within local coordinate system, turn to face South")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 2.0, 0.0, 180.0))
    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed \
                with error code: {error._result.result}")
    
    print(" -- Returning to launch")
    await drone.action.return_to_launch()

    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        i = 0
        async for status_text in drone.telemetry.status_text():
            print(f"[DEBUG] Status: {status_text.type}: {status_text.text}")
            if i > 5:
                break
            i += 1
    except asyncio.CancelledError:
        return


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)
        break


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())

