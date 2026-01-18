class ZoneStart:
    def __init__(self, zone_id, location, runtime_minutes):
        self.zone_id = zone_id
        self.location = location
        self.runtime_minutes = runtime_minutes
        self.outputs = []

        self.operatingPressure = None
        self.operatingFlow = None

    def add_output(self, output):
        self.outputs.append(output)

    def get_outputs(self):
        return self.outputs
    
    def setOperatingPressure(self, pressure):
        self.operatingPressure = pressure
        self.operatingFlow = 0.0
        for output in self.outputs:
            self.operatingFlow += output.getFlow(pressure) #this will solve downstream
            output.setOperatingPressure(pressure)

    def getOperatingFlow(self):
        return self.operatingFlow
    
    def getFlow(self, pressure):
        total_flow = 0.0
        for output in self.outputs:
            total_flow += output.getFlow(pressure)
        return total_flow