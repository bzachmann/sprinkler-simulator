import math
import numpy as np
from MathFunctions import interp1



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



        
    

    
    
    
    