# Akin Network License
# Author: Margareta Sandor
#         margareta.sandor@akin.network

# Project: FigSass Conversion Smart Contract
# Task: Create a script that generates a scss file with dummy data - sass classes

#!/usr/bin/env python

import random

# Function to generate dummy data
def generate_dummy_data():
    dummy_data = []
    for _ in range(10):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Random hex color
        width = random.randint(1, 5) * 100  # Random width
        height = random.randint(1, 5) * 100  # Random height
        dummy_data.append((color, width, height))
    return dummy_data

# Function to export data to .scss file
def export_to_scss(data, filename):
    with open(filename, 'w') as file:
        file.write("// Dummy data\n\n")
        for color, width, height in data:
            file.write(f".box-{color[1:]} {{\n")
            file.write(f"    background-color: {color};\n")
            file.write(f"    width: {width}px;\n")
            file.write(f"    height: {height}px;\n")
            file.write("}\n\n")
    print(f"Data exported to {filename}")

# Main function
def main():
    dummy_data = generate_dummy_data()
    export_to_scss(dummy_data, "dummy_styles.scss")

if __name__ == "__main__":
    main()