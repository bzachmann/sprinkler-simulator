from ZoneStart import ZoneStart
from Pipe import Pipe
from Sprinkler import Sprinkler
from WellPump import WellPump
import matplotlib.pyplot as plt


zone1 = ZoneStart(zone_id=1, location=(-46.65, 110), runtime_minutes=30)

# Top-level branch: pipe-1E
pipe1E = Pipe(name="pipe-1E", start=zone1.location, end=(-45.1, 38.42), diameter_in_inches=0.95)
sprinkler1E = Sprinkler(name="sprinkler-1E", model="42sa_3.0", location=(-45.1, 38.42), left_edge_deg=95.6, theta_deg=90, max_radius=33)

# pipe-1D branch off pipe-1E
pipe1D = Pipe(name="pipe-1D", start=pipe1E.end, end=(-44.18, 29.22), diameter_in_inches=0.95)
sprinkler1D = Sprinkler(name="sprinkler-1D", model="42sa_3.0", location=(-44.18, 29.22), left_edge_deg=2.7, theta_deg=87.1, max_radius=33)

# pipe-C branch off pipe-1D
pipeC = Pipe(name="pipe-C", start=pipe1D.end, end=(-39.95, -13.82), diameter_in_inches=0.95)
sprinkler1C = Sprinkler(name="sprinkler-1C", model="42sa_3.0", location=(-39.95, -13.82), left_edge_deg=95.6, theta_deg=180, max_radius=33)

# pipe-F branch off pipe-C
pipeF = Pipe(name="pipe-F", start=pipeC.end, end=(-11.29, -24.02), diameter_in_inches=0.95)
sprinkler1F = Sprinkler(name="sprinkler-1F", model="42sa_3.0", location=(-11.29, -24.02), left_edge_deg=95.5, theta_deg=180, max_radius=33)

# pipe-B branch off pipe-C
pipeB = Pipe(name="pipe-B", start=pipeC.end, end=(-36, -54.9), diameter_in_inches=0.95)
sprinkler1B = Sprinkler(name="sprinkler-1B", model="42sa_3.0", location=(-36, -54.9), left_edge_deg=95.5, theta_deg=180, max_radius=33)

# pipe-A branch off pipe-B
pipeA = Pipe(name="pipe-A", start=pipeB.end, end=(-2, -58.6), diameter_in_inches=0.95)
sprinkler1A = Sprinkler(name="sprinkler-1A", model="42sa_3.0", location=(-2, -58.6), left_edge_deg=68, theta_deg=330, max_radius=29)

# Connect outputs per zones_new2.json structure
pipe1E.add_output(sprinkler1E)
pipe1E.add_output(pipe1D)

pipe1D.add_output(sprinkler1D)
pipe1D.add_output(pipeC)

pipeC.add_output(sprinkler1C)
pipeC.add_output(pipeF)
pipeC.add_output(pipeB)

pipeF.add_output(sprinkler1F)

pipeB.add_output(sprinkler1B)
pipeB.add_output(pipeA)

pipeA.add_output(sprinkler1A)

# Attach top-level pipe to the zone
zone1.add_output(pipe1E)




# Solve the hydraulic network
operatingPressure = 68  # Example initial pressure at the zone start
zone1.setOperatingPressure(operatingPressure)  # Set initial operating pressure at the zone
zone1_flow, _ = zone1.getOperatingFlow()
# Print zone operating flow and pressure
print(f"Zone 1 Operating Flow: {zone1_flow:.2f} GPM")
print(f"Zone 1 Operating Pressure: {operatingPressure:.2f} PSI")  

# Print operating flow and pressure for each sprinkler
for sprinkler in [sprinkler1A, sprinkler1B, sprinkler1C, sprinkler1D, sprinkler1E, sprinkler1F]:
    print(f"{sprinkler.name} at {sprinkler.location}:")
    print(f"  Operating Flow: {sprinkler.getOperatingFlow()[0]:.2f} GPM")
    print(f"  Operating Pressure: {sprinkler.getOperatingPressure()[0]:.2f} PSI")

# Print operating flow and pressure for each pipe
for pipe in [pipe1E, pipe1D, pipeC, pipeF, pipeB, pipeA]:
    print(f"{pipe.name} from {pipe.start} to {pipe.end}:")
    print(f"  Operating Flow: {pipe.getOperatingFlow()[0]:.2f} GPM")
    print(f"  Operating Pressure: {pipe.getOperatingPressure()[0]:.2f} PSI")

pump = WellPump(depth=72)
inlet_pressures = [p for p in range(50, 80, 1)]
pumpFlows = [pump.get_flow_at_pressure(p) for p in inlet_pressures]
inlet_flows = []
valid_operating_points = []

for p in inlet_pressures:
    valid = zone1.setOperatingPressure(p)
    valid_operating_points.append(valid)
    inlet_flows.append(zone1.getOperatingFlow()[0])

# Separate valid and invalid points
valid_flows = [f for f, v in zip(inlet_flows, valid_operating_points) if v]
valid_pressures = [p for p, v in zip(inlet_pressures, valid_operating_points) if v]
invalid_flows = [f for f, v in zip(inlet_flows, valid_operating_points) if not v]
invalid_pressures = [p for p, v in zip(inlet_pressures, valid_operating_points) if not v]

pumpBackpressure = pump.get_pressure_at_flow(zone1_flow)
print(f"Pump backpressure at zone flow ({zone1_flow:.2f} GPM): {pumpBackpressure:.2f} PSI")
pumpFlowCapabilityAtOperatingPressure = pump.get_flow_at_pressure(operatingPressure)
demandTooHigh = False
if pumpFlowCapabilityAtOperatingPressure < zone1_flow:
    demandTooHigh = True
    print(f"Pump cannot deliver required flow at operating pressure. Pump capability: {pumpFlowCapabilityAtOperatingPressure:.2f} GPM, Required flow: {zone1_flow:.2f} GPM")

# Plot valid points with filled circles, invalid with empty circles
plt.plot(valid_pressures, valid_flows, marker='o', label='Zone Demand (Valid)', linestyle='None', markerfacecolor='C0')
if invalid_flows:  # Only plot if there are invalid points
    plt.plot(invalid_pressures, invalid_flows, marker='o', label='Zone Demand (Invalid)', linestyle='None', markerfacecolor='white', markeredgecolor='C0', markeredgewidth=1.5)
plt.title(f"Zone: {zone1.zone_id} -  Operating Pressure vs Zone Inlet Flow")
plt.xticks(range(int(min(inlet_pressures)), int(max(inlet_pressures)) + 1, 1))
plt.yticks(range(int(min(min(inlet_flows), min(pumpFlows))), int(max(max(inlet_flows), max(pumpFlows))) + 1, 1))
plt.grid(True)
plt.plot(inlet_pressures, pumpFlows, marker='x', label='Pump Production')
plt.axvline(x=operatingPressure, color='red', linestyle='--', linewidth=2, label=f'Operating Pressure ({operatingPressure} psi)')
plt.axvline(x=pumpBackpressure, color='green', linestyle='--', linewidth=2, label=f'Pump Backpressure ({pumpBackpressure:.2f} psi)')
plt.axhline(y=zone1_flow, color='orange', linestyle='--', linewidth=2, label=f'Zone Flow ({zone1_flow:.2f} gpm){"  DEMAND TOO HIGH" if demandTooHigh else ""}')
plt.legend()
plt.xlabel("Pressure (psi)")
plt.ylabel("Flow (gpm)")
plt.show()


from MathFunctions import add_partial_cylinder_to_surface
import numpy as np
import plotly.graph_objects as go

x = np.linspace(-72, 155, 1001)
y = np.linspace(-100, 150, 1001)
x, y = np.meshgrid(x, y)
z = np.zeros_like(x)

for sprinkler in [sprinkler1A, sprinkler1B, sprinkler1C, sprinkler1D, sprinkler1E, sprinkler1F]:

    #TODO make the color of the sprinkler sector red if its operating point is invalid
    if sprinkler.getOperatingFlow()[1]:
        add_partial_cylinder_to_surface(
            x, y, z,
            center=sprinkler.location,
            leftEdge_deg=sprinkler.left_edge_deg,
            theta_deg=sprinkler.theta_deg,
            radius=sprinkler.getOperatingRadius()[0],
            height=sprinkler.getHeight(zone1.runtime_minutes)[0] # Use operating flow as height
        )

# Create a surface plot with hard edges
fig = go.Figure(data=[go.Surface(
    z=z,
    x=x,
    y=y,
    colorscale='Viridis',
    showscale=True,
    contours=dict(
        z=dict(
            show=True,  # Show contour lines
            usecolormap=True,  # Use the colormap for contours
            highlightcolor="limegreen",  # Highlight color for edges
            project_z=True  # Project contours onto the z-axis
        )
    )
)])

# Set axis labels and layout
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
    ),
    title="Hard-Edged Surface with Plotly"
)

fig.show()