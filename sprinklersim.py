import plotly.graph_objects as go
import numpy as np

# Create a grid of x and y coordinates
x = np.linspace(0, 1, 1001)  # Lower resolution for bar grid
y = np.linspace(0, 1, 1001)
x, y = np.meshgrid(x, y)

# Initialize a height map (z values) with zeros
z = np.zeros_like(x)

# Function to add a cylindrical height to the surface
def add_cylinder_to_surface(x, y, z, center, radius, height):
    x_center, y_center = center
    # Calculate the distance of each point from the cylinder's center
    distance = np.sqrt((x - x_center)**2 + (y - y_center)**2)
    # Add height where the distance is within the cylinder's radius
    z[distance <= radius] += height

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


# Example usage: Add a cylinder to the surface
add_cylinder_to_surface(x, y, z, center=(0.5, 0.5), radius=0.2, height=0.4)
add_cylinder_to_surface(x, y, z, center=(0.3, 0.7), radius=0.1, height=0.2)     
add_partial_cylinder_to_surface(x, y, z, center=(0.0, 0.5), leftEdge_deg=90, theta_deg=110, radius=0.15, height=0.3)   


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