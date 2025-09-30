from Zone import Zone
from Pipe import Pipe
from Sprinkler import Sprinkler
from WellPump import WellPump

zone1 = Zone(name="Front Lawn")

#TODO diameter is set to 0.95 assuming some buildup  in the pipes, should be changed to 1.0 for new pipes
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=50))
zone1.add_sprinkler(Sprinkler("42sa_5.0"))
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=50))
zone1.add_sprinkler(Sprinkler("42sa_4.0"))
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=34))
zone1.add_sprinkler(Sprinkler("42sa_4.0"))
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=32))
zone1.add_sprinkler(Sprinkler("42sa_4.0"))
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=20))
zone1.add_sprinkler(Sprinkler("42sa_5.0"))
zone1.add_pipe(Pipe(diameter_in_inches=0.95, length_in_feet=32))
zone1.add_sprinkler(Sprinkler("42sa_5.0"))

# inlet_pressure, inlet_flow = zone1.calculate_pressure_and_input_flow(ending_pressure=40)

# print(f"Zone: {zone1.name}")
# print(f"Required inlet pressure: {inlet_pressure:.2f} psi")
# print(f"Required inlet flow: {inlet_flow:.2f} gpm")

pressures = [p for p in range(25, 66, 1)]
results = [zone1.calculate_pressure_and_input_flow(ending_pressure=p) for p in pressures]
inlet_pressures, inlet_flows = zip(*results)
for p, f in zip(inlet_pressures, inlet_flows):
    print(f"Ending Pressure: {p} psi -> Inlet Flow: {f:.2f} gpm")


pump = WellPump(depth=72)
pumpFlows = [pump.get_flow_at_pressure(p) for p in inlet_pressures]

import matplotlib.pyplot as plt
plt.plot(inlet_flows, inlet_pressures, marker='o', label='Zone Curve')
plt.title(f"Zone: {zone1.name} - Inlet Flow vs Ending Pressure")
plt.xticks(range(int(min(inlet_flows)), int(max(inlet_flows)) + 1, 1))
plt.yticks(range(int(min(inlet_pressures)), int(max(inlet_pressures)) + 1, 1))
plt.grid(True)
plt.plot(pumpFlows, inlet_pressures, marker='x', label='Pump Curve')
plt.legend()
plt.xlabel("Inlet Flow (gpm)")
plt.ylabel("Ending Pressure (psi)")
plt.show()