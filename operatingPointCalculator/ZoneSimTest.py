from ZoneStart import ZoneStart
from Pipe import Pipe
from Sprinkler import Sprinkler


zone1 = ZoneStart(zone_id=1, location=(-46.65, 110), runtime_minutes=30)

# Top-level branch: pipe-1E
pipe1E = Pipe(start=zone1.location, end=(-45.1, 38.42), diameter_in_inches=0.95)
sprinkler1E = Sprinkler(name="sprinkler-1E", model="42sa_3.0", location=(-45.1, 38.42), left_edge_deg=95.6, theta_deg=90, max_radius=33)

# pipe-1D branch off pipe-1E
pipe1D = Pipe(start=pipe1E.end, end=(-44.18, 29.22), diameter_in_inches=0.95)
sprinkler1D = Sprinkler(name="sprinkler-1D", model="42sa_3.0", location=(-44.18, 29.22), left_edge_deg=2.7, theta_deg=87.1, max_radius=33)

# pipe-C branch off pipe-1D
pipeC = Pipe(start=pipe1D.end, end=(-39.95, -13.82), diameter_in_inches=0.95)
sprinkler1C = Sprinkler(name="sprinkler-1C", model="42sa_3.0", location=(-39.95, -13.82), left_edge_deg=95.6, theta_deg=180, max_radius=33)

# pipe-F branch off pipe-C
pipeF = Pipe(start=pipeC.end, end=(-11.29, -24.02), diameter_in_inches=0.95)
sprinkler1F = Sprinkler(name="sprinkler-1F", model="42sa_3.0", location=(-11.29, -24.02), left_edge_deg=95.5, theta_deg=180, max_radius=33)

# pipe-B branch off pipe-C
pipeB = Pipe(start=pipeC.end, end=(-36, -54.9), diameter_in_inches=0.95)
sprinkler1B = Sprinkler(name="sprinkler-1B", model="42sa_3.0", location=(-36, -54.9), left_edge_deg=95.5, theta_deg=180, max_radius=33)

# pipe-A branch off pipe-B
pipeA = Pipe(start=pipeB.end, end=(-2, -58.6), diameter_in_inches=0.95)
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
zone1_flow = zone1.getOperatingFlow()
# Print zone operating flow and pressure
print(f"Zone 1 Operating Flow: {zone1_flow:.2f} GPM")
print(f"Zone 1 Operating Pressure: {operatingPressure:.2f} PSI")  

# Print operating flow and pressure for each sprinkler
for sprinkler in [sprinkler1A, sprinkler1B, sprinkler1C, sprinkler1D, sprinkler1E, sprinkler1F]:
    print(f"{sprinkler.name} at {sprinkler.location}:")
    print(f"  Operating Flow: {sprinkler.getOperatingFlow():.2f} GPM")
    print(f"  Operating Pressure: {sprinkler.getOperatingPressure():.2f} PSI")

# Print operating flow and pressure for each pipe
for pipe in [pipe1E, pipe1D, pipeC, pipeF, pipeB, pipeA]:
    print(f"Pipe from {pipe.start} to {pipe.end}:")
    print(f"  Operating Flow: {pipe.getOperatingFlow():.2f} GPM")
    print(f"  Operating Pressure: {pipe.getOperatingPressure():.2f} PSI")

# Optional: set operating pressure to compute flows (example)
# zone1.setOperatingPressure(68)
