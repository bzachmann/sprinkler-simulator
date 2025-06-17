import plotly.graph_objects as go
import numpy as np

# Create a grid of x and y coordinates
x = np.linspace(0, 1, 101)  # Lower resolution for bar grid
y = np.linspace(0, 1, 101)
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

# Example usage: Add a cylinder to the surface
add_cylinder_to_surface(x, y, z, center=(0.5, 0.5), radius=0.2, height=0.4)
add_cylinder_to_surface(x, y, z, center=(0.3, 0.7), radius=0.1, height=0.2)     


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