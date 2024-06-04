# Akin Network License
# Author: Margareta Sandor
#         margareta.sandor@akin.network

# Project: FigSass Conversion Smart Contract
# Task: Create a script that generates a scss file with dummy data - sass variables (variation of the initial task)

#!/usr/bin/env python

import random
import os

# Function to generate dummy SASS variables
def generate_sass_variables(num_variables=10):
    sass_variables = []
    for i in range(num_variables):
        variable_name = f"variable-{i+1}"
        value_type = random.choice(['color', 'size', 'number'])
        
        if value_type == 'color':
            value = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        elif value_type == 'size':
            value = f"{random.randint(1, 100)}px"
        elif value_type == 'number':
            value = random.randint(1, 100)
        
        sass_variables.append({
            "name": variable_name,
            "value": value
        })
    return sass_variables

# Function to export variables to a .scss file
def export_to_scss(variables, filepath="output/scss/", filename="variables.scss"):
    path= os.path.abspath(filepath)
    output=path+"/"+filename    
    with open(output, 'w') as file:
        file.write("// Generated SASS Variables\n\n")
        for variable in variables:
            file.write(f"${variable['name']}: {variable['value']};\n")
    print(f"Variables exported to {filename} to {output}")

# Main function
def main():
    num_variables = 10  # Number of SASS variables to generate
    sass_variables = generate_sass_variables(num_variables)
    export_to_scss(sass_variables)

if __name__ == "__main__":
    main()