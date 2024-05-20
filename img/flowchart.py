import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Modify the existing code to include the additional data source rectangles and arrows

# Define a function to create a rounded rectangle
def draw_rounded_rect(ax, x, y, width, height, color, text, edge_color="black"):
    # Create a rounded box
    bbox = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1", ec=edge_color, fc=color, lw=2)
    ax.add_patch(bbox)
    # Add text in the center of the box
    ax.text(x + width / 2, y + height / 2, text, ha='center', va='center', fontsize=12, weight='bold', color='white')

# Setup the figure and axis
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors for different services
colors = {
    'Data Sources': 'skyblue',
    'ETL Process': 'seagreen',
    'Data Storage': 'salmon',
    'Analytics/Visualization': 'mediumpurple',
    'AWS Services': 'gold',
    'API': 'lightblue',
    'CSV': 'lightgreen'
}

# Draw the flowchart boxes
draw_rounded_rect(ax, 1, 9, 3, 1, colors['Data Sources'], 'Data Sources')

# Draw arrows from Data Sources
ax.annotate('', xy=(1.5, 9), xytext=(1.5, 8), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(2.5, 9), xytext=(2.5, 8), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(3.5, 9), xytext=(3.5, 8), arrowprops=dict(arrowstyle="->", lw=2))

# Draw rectangles for each API
draw_rounded_rect(ax, 0.5, 7, 2, 0.75, colors['API'], 'NASA Mars Weather\nService API (JSON)', edge_color='black')
draw_rounded_rect(ax, 2, 7, 2, 0.75, colors['API'], 'Open-Meteo Weather\nAPI (JSON)', edge_color='black')
draw_rounded_rect(ax, 3.5, 7, 2, 0.75, colors['CSV'], 'NASA Rover Environmental\nMonitoring Station (REMS)\non-board the Curiosity Rover (CSV)', edge_color='black')

# Continue with the original flowchart
draw_rounded_rect(ax, 1, 5, 3, 1, colors['ETL Process'], 'ETL Process')
draw_rounded_rect(ax, 1, 3, 3, 1, colors['Data Storage'], 'Data Storage')
draw_rounded_rect(ax, 1, 1, 3, 1, colors['Analytics/Visualization'], 'Analytics/Visualization')

# Draw the arrows for the rest of the pipeline
ax.annotate('', xy=(2.5, 5), xytext=(2.5, 6), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(2.5, 3), xytext=(2.5, 4), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(2.5, 1), xytext=(2.5, 2), arrowprops=dict(arrowstyle="->", lw=2))

# Draw AWS Services box
draw_rounded_rect(ax, 5, 4, 4, 3, colors['AWS Services'], 'AWS Services')

# Label AWS Services
services = ['S3', 'Lambda', 'Glue', 'Athena', 'Redshift', 'Lake Formation', 'Python Streamlit App']
for i, service in enumerate(services):
    ax.text(7, 6.8 - i*0.5, service, ha='center', va='center', fontsize=12, color='black')

plt.show()
