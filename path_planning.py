import networkx as nx

def plan_path(track_graph, start_node_id, end_node_id, avoid_node_ids):
    temp_graph = track_graph.copy()
    # Remove nodes to avoid
    temp_graph.remove_nodes_from(avoid_node_ids)
    try:
        # Compute the shortest path using Dijkstra's algorithm
        path = nx.dijkstra_path(temp_graph, source=start_node_id, target=end_node_id, weight='weight')
    except nx.NetworkXNoPath:
        path = []
    return path
