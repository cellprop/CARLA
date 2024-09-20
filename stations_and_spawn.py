import carla

# Provide actual coordinates for stations and spawn point
station_coords = {
    'A': carla.Location(x=..., y=..., z=...),  # Replace with actual coordinates
    'B': carla.Location(x=..., y=..., z=...),
    'C': carla.Location(x=..., y=..., z=...),
    'D': carla.Location(x=..., y=..., z=...)
}

spawn_point_coord = carla.Location(x=..., y=..., z=...)  # Replace with actual coordinates

def get_closest_node_id(carla_map, location):
    waypoint = carla_map.get_waypoint(location, project_to_road=True, lane_type=carla.LaneType.Driving)
    loc = waypoint.transform.location
    node_id = (loc.x, loc.y, loc.z)
    return node_id, waypoint

# Map stations to waypoints
stations = {}
for label, coord in station_coords.items():
    node_id, waypoint = get_closest_node_id(carla_map, coord)
    stations[label] = {
        'id': node_id,
        'waypoint': waypoint
    }

# Map spawn point to waypoint
spawn_node_id, spawn_waypoint = get_closest_node_id(carla_map, spawn_point_coord)