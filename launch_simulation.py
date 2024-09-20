import threading
import time
import queue
from environment_setup import client, world, blueprint_library, carla_map
from track_graph_generation import track_graph
from stations_and_spawn import stations, spawn_node_id
from collision_avoidance import segment_reservations
from pod import Pod

# Queue to receive pod dispatch commands
pod_dispatch_queue = queue.Queue()

# List to keep track of active pods
active_pods = []

def main_simulation_loop():
    while True:
        try:
            # Check for new pod dispatch commands
            if not pod_dispatch_queue.empty():
                dispatch_info = pod_dispatch_queue.get()
                dispatch_pod(dispatch_info['start_station'], dispatch_info['end_station'], dispatch_info['pod_id'])
            # Perform other simulation tasks if needed
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Simulation terminated.")
            # Clean up
            for pod in active_pods:
                if pod.vehicle is not None:
                    pod.vehicle.destroy()
            break

def dispatch_pod(start_station_label, end_station_label, pod_id):
    start_station = stations[start_station_label]
    end_station = stations[end_station_label]

    start_node_id = start_station['id']
    end_node_id = end_station['id']

    pod = Pod(world, blueprint_library, pod_id, track_graph, segment_reservations, start_node_id, end_node_id)
    # Start pod operation in a separate thread
    pod_thread = threading.Thread(target=pod.run)
    pod_thread.start()
    active_pods.append(pod)

if __name__ == "__main__":
    print("Simulation initialized. Waiting for pod dispatch commands...")
    simulation_thread = threading.Thread(target=main_simulation_loop)
    simulation_thread.start()