# Akin Network License
# Author: Margareta Sandor
#         margareta.sandor@akin.network

# Project: FigSass Conversion Smart Contract


# Objective 1: Read the Figma JSON file using a python data object

import os
import json

# Define the path to the JSON file
json_file_path = os.path.abspath("fig/Primitives_ Akin Colours_LV.json")

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Print the content of the JSON file to verify
print(data)

# Now 'data' is a Python dictionary containing the JSON data