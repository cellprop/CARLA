import carla
import networkx as nx

def build_track_graph(carla_map):
    track_graph = nx.DiGraph()
    topology = carla_map.get_topology()

    for segment in topology:
        wp_start = segment[0]
        wp_end = segment[1]

        loc_start = wp_start.transform.location
        loc_end = wp_end.transform.location

        id_start = (loc_start.x, loc_start.y, loc_start.z)
        id_end = (loc_end.x, loc_end.y, loc_end.z)

        # Add nodes with waypoint information
        track_graph.add_node(id_start, waypoint=wp_start)
        track_graph.add_node(id_end, waypoint=wp_end)

        # Calculate distance as weight
        distance = loc_start.distance(loc_end)

        # Add edge in the direction of the road
        track_graph.add_edge(id_start, id_end, weight=distance)

        # If the road is bidirectional, add the reverse edge
        if wp_start.is_bidirectional():
            track_graph.add_edge(id_end, id_start, weight=distance)

    return track_graph

# Build the track graph
track_graph = build_track_graph(carla_map)