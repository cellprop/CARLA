import threading

segment_reservations = {}
segment_lock = threading.Lock()

def reserve_segment(pod_id, segment):
    with segment_lock:
        if segment not in segment_reservations:
            segment_reservations[segment] = pod_id
            return True
        else:
            return False

def release_segment(pod_id, segment):
    with segment_lock:
        if segment_reservations.get(segment) == pod_id:
            del segment_reservations[segment]