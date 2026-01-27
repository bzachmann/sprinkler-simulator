from MathFunctions import interp1


class CycleStopValve:

    _reducedPressureFalloff = {
        "flow": [0, 34],
        "pressureFalloff": [0, 20]
    }

    _frictionLoss = {
        "flow": [0, 22, 31],
        "pressureLoss": [0, 12, 35]
    }

    def __init__(self, set_point_psi):
        self.set_point_psi = set_point_psi

    def getMinimumInletPressure(self, flow_gpm):
        """
        Calculate the minimum inlet pressure (in psi) required for the cycle stop valve
        to maintain its set point pressure.

        :return: Minimum inlet pressure (psi)
        """

        outlet_pressure_psi = self.getOutletPressure(flow_gpm)
        friction_loss_psi = interp1(
            CycleStopValve._frictionLoss["flow"],
            CycleStopValve._frictionLoss["pressureLoss"],
            flow_gpm,
        )

        return outlet_pressure_psi + friction_loss_psi

    def getOutletPressure(self, flow_gpm):
        """
        Given an inlet pressure (in psi) and flow rate (in gpm),
        calculate the outlet pressure (in psi) of the cycle stop valve.

        :param flow_gpm: Flow rate (gpm)
        :param inlet_pressure_psi: Inlet pressure (psi)
        :return: Outlet pressure (psi)
        """
        if flow_gpm <= 0:
            return self.set_point_psi

        pressure_falloff = interp1(
            CycleStopValve._reducedPressureFalloff["flow"],
            CycleStopValve._reducedPressureFalloff["pressureFalloff"],
            flow_gpm,
        )

        outlet_pressure_psi = self.set_point_psi - pressure_falloff
        return max(outlet_pressure_psi, 0)