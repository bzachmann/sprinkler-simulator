class ZoneStart:
    def __init__(self, zone_id, location, runtime_minutes):
        self.zone_id = zone_id
        self.location = location
        self.runtime_minutes = runtime_minutes
        self.outputs = []

        self.operatingPressure = None
        self.operatingFlow = None
        self.operatingPointValid = None

    def add_output(self, output):
        self.outputs.append(output)

    def get_outputs(self):
        return self.outputs
    
    def setOperatingPressure(self, pressure):
        self.operatingPressure = pressure
        self.operatingFlow = self.getFlow(self.operatingPressure) #this will solve, if not already solved
        self.operatingPointValid = True

        for output in self.outputs:
            valid = output.setOperatingPressure(pressure)
            self.operatingPointValid = self.operatingPointValid and valid

        return self.operatingPointValid

    def getOperatingFlow(self):
        if self.operatingPressure is None:
            raise ValueError("Operating pressure not set.")
        return (self.operatingFlow, self.operatingPointValid)

    def getFlow(self, pressure):
        total_flow = 0.0
        for output in self.outputs:
            total_flow += output.getFlow(pressure)
        return total_flow