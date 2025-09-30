import math

class Pipe:
    def __init__(self, diameter_in_inches: float, length_in_feet: float):
        self.diameter_in_inches = diameter_in_inches
        self.length_in_feet = length_in_feet

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