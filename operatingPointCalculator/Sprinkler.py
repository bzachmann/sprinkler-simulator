from MathFunctions import interp1
import numpy as np

class Sprinkler:
    # lookup tables for different sprinkler models (pressure in psi : flow in gpm)
    # Store lookup tables as a dict of model: [pressures, flows]
    _lookup_tables = {
        "42sa_3.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0,   2.3,    2.7,    3.1,    3.5,    3.8],
            "radius":   [0.0,   36,     38,     40,     40,     40]  
        },
        "42sa_4.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0,   2.9,    3.5,    4.0,    4.4,    4.8],
            "radius":   [0.0,   37,     40,     42,     42,     42]
        },
        "42sa_5.0": {
            "pressure": [0,     25,     35,     45,     55,     65],
            "flow":     [0.0,   3.7,    4.5,    5.1,    5.7,    6.2],
            "radius":   [0.0,   39,     41,     45,     45,     45]
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
    
    def getOperatingRadius(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        radius = interp1(self.lookup_table["pressure"], self.lookup_table["radius"], self.operatingPressure)
        return (min(radius, self.max_radius), self.operatingPointValid)
    
    def getHeight(self, runtime_minutes):
        """
        Calculate the height representing the amount of water spread across the sector.
        The height is proportional to the total water (cubic inches) divided by the sector area.
        """
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")

        # Convert theta from degrees to radians
        theta_rad = np.deg2rad(abs(self.theta_deg))
        # Area of the sector (slice of a circle)
        sector_area_sqft = 0.5 * (self.getOperatingRadius()[0] ** 2) * theta_rad
        sector_area_sqinches = sector_area_sqft * 144  # Convert square feet to square inches
        # Total water applied (gallons)
        total_gallons = self.getOperatingFlow()[0] * runtime_minutes
        # Convert gallons to cubic inches (1 gallon = 231 cubic inches)
        total_cubic_inches = total_gallons * 231
        # Height = total water (cubic inches) / area (if area > 0)
        if sector_area_sqinches > 0:
            height = total_cubic_inches / sector_area_sqinches
        else:
            height = 0

        return (height, self.operatingPointValid)

# Example usage:
# sprinkler = Sprinkler("42sa_3.0")
# flow = sprinkler.getFlow(45)  # Interpolates between 40 and 50 psi