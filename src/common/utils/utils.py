import os

def is_inside_container():
    """Check if running inside a container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return any('docker' in line or 'kubepods' in line for line in ifh)
    except Exception:
        return False