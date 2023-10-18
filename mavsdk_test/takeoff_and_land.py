#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

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

    await drone.action.set_current_speed(5)
    print("[DEBUG] Printing position:")
    asyncio.ensure_future(print_position(drone))

    await asyncio.sleep(10)
    
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
