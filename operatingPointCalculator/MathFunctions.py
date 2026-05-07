import math
import numpy as np

def interp1(x, y, xi):
    """Simple linear interpolation like MATLAB's interp1.

    Args:
        x: 1-D sequence of x coordinates (must be sorted ascending).
        y: 1-D sequence of y values (same length as x).
        xi: scalar x at which to interpolate.

    Behavior:
        - If xi <= x[0], returns y[0].
        - If xi >= x[-1], returns y[-1].
        - Otherwise performs linear interpolation between enclosing points.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be 1-D sequences")
    if x.size != y.size:
        raise ValueError("x and y must have the same length")
    if x.size == 0:
        raise ValueError("x and y must be non-empty")

    # Bounds handling (clamp to endpoints)
    if xi <= x[0]:
        return float(y[0])
    if xi >= x[-1]:
        return float(y[-1])

    # find the insertion index where x[idx] >= xi
    idx = np.searchsorted(x, xi)
    x1, x2 = x[idx - 1], x[idx]
    y1, y2 = y[idx - 1], y[idx]
    if x2 == x1:
        return float(y1)
    return float(y1 + (y2 - y1) * (xi - x1) / (x2 - x1))

def line_intersection(xs1, ys1, xs2, ys2):
    """
    Finds the first intersection point between two polylines defined by (xs1, ys1) and (xs2, ys2).
    Returns (x, y) of the intersection or None if no intersection is found.
    """
    for i in range(len(xs1) - 1):
        x1, y1 = xs1[i], ys1[i]
        x2, y2 = xs1[i + 1], ys1[i + 1]
        for j in range(len(xs2) - 1):
            x3, y3 = xs2[j], ys2[j]
            x4, y4 = xs2[j + 1], ys2[j + 1]

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                continue  # Parallel lines

            px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
            py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

            # Check if intersection is within both segments
            if (min(x1, x2) <= px <= max(x1, x2) and
                min(y1, y2) <= py <= max(y1, y2) and
                min(x3, x4) <= px <= max(x3, x4) and
                min(y3, y4) <= py <= max(y3, y4)):
                return (px, py)
    return None

# Function to add a partial cylinder (sector) to the surface
def add_partial_cylinder_to_surface(x, y, z, center, leftEdge_deg, theta_deg, radius, height):
    x_center, y_center = center
    # Normalize angles to 0-360 range
    leftEdge_deg = (leftEdge_deg % 360 + 360) % 360
    theta_deg = (theta_deg % 360 + 360) % 360
    # Calculate the distance and angle of each point from the center
    dx = x - x_center
    dy = y - y_center
    distance = np.sqrt(dx**2 + dy**2)
    # Angle from east (x-axis), counterclockwise, in degrees
    angles = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
    # Calculate end angle
    end_deg = (leftEdge_deg - theta_deg) % 360
    # Determine mask for sector
    if theta_deg < 0:
        if leftEdge_deg < end_deg:
            mask = (distance <= radius) & (angles >= leftEdge_deg) & (angles <= end_deg)
        else:
            mask = (distance <= radius) & ((angles >= leftEdge_deg) | (angles <= end_deg))
    else:
        if leftEdge_deg > end_deg:
            mask = (distance <= radius) & (angles <= leftEdge_deg) & (angles >= end_deg)
        else:
            mask = (distance <= radius) & ((angles <= leftEdge_deg) | (angles >= end_deg))
    z[mask] += height