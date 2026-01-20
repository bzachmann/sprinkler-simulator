from MathFunctions import interp1

class Sprinkler:
    # lookup tables for different sprinkler models (pressure in psi : flow in gpm)
    # Store lookup tables as a dict of model: [pressures, flows]
    _lookup_tables = {
        "42sa_3.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0,   2.3,    2.7,    3.1,    3.5,    3.8]
        },
        "42sa_4.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0, 2.9,   3.5,    4.0,    4.4,    4.8]
        },
        "42sa_5.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0,   3.7,    4.5,    5.1,    5.7,    6.2]
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
        self.operatingPointValid = None
        self.fittingPressureLoss = 5  # psi, assumed loss through elbows and fittings

        if model not in self._lookup_tables:
            raise ValueError(f"Unknown sprinkler model: {model}")
        self.lookup_table = self._lookup_tables[model]

    def getFlow(self, pressure):
        """
        Returns the flow (gpm) for the given pressure (psi).
        If the exact pressure is not in the table, interpolate linearly.
        """
        pressure = max(pressure - self.fittingPressureLoss, 0)
        
        #TODO handle pressures outside the table range
        #if pressure < self.lookup_table["pressure"][0] or pressure > self.lookup_table["pressure"][-1]:
        #    raise ValueError(f"Pressure {pressure} out of bounds for sprinkler model {self.model}.")
        
        return interp1(self.lookup_table["pressure"], self.lookup_table["flow"], pressure)
    
    def setOperatingPressure(self, pressure):
        self.operatingPressure = max(pressure - self.fittingPressureLoss, 0)
        self.operatingPointValid = True

        if self.operatingPressure < self.lookup_table["pressure"][1] or self.operatingPressure > self.lookup_table["pressure"][-1]:
            self.operatingPointValid = False
            print(f"Warning: Operating pressure {self.operatingPressure} psi is out of valid range for sprinkler {self.name} model {self.model}.")

        self.operatingFlow = self.getFlow(self.operatingPressure)
        return self.operatingPointValid

    def getOperatingFlow(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        return (self.operatingFlow, self.operatingPointValid)
    
    def getOperatingPressure(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        return (self.operatingPressure, self.operatingPointValid)
# Example usage:
# sprinkler = Sprinkler("42sa_3.0")
# flow = sprinkler.getFlow(45)  # Interpolates between 40 and 50 psi