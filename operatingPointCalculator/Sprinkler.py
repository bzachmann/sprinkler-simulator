class Sprinkler:
    # lookup tables for different sprinkler models (pressure in psi : flow in gpm)
    _lookup_tables = {
        "42sa_3.0": {
            25: 2.3,
            35: 3.7,
            45: 3.1,
            55: 3.5,
            65: 3.8
        },
        "42sa_4.0": {
            25: 2.9,
            35: 3.5,
            45: 4.0,
            55: 4.4,
            65: 4.8
        },
        "42sa_5.0": {
            25: 3.7,
            35: 4.5,
            45: 5.1,
            55: 5.7,
            65: 6.2
        },
        # Add more models as needed
    }

    def __init__(self, name, model, location, left_edge_deg, theta_deg, max_radius):
        self.name = name
        self.model = model
        self.location = location
        self.left_edge_deg = left_edge_deg
        self.theta_deg = theta_deg
        self.max_radius = max_radius
        self.operatingPressure = None
        self.operatingFlow = None

        if model not in self._lookup_tables:
            raise ValueError(f"Unknown sprinkler model: {model}")
        self.lookup_table = self._lookup_tables[model]

    def getFlow(self, pressure):
        """
        Returns the flow (gpm) for the given pressure (psi).
        If the exact pressure is not in the table, interpolate linearly.
        """
        pressure = pressure - 5 #assume a 5 psi loss through elbows and fittings ##################################### CHANGE THIS LATER
        pressures = sorted(self.lookup_table.keys())
        if pressure <= pressures[0]:
            return self.lookup_table[pressures[0]]
        if pressure >= pressures[-1]:
            return self.lookup_table[pressures[-1]]

        # Linear interpolation
        for i in range(1, len(pressures)):
            p1, p2 = pressures[i-1], pressures[i]
            if p1 <= pressure <= p2:
                f1, f2 = self.lookup_table[p1], self.lookup_table[p2]
                # Linear interpolation formula
                return f1 + (f2 - f1) * (pressure - p1) / (p2 - p1)

        # Should not reach here
        raise ValueError("Pressure out of interpolation range.")
    
    def setOperatingPressure(self, pressure):
        self.operatingPressure = pressure
        self.operatingFlow = self.getFlow(pressure)

    def getOperatingFlow(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        return self.getFlow(self.operatingPressure)
    
    def getOperatingPressure(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        return self.operatingPressure
# Example usage:
# sprinkler = Sprinkler("42sa_3.0")
# flow = sprinkler.getFlow(45)  # Interpolates between 40 and 50 psi