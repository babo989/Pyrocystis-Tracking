import os
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

# Define the folder containing the masks
mask_folder = '{path to folder containing masks goes here}'

# Define the path to the CSV file containing the object information
object_info_path = '{path to file containing tracking information goes here}'

# Define the chosen label and frame number to display
chosen_label = {}
chosen_frame_number = {}

# Load the object information from the CSV file
object_info = pd.read_csv(object_info_path)

# Filter the object information for the chosen label
object_info = object_info[object_info['label'] == chosen_label]

# Get the file path for the mask corresponding to the chosen frame number
mask_file = f"{chosen_frame_number:04d}.png"
mask_path = os.path.join(mask_folder, mask_file)

# Load the mask and overlay it on the image
mask = io.imread(mask_path)
image_file = f"{chosen_frame_number:04d}.png"
image_path = os.path.join(mask_folder, image_file)
original_image = io.imread(image_path).copy()
masked_image = original_image.copy()

# Apply the mask based on the chosen label
masked_image[mask != chosen_label] = 0

# Define the path to save the masked image
output_path = '{path for saving overlayed image}'

# Display the masked image with the label
plt.imshow(masked_image)
plt.savefig(output_path)
plt.close()
