import plotly.graph_objects as go
import numpy as np
import json

class Sprinkler:
    def __init__(self, origin, left_edge_deg, theta_deg, radius, gpm, minutes=0):
        self.origin = origin
        self.left_edge_deg = left_edge_deg
        self.theta_deg = theta_deg
        self.radius = radius
        self.gpm = gpm
        self.minutes = minutes
        self.height = self.calculate_height()  # Calculate height based on water spread

    def __repr__(self):
        return (f"Sprinkler(origin={self.origin}, left_edge_deg={self.left_edge_deg}, "
                f"theta_deg={self.theta_deg}, radius={self.radius}, gpm={self.gpm}, minutes={self.minutes})")

    def calculate_height(self):
        """
        Calculate the height representing the amount of water spread across the sector.
        The height is proportional to the total water (cubic inches) divided by the sector area.
        """
        # Convert theta from degrees to radians
        theta_rad = np.deg2rad(abs(self.theta_deg))
        # Area of the sector (slice of a circle)
        sector_area_sqft = 0.5 * (self.radius ** 2) * theta_rad
        sector_area_sqinches = sector_area_sqft * 144  # Convert square feet to square inches
        # Total water applied (gallons)
        total_gallons = self.gpm * self.minutes
        # Convert gallons to cubic inches (1 gallon = 231 cubic inches)
        total_cubic_inches = total_gallons * 231
        # Height = total water (cubic inches) / area (if area > 0)
        if sector_area_sqinches > 0:
            return total_cubic_inches / sector_area_sqinches
        else:
            return 0

def load_sprinklers_from_zones_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    sprinklers = []
    for zone_name, zone_info in data.items():
        runtime = zone_info.get('time', 0)
        for s in zone_info['sprinklers']:
            sprinkler = Sprinkler(
                origin=tuple(s['origin']),
                left_edge_deg=s['left_edge_deg'],
                theta_deg=s['theta_deg'],
                radius=s['radius'],
                gpm=s['gpm'],
                minutes=runtime
            )
            sprinklers.append(sprinkler)
    return sprinklers

# Function to add a partial cylinder (sector) to the surface
def add_partial_cylinder_to_surface(x, y, z, center, leftEdge_deg, theta_deg, radius, height):
    x_center, y_center = center
    # Calculate the distance and angle of each point from the center
    dx = x - x_center
    dy = y - y_center
    distance = np.sqrt(dx**2 + dy**2)
    # Angle from east (x-axis), counterclockwise, in degrees
    angles = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
    # Calculate end angle
    end_deg = (leftEdge_deg - theta_deg) % 360
    # Determine mask for sector
    if theta_deg < 0:
        if leftEdge_deg < end_deg:
            mask = (distance <= radius) & (angles >= leftEdge_deg) & (angles <= end_deg)
        else:
            mask = (distance <= radius) & ((angles >= leftEdge_deg) | (angles <= end_deg))
    else:
        if leftEdge_deg > end_deg:
            mask = (distance <= radius) & (angles <= leftEdge_deg) & (angles >= end_deg)
        else:
            mask = (distance <= radius) & ((angles <= leftEdge_deg) | (angles >= end_deg))
    z[mask] += height


# Create a grid of x and y coordinates
x = np.linspace(0, 100, 1001)
y = np.linspace(0, 100, 1001)
x, y = np.meshgrid(x, y)
z = np.zeros_like(x)

sprinklers = load_sprinklers_from_zones_json('zones.json')

# Add each sprinkler's effect to the surface
for sprinkler in sprinklers:
    # Calculate the center of the sprinkler's sector
    center = sprinkler.origin
    # Add the height of the sprinkler to the surface
    add_partial_cylinder_to_surface(
        x, y, z,
        center=center,
        leftEdge_deg=sprinkler.left_edge_deg,
        theta_deg=sprinkler.theta_deg,
        radius=sprinkler.radius,
        height=sprinkler.height
    )   

## Function to add a cylindrical height to the surface
#def add_cylinder_to_surface(x, y, z, center, radius, height):
#    x_center, y_center = center
#    # Calculate the distance of each point from the cylinder's center
#    distance = np.sqrt((x - x_center)**2 + (y - y_center)**2)
#    # Add height where the distance is within the cylinder's radius
#    z[distance <= radius] += height
#
#
#
#
## Example usage: Add a cylinder to the surface
#add_cylinder_to_surface(x, y, z, center=(0.5, 0.5), radius=0.2, height=0.4)
#add_cylinder_to_surface(x, y, z, center=(0.3, 0.7), radius=0.1, height=0.2)     
#add_partial_cylinder_to_surface(x, y, z, center=(0.0, 0.5), leftEdge_deg=90, theta_deg=110, radius=0.15, height=0.3)   



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


