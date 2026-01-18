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

class Pipe:
    def __init__(self, name, start, end, diameter_in_inches):
        self.name = name
        self.start = start
        self.end = end
        self.diameter_in_inches = diameter_in_inches
        self.length_in_feet = math.dist(start, end)
        self.outputs = []
        self.solved = False
        self.endingPressures = np.arange(0, 100, 1) # Example pressures from 20 to 100 psi
        self.startingPressures = [] 
        self.flows = []
        self.operatingPressureStart = None
        self.operatingPressureEnd = None
        self.operatingFlow = None

    def frictionLoss(self, flow_gpm: float) -> float:
        """
        Calculate the pressure loss (psi) due to friction in poly piping.
        Uses the Hazen-Williams equation for water at ~60°F.

        Assumed constants:
        - Hazen-Williams coefficient (C) for poly pipe: 150
        - Water temperature: ~60°F
        - Flow in gallons per minute (GPM)
        - Length in feet
        - Diameter in inches

        Returns:
            Pressure loss in psi
        """
        C = 150  # Hazen-Williams roughness coefficient for poly pipe
        Q = flow_gpm  # Flow rate in GPM
        d = self.diameter_in_inches  # Diameter in inches
        L = self.length_in_feet  # Length in feet

        # Hazen-Williams formula for pressure loss (psi):
        #   P = 4.52 * (Q^1.85) / (C^1.85 * d^4.87) * L
        pressure_loss = 4.52 * (Q ** 1.85) / (C ** 1.85 * d ** 4.87) * L
        return pressure_loss
    
    def add_output(self, output):
        self.outputs.append(output)

    def get_outputs(self):
        return self.outputs

    def getFlow(self, pressure):
        if not self.solved:
            self.solve()

        if pressure < self.startingPressures[0] or pressure > self.startingPressures[-1]:
            raise ValueError(f"Pressure {pressure:.2f} out of bounds for {self.name}'s solved range.")
           
        return interp1(self.startingPressures, self.flows, pressure)

    def solve(self):
        for pressure in self.endingPressures:
            flow = 0.0
            for output in self.outputs:
                flow += output.getFlow(pressure)

            pressure_loss = self.frictionLoss(flow)
            starting_pressure = pressure + pressure_loss
            self.startingPressures.append(starting_pressure)
            self.flows.append(flow)
        
        self.solved = True

    def setOperatingPressure(self, pressure):
        self.operatingPressureStart = pressure
        self.operatingPressureEnd = interp1(self.startingPressures, self.endingPressures, pressure)
        self.operatingFlow = interp1(self.startingPressures, self.flows, pressure)
        for output in self.outputs:
            output.setOperatingPressure(self.operatingPressureEnd)

    def getOperatingPressure(self):
        if self.operatingPressureStart is None:
            raise ValueError("Operating pressure not set.")
        return self.operatingPressureStart

    def getOperatingFlow(self):
        if self.operatingPressureStart is None:
            raise ValueError("Operating pressure not set.")
        return self.operatingFlow



        
    

    
    
    
    