import os
from skimage.color import label2rgb
from skimage import io 
from skimage.measure import regionprops
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the folder containing the images
folder_path = '{path to folder containing masks goes here}'

# Define the minimum initial area to track only dividing cells
min_initial_area = 900

# Create an empty dataframe to store the object information
object_df = pd.DataFrame(columns=['object_id', 'frame', 'area', 'centroid_x', 'centroid_y', 'label', 'initial_area', 'area_diff','image'])


# Initialize a variable to store the new object ID
new_object = 1

# Get a sorted list of files in the folder
# Filter the list to include only files with the '.png' extension
files = os.listdir(folder_path)
png_files = [file for file in files if file.endswith(".png")]
sorted_files = sorted(png_files, key=lambda x: int(x.split('.')[0][-4:]))

# Define the range around the centroid (for tracking)
min_range = 30

#make a color dictionary so we can follow the objects if we want
colors = {}

# Iterate over the unique object_id's and assign a unique color to each
for object_id in object_df['object_id'].unique():
    colors[object_id] = np.random.randint(0, 256, 3)
# Iterate over the images in the folder
for file in sorted_files:
    if file.endswith('.png'):
        # Read the image
        image = io.imread(os.path.join(folder_path, file))
        # Get the properties of the objects in the image
        obj_props = regionprops(image, cache=True)
        # Get the frame number from the file name
        frame = int(file.split('.')[0])
        # Iterate over the objects in the image
        matched_objects = set()
        temp_df = pd.DataFrame(columns=['object_id', 'frame', 'area', 'centroid_x', 'centroid_y', 'label', 'initial_area', 'area_diff', 'image'])

        for obj_prop in obj_props:
            label = obj_prop.label
            area = obj_prop.area
            centroid = obj_prop.centroid
            centroid_x = centroid[0]
            centroid_y = centroid[1]
            object_id = obj_prop.label
        
            # Check if this is the first frame
            if frame == 1:
                # Check if the object has an area less than the specified minimum
                if area < min_initial_area:
                    # Add the object's information to the dataframe
                    new_row = pd.DataFrame({'object_id': [new_object], 'frame': [frame], 'area': [area], 'centroid_x': [centroid_x], 'centroid_y': [centroid_y], 'label': [label], 'initial_area': [area], 'area_diff': [0], 'image': [frame]})
                    object_df = pd.concat([object_df, new_row], ignore_index=True)
                    # Assign a color
                    colors[new_object] = np.random.randint(0, 256, 3)
                    new_object += 1
            else:
                # Check if the object has been seen in a previous frame
                match = object_df[(object_df['centroid_x'].between(centroid_x - min_range, centroid_x + min_range)) & 
                                  (object_df['centroid_y'].between(centroid_y - min_range, centroid_y + min_range))]
                if match.empty:
                    # This is a new object, skip it and move on
                    continue
                else:
                    match = match.copy()
                    # Calculate centroid distances for each match
                    match.loc[:, 'centroid_distance'] = np.sqrt((match['centroid_x'] - centroid_x)**2 + (match['centroid_y'] - centroid_y)**2)
        
                    # Find the match with the closest centroid
                    closest_match = match.loc[match['centroid_distance'].idxmin()]
        
                    if closest_match['object_id'] not in matched_objects:
                        # Update the object's information in a temporary DataFrame
                        initial_area = closest_match['initial_area']
                        delta_area = area - initial_area
                        new_row = pd.DataFrame({'object_id': [closest_match['object_id']], 'frame': [frame], 'area': [area], 'centroid_x': [centroid_x], 'centroid_y': [centroid_y], 'label': [closest_match['label']], 'initial_area': [initial_area], 'area_diff': [delta_area], 'image': [frame]})
                        temp_df = pd.concat([temp_df, new_row], ignore_index=True)
                        matched_objects.add(closest_match['object_id'])  # Mark the object as matched

        # Update the main object_df DataFrame with the information from the temp_df DataFrame
        object_df = pd.concat([object_df, temp_df], ignore_index=True)
# Calculate relative fold change
object_df['fold_change'] = np.log2(object_df['area'].astype(float) / object_df['initial_area'].astype(float))
# Write out dataframe to a csv file
object_df.to_csv('{path to output path for csv data file goes here}')         