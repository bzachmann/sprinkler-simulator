from Pipe import Pipe
from Sprinkler import Sprinkler

class Component:
    """Base class for zone components."""
    pass

class PipeComponent(Pipe, Component):
    pass

class SprinklerComponent(Sprinkler, Component):
    pass

class Zone:
    def __init__(self, name):
        self.name = name
        self.components = []  # Ordered list of PipeComponent and SprinklerComponent

    def add_pipe(self, pipe: Pipe):
        self.components.append(PipeComponent(pipe.diameter_in_inches, pipe.length_in_feet))

    def add_sprinkler(self, sprinkler: Sprinkler):
        self.components.append(SprinklerComponent(sprinkler.name))

    def is_sprinkler(self, component: Component) -> bool:
        return isinstance(component, SprinklerComponent)

    def is_pipe(self, component: Component) -> bool:
        return isinstance(component, PipeComponent)
    
    def calculate_pressure_and_input_flow(self, ending_pressure: float):
        """
        Calculates the pressure and input flow at the start of the zone,
        given the ending pressure at the last component.
        Returns a tuple: (start_pressure, input_flow)
        """
        pressure = ending_pressure
        flow = 0.0

        # Traverse components in reverse to propagate pressure and flow backwards
        for component in reversed(self.components):
            if self.is_sprinkler(component):
                flow += component.getFlow(pressure) 
            elif self.is_pipe(component):
                pressure += component.frictionLoss(flow)
            else:
                raise TypeError("Unknown component type in zone.")

        return pressure, flow

    def __repr__(self):
        return f"Zone(name={self.name}, components={self.components})"