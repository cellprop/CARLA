import carla
import random
import time
import sys

# Connect to the CARLA simulator
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
except Exception as e:
    print(f"Error connecting to CARLA: {e}")
    sys.exit(1)

# Load the custom map (replace 'YourCustomMap' with your actual map name)
try:
    world = client.load_world('YourCustomMap')
except Exception as e:
    print(f"Error loading map: {e}")
    sys.exit(1)

# Get the blueprint library
blueprint_library = world.get_blueprint_library()

# Get the map
carla_map = world.get_map()