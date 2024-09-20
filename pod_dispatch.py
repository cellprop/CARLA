import sys
from launch_simulation import pod_dispatch_queue

def pod_dispatch_interface():
    pod_id = 1
    while True:
        print("\nEnter pod dispatch parameters:")
        start_station = input("Start Station (A/B/C/D): ").strip().upper()
        end_station = input("End Station (A/B/C/D): ").strip().upper()
        if start_station not in ['A', 'B', 'C', 'D'] or end_station not in ['A', 'B', 'C', 'D']:
            print("Invalid station input. Please enter A, B, C, or D.")
            continue
        if start_station == end_station:
            print("Start and end stations cannot be the same.")
            continue
        dispatch_info = {
            'start_station': start_station,
            'end_station': end_station,
            'pod_id': pod_id
        }
        pod_dispatch_queue.put(dispatch_info)
        print(f"Pod {pod_id} dispatched from {start_station} to {end_station}.")
        pod_id += 1

if __name__ == "__main__":
    pod_dispatch_interface()