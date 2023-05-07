import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV file
df = pd.read_csv('{path to file containing tracking information goes here}')

# Define a list of objects to track and their associated colors
# Format for objects input is:(object number, color for line, color for marker)
# Multiple objects are separated by a comma
objects = []
output_path = "{path for output image goes here}"

# Plot the area values for each object
for obj, line_color, marker_color in objects:
    # Get the unique frames for this object and multiply them by 2
    frames = df.loc[df['object_id'] == obj, 'frame'].unique() * 2

    # Initialize an empty list to store the area values for each frame
    areas = []

    # Loop through each frame and extract the area values
    for frame in frames:
        area = df.loc[(df['object_id'] == obj) & (df['frame'] == frame/2), 'area'].mean()
        areas.append(area)

    # Plot the area values
    plt.plot(frames, areas, color=line_color)
    plt.scatter(frames, areas, color=marker_color, s=30)

# Set the plot labels and title
plt.xlabel('')
plt.ylabel('')
plt.title('', fontsize=16)

# Save and show the plot
plt.savefig(output_path, dpi=300)
plt.show()

