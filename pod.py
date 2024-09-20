import carla
import time
import threading
from path_planning import plan_path
from collision_avoidance import reserve_segment, release_segment

class Pod:
    def __init__(self, world, blueprint_library, pod_id, track_graph, segment_reservations, start_node_id, end_node_id):
        self.world = world
        self.blueprint_library = blueprint_library
        self.pod_id = pod_id
        self.track_graph = track_graph
        self.segment_reservations = segment_reservations
        self.current_node_id = spawn_node_id  # Initialized at the spawn point
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.vehicle = None
        self.state = 'En Route to Pick-Up'
        self.path = []
        self.speed = 20.0  # Cruising speed (km/h)
        self.turn_speed = 10.0  # Turn speed (km/h)
        self.thread = None

    def spawn_pod(self):
        pod_bp = self.blueprint_library.filter('vehicle.audi.tt')[0]  # Use your pod model
        spawn_transform = self.track_graph.nodes[spawn_node_id]['waypoint'].transform
        self.vehicle = self.world.spawn_actor(pod_bp, spawn_transform)
        self.vehicle.set_autopilot(False)
        print(f"Pod {self.pod_id} spawned.")

    def run(self):
        self.spawn_pod()
        # Plan path to start station
        self.plan_and_move(self.start_node_id, 'Start Station')
        # Simulate passenger pick-up
        print(f"Pod {self.pod_id} arrived at start station for pick-up.")
        time.sleep(2)  # Boarding time
        self.state = 'En Route to Destination'
        # Plan path to end station
        self.plan_and_move(self.end_node_id, 'End Station')
        # Simulate passenger drop-off
        print(f"Pod {self.pod_id} arrived at end station for drop-off.")
        time.sleep(2)  # Disembarking time
        self.state = 'Returning to Spawn Point'
        # Plan path back to spawn point
        self.plan_and_move(spawn_node_id, 'Spawn Point')
        # Remove pod from simulation
        print(f"Pod {self.pod_id} has returned to spawn point and will be removed.")
        self.vehicle.destroy()

    def plan_and_move(self, destination_node_id, destination_label):
        avoid_node_ids = set(station['id'] for label, station in stations.items() if station['id'] not in [self.start_node_id, self.end_node_id])
        self.path = plan_path(self.track_graph, self.current_node_id, destination_node_id, avoid_node_ids)
        if not self.path:
            print(f"Pod {self.pod_id}: No path found to {destination_label}.")
            return
        self.move_along_path()
        self.current_node_id = destination_node_id

    def move_along_path(self):
        for index in range(len(self.path) - 1):
            node_id = self.path[index]
            next_node_id = self.path[index + 1]
            segment = (node_id, next_node_id)

            # Attempt to reserve the segment
            while not reserve_segment(self.pod_id, segment):
                time.sleep(0.5)  # Wait before trying again

            # Move to the next node
            self.navigate_to(next_node_id)

            # Release the previous segment
            if index > 0:
                prev_segment = (self.path[index - 1], node_id)
                release_segment(self.pod_id, prev_segment)

        # Release the last segment
        last_segment = (self.path[-2], self.path[-1]) if len(self.path) > 1 else None
        if last_segment:
            release_segment(self.pod_id, last_segment)

    def navigate_to(self, destination_node_id):
        destination_waypoint = self.track_graph.nodes[destination_node_id]['waypoint']
        destination_transform = destination_waypoint.transform

        # Implement movement logic
        control = carla.VehicleControl()
        while True:
            current_location = self.vehicle.get_location()
            distance = current_location.distance(destination_transform.location)

            # Simple proportional controller for throttle
            if distance > 5.0:
                control.throttle = 0.6
            elif distance > 2.0:
                control.throttle = 0.3
            else:
                control.throttle = 0.0
                control.brake = 1.0

            # Set steering based on direction to waypoint
            control.steer = self.compute_steering(current_location, destination_transform.location)

            self.vehicle.apply_control(control)

            if distance <= 2.0:
                # Stop the vehicle
                control.throttle = 0.0
                control.brake = 1.0
                self.vehicle.apply_control(control)
                break

            time.sleep(0.05)  # Control loop delay

    def compute_steering(self, current_location, target_location):
        # Compute the required steering angle
        # This is a simplified example; consider using a proper vehicle controller
        vehicle_transform = self.vehicle.get_transform()
        yaw = vehicle_transform.rotation.yaw

        direction_vector = target_location - current_location
        desired_yaw = direction_vector.make_unit_vector().rotation.yaw

        steer_angle = (desired_yaw - yaw) / 180.0  # Normalize to [-1, 1]

        # Clamp steer_angle to valid range
        steer_angle = max(min(steer_angle, 1.0), -1.0)

        return steer_angle