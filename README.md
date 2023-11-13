# Signal-Hawk
Code to control the Signal Hawk, an end-to-end solution to locate the source of a signal by using a drone.

# Getting Started
To begin development, please start with the following commands:

cd /path/to/Signal-Hawk/

python3 -m venv venv # This will be ignored by .gitignore

source venv/bin/activate

pip3 install -r requirements.txt

# Building with c++
cd Signal-Hawk/mavsdk_cpp/src/takeoff_and_land

cmake -DCMAKE_PREFIX_PATH=/home/signalhawk/src/MAVSDK/install -Bbuild -H.

cmake --build build -j4

./build/takeoff_and_land udp://:14540

# Run Simulation
cd PX4-Autopilot

make px4_sitl jmavsim
