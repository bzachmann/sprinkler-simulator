class WellPump:
    # Class variable shared by all instances
    # This should be set statically, not constructed at runtime
    flow_head_table = {
        # Example: 10: 120, 20: 110, 30: 95
        # Fill in with actual flow (gpm): total head (ft) pairs as needed
        0: 374,
        1: 374,
        2: 374,
        3: 374,
        4: 374,
        5: 350,
        6: 348,
        7: 345,
        8: 340,
        9: 335,
        10: 330,
        11: 325,
        12: 320,
        13: 315,
        14: 305,
        15: 300,
        16: 290,
        17: 280,
        18: 270,
        19: 255,
        20: 248,
        21: 230,
        22: 220,
        23: 205,
        24: 190,
        25: 175,
        26: 155,
        27: 140,
        28: 125,
        29: 105,
        30: 80,
    }

    def __init__(self, depth):
        """
        Initialize the WellPump.

        :param depth: Depth of the well in feet.
        """
        self.depth = depth

    def get_flow_at_pressure(self, pressure_psi):
        """
        Given an operating pressure (in psi), calculate the flow (gpm) the pump can deliver.

        :param pressure_psi: Operating pressure at the surface (psi)
        :return: Flow rate (gpm) or None if outside pump curve
        """
        # Convert pressure (psi) to head (ft): 1 psi = 2.31 ft H2O
        pressure_head = pressure_psi * 2.31
        total_head = pressure_head + self.depth

        # Find the closest head in the table (interpolating if needed)
        sorted_items = sorted(self.flow_head_table.items())
        for i, (flow, head) in enumerate(sorted_items):
            if head <= total_head:
                if i == 0:
                    return flow
                prev_flow, prev_head = sorted_items[i - 1]
                # Linear interpolation between prev and current
                if prev_head == head:
                    return flow
                ratio = (total_head - head) / (prev_head - head)
                interpolated_flow = flow + ratio * (prev_flow - flow)
                return interpolated_flow
        # If total_head is higher than any in the table, return the lowest flow
        return sorted_items[-1][0]
    
    def get_pressure_at_flow(self, flow_gpm):
        """
        Given a flow rate (in gpm), calculate the operating pressure (in psi) the pump can provide.

        :param flow_gpm: Flow rate (gpm)
        :return: Operating pressure (psi) or None if outside pump curve
        """
        # Find the closest flow in the table (interpolating if needed)
        sorted_items = sorted(self.flow_head_table.items())
        for i, (flow, head) in enumerate(sorted_items):
            if flow_gpm <= flow:
                if i == 0:
                    total_head = head
                else:
                    prev_flow, prev_head = sorted_items[i - 1]
                    # Linear interpolation between prev and current
                    if prev_flow == flow:
                        total_head = head
                    else:
                        ratio = (flow_gpm - flow) / (prev_flow - flow)
                        total_head = head + ratio * (prev_head - head)
                pressure_head = total_head - self.depth
                pressure_psi = pressure_head / 2.31
                return pressure_psi
        # If flow_gpm is higher than any in the table, return the lowest pressure
        lowest_flow, lowest_head = sorted_items[-1]
        pressure_head = lowest_head - self.depth
        pressure_psi = pressure_head / 2.31
        return pressure_psi
    
    def get_head_pressure_at_flow(self, flow_gpm):
        """
        Given a flow rate (in gpm), calculate the operating pressure (in psi) the pump can provide.

        :param flow_gpm: Flow rate (gpm)
        :return: Operating pressure (psi) or None if outside pump curve
        """
        # Find the closest flow in the table (interpolating if needed)
        sorted_items = sorted(self.flow_head_table.items())
        for i, (flow, head) in enumerate(sorted_items):
            if flow_gpm <= flow:
                if i == 0:
                    pressure_psi = head / 2.31
                    return pressure_psi
                else:
                    prev_flow, prev_head = sorted_items[i - 1]
                    # Linear interpolation between prev and current
                    if prev_flow == flow:
                        pressure_psi = head / 2.31
                        return pressure_psi
                    ratio = (flow_gpm - flow) / (prev_flow - flow)
                    interpolated_head = head + ratio * (prev_head - head)
                    pressure_psi = interpolated_head / 2.31
                    return pressure_psi
        # If flow_gpm is higher than any in the table, return the lowest pressure
        lowest_flow, lowest_head = sorted_items[-1]
        pressure_psi = lowest_head / 2.31
        return pressure_psi
