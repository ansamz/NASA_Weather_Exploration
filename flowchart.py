import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Define a function to create a rounded rectangle
def draw_rounded_rect(ax, x, y, width, height, color, text):
    # Create a rounded box
    bbox = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1", ec="black", fc=color, lw=2)
    ax.add_patch(bbox)
    # Add text in the center of the box
    ax.text(x + width / 2, y + height / 2, text, ha='center', va='center', fontsize=14, weight='bold', color='white')

# Setup the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors for different services
colors = {
    'Data Sources': 'skyblue',
    'ETL Process': 'seagreen',
    'Data Storage': 'salmon',
    'Analytics/Visualization': 'mediumpurple',
    'AWS Services': 'gold'
}

# Draw the flowchart boxes
draw_rounded_rect(ax, 1, 8, 3, 1, colors['Data Sources'], 'Data Sources')
draw_rounded_rect(ax, 1, 6, 3, 1, colors['ETL Process'], 'ETL Process')
draw_rounded_rect(ax, 1, 4, 3, 1, colors['Data Storage'], 'Data Storage')
draw_rounded_rect(ax, 1, 2, 3, 1, colors['Analytics/Visualization'], 'Analytics/Visualization')

# Draw the arrows
ax.annotate('', xy=(2.5, 6), xytext=(2.5, 7), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(2.5, 4), xytext=(2.5, 5), arrowprops=dict(arrowstyle="->", lw=2))
ax.annotate('', xy=(2.5, 2), xytext=(2.5, 3), arrowprops=dict(arrowstyle="->", lw=2))

# Draw AWS Services box
draw_rounded_rect(ax, 5, 5, 4, 2.5, colors['AWS Services'], 'AWS Services')

# Label AWS Services
services = ['S3', 'Lambda', 'Glue', 'Athena', 'Redshift', 'Lake Formation', 'Python Streamlit App']
for i, service in enumerate(services):
    ax.text(7, 7.2 - i*0.35, service, ha='center', va='center', fontsize=12, color='black')

plt.show()
