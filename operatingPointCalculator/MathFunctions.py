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