from ZoneStart import ZoneStart
from Pipe import Pipe
from Sprinkler import Sprinkler
from WellPump import WellPump
import matplotlib.pyplot as plt
from CycleStopValve import CycleStopValve
from MathFunctions import line_intersection


zone1 = ZoneStart(zone_id=1, location=(-46.65, 110), runtime_minutes=30)
zone2 = ZoneStart(zone_id=2, location=(-46.65, 110), runtime_minutes=30)

# Zone2 sprinklers from zoneInfo.csv
sprinkler2A = Sprinkler(name="sprinkler-2A", model="42sa_3.0", location=(-23.77, 60.59), left_edge_deg=56.1, theta_deg=150.3, max_radius=24.92)
sprinkler2B = Sprinkler(name="sprinkler-2B", model="42sa_4.0", location=(-3.08, 20.83), left_edge_deg=-90, theta_deg=180, max_radius=26)
sprinkler2C = Sprinkler(name="sprinkler-2C", model="42sa_4.0", location=(7.78, -3.63), left_edge_deg=-64.4, theta_deg=127.4, max_radius=30)
sprinkler2D = Sprinkler(name="sprinkler-2D", model="42sa_3.0", location=(22.93, -34.04), left_edge_deg=-85.9, theta_deg=150.2, max_radius=18)
sprinkler2E = Sprinkler(name="sprinkler-2E", model="42sa_3.0", location=(24.18, -54.83), left_edge_deg=-90, theta_deg=171.1, max_radius=23)
sprinkler2F = Sprinkler(name="sprinkler-2F", model="42sa_2.0", location=(-2.06, -58.54), left_edge_deg=-35.6, theta_deg=84.6, max_radius=27)

# Zone2 pipes in chain
pipe2A = Pipe(name="pipe-2A", start=zone2.location, end=sprinkler2A.location, diameter_in_inches=0.95)
pipe2B = Pipe(name="pipe-2B", start=sprinkler2A.location, end=sprinkler2B.location, diameter_in_inches=0.95)
pipe2C = Pipe(name="pipe-2C", start=sprinkler2B.location, end=sprinkler2C.location, diameter_in_inches=0.95)
pipe2D = Pipe(name="pipe-2D", start=sprinkler2C.location, end=sprinkler2D.location, diameter_in_inches=0.95)
pipe2E = Pipe(name="pipe-2E", start=sprinkler2D.location, end=sprinkler2E.location, diameter_in_inches=0.95)
pipe2F = Pipe(name="pipe-2F", start=sprinkler2E.location, end=sprinkler2F.location, diameter_in_inches=0.95)

# Connect zone2 outputs
zone2.add_output(pipe2A)
pipe2A.add_output(sprinkler2A)
pipe2A.add_output(pipe2B)
pipe2B.add_output(sprinkler2B)
pipe2B.add_output(pipe2C)
pipe2C.add_output(sprinkler2C)
pipe2C.add_output(pipe2D)
pipe2D.add_output(sprinkler2D)
pipe2D.add_output(pipe2E)
pipe2E.add_output(sprinkler2E)
pipe2E.add_output(pipe2F)
pipe2F.add_output(sprinkler2F)

# Top-level branch: pipe-1E
pipe1E = Pipe(name="pipe-1E", start=zone1.location, end=(-45.1, 38.42), diameter_in_inches=0.95)
sprinkler1E = Sprinkler(name="sprinkler-1E", model="42sa_2.0", location=(-45.1, 38.42), left_edge_deg=95.6, theta_deg=90, max_radius=33)

# pipe-1D branch off pipe-1E
pipe1D = Pipe(name="pipe-1D", start=pipe1E.end, end=(-44.18, 29.22), diameter_in_inches=0.95)
sprinkler1D = Sprinkler(name="sprinkler-1D", model="42sa_2.0", location=(-44.18, 29.22), left_edge_deg=2.7, theta_deg=87.1, max_radius=33)

# pipe-C branch off pipe-1D
pipeC = Pipe(name="pipe-C", start=pipe1D.end, end=(-39.95, -13.82), diameter_in_inches=0.95)
sprinkler1C = Sprinkler(name="sprinkler-1C", model="42sa_5.0", location=(-39.95, -13.82), left_edge_deg=95.6, theta_deg=180, max_radius=33)

# pipe-F branch off pipe-C
pipeF = Pipe(name="pipe-F", start=pipeC.end, end=(-11.29, -24.02), diameter_in_inches=0.95)
sprinkler1F = Sprinkler(name="sprinkler-1F", model="42sa_5.0", location=(-11.29, -24.02), left_edge_deg=95.5, theta_deg=180, max_radius=33)

# pipe-B branch off pipe-C
pipeB = Pipe(name="pipe-B", start=pipeC.end, end=(-36, -54.9), diameter_in_inches=0.95)
sprinkler1B = Sprinkler(name="sprinkler-1B", model="42sa_5.0", location=(-36, -54.9), left_edge_deg=95.5, theta_deg=180, max_radius=33)


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


# Attach top-level pipe to the zone
zone1.add_output(pipe1E)




# Generate inlet pressure vs inlet flow data for this zone
inlet_pressures = [p for p in range(40, 80, 1)]
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

# Find operating point with Cycle Stop Valve
csv = CycleStopValve(set_point_psi=68)
csv_flows = [f for f in range(15, 25, 1)]
csv_pressures = [csv.getOutletPressure(f) for f in csv_flows]
csv_minBackPressures = [csv.getMinimumInletPressure(f) for f in csv_flows]
result = line_intersection(inlet_pressures, inlet_flows, csv_pressures, csv_flows)
if result is None:
    raise ValueError("Operating point not found. No intersection found between zone demand curve and CSV outlet pressure curve. Increase csv_flows being graphed")
operatingPressure, operatingFlow = result
minimum_backPressure = csv.getMinimumInletPressure(operatingFlow)

print(f"Operating Point at Pressure: {operatingPressure:.2f} PSI, Flow: {operatingFlow:.2f} GPM, Minimum Backpressure: {minimum_backPressure:.2f} PSI")


# Set initial operating pressure at the zone
zone1.setOperatingPressure(operatingPressure)  
zone1_flow, _ = zone1.getOperatingFlow()
# Print zone operating flow and pressure
print(f"Zone 1 Operating Flow: {zone1_flow:.2f} GPM")
print(f"Zone 1 Operating Pressure: {operatingPressure:.2f} PSI")  

# Print operating flow and pressure for each sprinkler
for sprinkler in [sprinkler1B, sprinkler1C, sprinkler1D, sprinkler1E, sprinkler1F]:
    print(f"{sprinkler.name} at {sprinkler.location}:")
    print(f"  Operating Flow: {sprinkler.getOperatingFlow()[0]:.2f} GPM")
    print(f"  Operating Pressure: {sprinkler.getOperatingPressure()[0]:.2f} PSI")
    set_radius = sprinkler.max_radius
    operating_radius = sprinkler.getMaxOperatingRadius()[0]
    print(f"  Set Radius: {set_radius:.2f} ft")
    print(f"  Max Radius at Operating Pressure: {operating_radius:.2f} ft")
    if set_radius > operating_radius:
        print(f"  WARNING: Set radius ({set_radius:.2f} ft) is larger than max radius at operating pressure ({operating_radius:.2f} ft)")

# # Print operating flow and pressure for each pipe
# for pipe in [pipe1E, pipe1D, pipeC, pipeF, pipeB]:
#     print(f"{pipe.name} from {pipe.start} to {pipe.end}:")
#     print(f"  Operating Flow: {pipe.getOperatingFlow()[0]:.2f} GPM")
#     print(f"  Operating Pressure: {pipe.getOperatingPressure()[0]:.2f} PSI")


# For zone2
inlet_pressures2 = [p for p in range(40, 80, 1)]
inlet_flows2 = []
valid_operating_points2 = []
for p in inlet_pressures2:
    valid = zone2.setOperatingPressure(p)
    valid_operating_points2.append(valid)
    inlet_flows2.append(zone2.getOperatingFlow()[0])

# Separate valid and invalid points for zone2
valid_flows2 = [f for f, v in zip(inlet_flows2, valid_operating_points2) if v]
valid_pressures2 = [p for p, v in zip(inlet_pressures2, valid_operating_points2) if v]
invalid_flows2 = [f for f, v in zip(inlet_flows2, valid_operating_points2) if not v]
invalid_pressures2 = [p for p, v in zip(inlet_pressures2, valid_operating_points2) if not v]

# Find operating point with Cycle Stop Valve for zone2
result2 = line_intersection(inlet_pressures2, inlet_flows2, csv_pressures, csv_flows)
if result2 is None:
    raise ValueError("Operating point not found for zone2. No intersection found between zone demand curve and CSV outlet pressure curve.")
operatingPressure2, operatingFlow2 = result2
minimum_backPressure2 = csv.getMinimumInletPressure(operatingFlow2)

print(f"Zone2 Operating Point at Pressure: {operatingPressure2:.2f} PSI, Flow: {operatingFlow2:.2f} GPM, Minimum Backpressure: {minimum_backPressure2:.2f} PSI")

# Set initial operating pressure at zone2
zone2.setOperatingPressure(operatingPressure2)  
zone2_flow, _ = zone2.getOperatingFlow()
# Print zone operating flow and pressure
print(f"Zone 2 Operating Flow: {zone2_flow:.2f} GPM")
print(f"Zone 2 Operating Pressure: {operatingPressure2:.2f} PSI")  

# Print operating flow and pressure for each sprinkler in zone2
for sprinkler in [sprinkler2A, sprinkler2B, sprinkler2C, sprinkler2D, sprinkler2E, sprinkler2F]:
    print(f"{sprinkler.name} at {sprinkler.location}:")
    print(f"  Operating Flow: {sprinkler.getOperatingFlow()[0]:.2f} GPM")
    print(f"  Operating Pressure: {sprinkler.getOperatingPressure()[0]:.2f} PSI")
    set_radius = sprinkler.max_radius
    operating_radius = sprinkler.getMaxOperatingRadius()[0]
    print(f"  Set Radius: {set_radius:.2f} ft")
    print(f"  Max Radius at Operating Pressure: {operating_radius:.2f} ft")
    if set_radius > operating_radius:
        print(f"  WARNING: Set radius ({set_radius:.2f} ft) is larger than max radius at operating pressure ({operating_radius:.2f} ft)")


# # Print operating flow and pressure for each pipe in zone2
# for pipe in [pipe2A, pipe2B, pipe2C, pipe2D, pipe2E, pipe2F]:
#     print(f"{pipe.name} from {pipe.start} to {pipe.end}:")
#     print(f"  Operating Flow: {pipe.getOperatingFlow()[0]:.2f} GPM")
#     print(f"  Operating Pressure: {pipe.getOperatingPressure()[0]:.2f} PSI")


pump = WellPump(depth=72)
pumpPressures = [p for p in range(50, 100, 1)]
pumpFlows = [pump.get_flow_at_pressure(p) for p in pumpPressures]
result = line_intersection(csv_minBackPressures, csv_flows, pumpPressures, pumpFlows)
if result is None:
    raise ValueError("Maximum valid zone flow at CSV Set Point not found. No intersection found between pump curve and CSV minimum inlet pressure curve. Increase csv_flows being graphed")
_, maximum_valid_zone_flow = result
print(f"Maximum valid zone flow at CSV Set Point: {maximum_valid_zone_flow:.2f} GPM")

pumpBackpressure = pump.get_pressure_at_flow(zone1_flow)
print(f"Pump backpressure at zone flow ({zone1_flow:.2f} GPM): {pumpBackpressure:.2f} PSI")
backPressureTooLow = False
if pumpBackpressure < minimum_backPressure:
    backPressureTooLow = True
    print(f"Warning: Pump backpressure ({pumpBackpressure:.2f} PSI) is less than minimum required by CSV ({minimum_backPressure:.2f} PSI).")

demandTooHigh = False
if zone1_flow > maximum_valid_zone_flow:
    demandTooHigh = True
    print(f"Pump cannot deliver required flow at operating pressure. Pump capability: {maximum_valid_zone_flow:.2f} GPM, Required flow: {zone1_flow:.2f} GPM")




#check the maximum differential pressure across the CSV
CSV_pressure_at_1gpm = csv.getOutletPressure(1)
backPressure_at_1gpm = pump.get_pressure_at_flow(1)
differentialPressure_CSV = backPressure_at_1gpm - CSV_pressure_at_1gpm
headPressure_at_1gpm = pump.get_head_pressure_at_flow(1)
print(f"Maximum Backpressure (at 1 GPM): {backPressure_at_1gpm:.2f} PSI")
print(f"Maximum Pump Head Pressure (at 1 GPM): {headPressure_at_1gpm:.2f} PSI")
print(f"Maximum differential pressure across CSV (at 1 GPM): {differentialPressure_CSV:.2f} PSI")




# Plot valid points with filled circles, invalid with empty circles

plt.plot(valid_pressures, valid_flows, marker='o', label='Zone Demand (Valid)', linestyle='None', markerfacecolor='C0')
if invalid_flows:  # Only plot if there are invalid points
    plt.plot(invalid_pressures, invalid_flows, marker='o', label='Zone Demand (Invalid)', linestyle='None', markerfacecolor='white', markeredgecolor='C0', markeredgewidth=1.5)
plt.title(f"Zone: {zone1.zone_id} -  Operating Pressure vs Zone Inlet Flow")
plt.xticks(range(int(min(min(inlet_pressures), min(pumpPressures))), int(max(max(inlet_pressures), max(pumpPressures))) + 1, 1))
plt.yticks(range(int(min(min(inlet_flows), min(pumpFlows))), int(max(max(inlet_flows), max(pumpFlows))) + 1, 1))
plt.grid(True)
plt.plot(pumpPressures, pumpFlows, marker='x', label='Pump Production')
plt.axvline(x=operatingPressure, color='red', linestyle='--', linewidth=2, label=f'Operating Pressure ({operatingPressure} psi)')
plt.axvline(x=pumpBackpressure, color='green', linestyle='--', linewidth=2, label=f'Pump Backpressure ({pumpBackpressure:.2f} psi){"  INSUFFICIENT BACKPRESSURE" if backPressureTooLow else ""}')
plt.axhline(y=zone1_flow, color='orange', linestyle='--', linewidth=2, label=f'Zone Flow ({zone1_flow:.2f} gpm){"  DEMAND TOO HIGH" if demandTooHigh else ""}')
plt.axhline(y=maximum_valid_zone_flow, color='purple', linestyle='--', linewidth=2, label=f'Max Valid Zone Flow at CSV Set Point ({maximum_valid_zone_flow:.2f} gpm)')

plt.plot(csv_pressures, csv_flows, marker='s', color='purple', label='CSV Outlet Pressure (Reduced Pressure Falloff)')
plt.plot(csv_minBackPressures, csv_flows, marker='^', color='purple', label='CSV Min Inlet Pressure (Friction Loss)')
plt.fill_betweenx(csv_flows, csv_minBackPressures, csv_pressures, color='purple', alpha=0.2, label='CSV Pressure Loss Region')
plt.legend()
plt.xlabel("Pressure (psi)")
plt.ylabel("Flow (gpm)")

plt.show(block=False)

# Plot for zone2
plt.figure()
plt.plot(valid_pressures2, valid_flows2, marker='o', label='Zone Demand (Valid)', linestyle='None', markerfacecolor='C0')
if invalid_flows2:  # Only plot if there are invalid points
    plt.plot(invalid_pressures2, invalid_flows2, marker='o', label='Zone Demand (Invalid)', linestyle='None', markerfacecolor='white', markeredgecolor='C0', markeredgewidth=1.5)
plt.title(f"Zone: {zone2.zone_id} -  Operating Pressure vs Zone Inlet Flow")
plt.xticks(range(int(min(min(inlet_pressures2), min(pumpPressures))), int(max(max(inlet_pressures2), max(pumpPressures))) + 1, 1))
plt.yticks(range(int(min(min(inlet_flows2), min(pumpFlows))), int(max(max(inlet_flows2), max(pumpFlows))) + 1, 1))
plt.grid(True)
plt.plot(pumpPressures, pumpFlows, marker='x', label='Pump Production')
plt.axvline(x=operatingPressure2, color='red', linestyle='--', linewidth=2, label=f'Operating Pressure ({operatingPressure2} psi)')
pumpBackpressure2 = pump.get_pressure_at_flow(zone2_flow)
plt.axvline(x=pumpBackpressure2, color='green', linestyle='--', linewidth=2, label=f'Pump Backpressure ({pumpBackpressure2:.2f} psi)')
plt.axhline(y=zone2_flow, color='orange', linestyle='--', linewidth=2, label=f'Zone Flow ({zone2_flow:.2f} gpm)')
plt.axhline(y=maximum_valid_zone_flow, color='purple', linestyle='--', linewidth=2, label=f'Max Valid Zone Flow at CSV Set Point ({maximum_valid_zone_flow:.2f} gpm)')

plt.plot(csv_pressures, csv_flows, marker='s', color='purple', label='CSV Outlet Pressure (Reduced Pressure Falloff)')
plt.plot(csv_minBackPressures, csv_flows, marker='^', color='purple', label='CSV Min Inlet Pressure (Friction Loss)')
plt.fill_betweenx(csv_flows, csv_minBackPressures, csv_pressures, color='purple', alpha=0.2, label='CSV Pressure Loss Region')
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

# # Zone 1 sprinklers
# for sprinkler in [sprinkler1B, sprinkler1C, sprinkler1D, sprinkler1E, sprinkler1F]:
#     #TODO make the color of the sprinkler sector red if its operating point is invalid
#     add_partial_cylinder_to_surface(
#         x, y, z,
#         center=sprinkler.location,
#         leftEdge_deg=sprinkler.left_edge_deg,
#         theta_deg=sprinkler.theta_deg,
#         radius=sprinkler.getOperatingRadius()[0],
#         height=sprinkler.getHeight(zone1.runtime_minutes)[0] # Use operating flow as height
#     )

# Zone 2 sprinklers
for sprinkler in [sprinkler2A, sprinkler2B, sprinkler2C, sprinkler2D, sprinkler2E, sprinkler2F]:
    #TODO make the color of the sprinkler sector red if its operating point is invalid
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