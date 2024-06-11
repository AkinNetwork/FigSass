# Akin Network License
# Author: Margareta Sandor
#         margareta.sandor@akin.network

# Project: FigSass Conversion Smart Contract


# Objective 1: Read the Figma JSON file using a python data object

import os
import json

# Function to return the data from the json external file.
def get_json_data (directory, filename):
    result = {
        "status": True,
        "message": "",
        "data": {}
    }
    try:
        # Check if the directory is valid
        if not os.path.isdir(directory):
            raise ValueError(f"Error: '{directory}' is not a valid directory")
        
        # Check if the filename points to a JSON file
        if not filename.endswith('.json'):
            raise ValueError(f"Error: '{filename}' is not a JSON file")
        
        # Construct the full file path
        fullpath = os.path.join(directory, filename)
        
        # Check if the file exists
        if not os.path.exists(fullpath):
            raise FileNotFoundError(f"File not found: '{fullpath}'")
        
        # Read the JSON file
        with open(fullpath, 'r') as file:
            data = json.load(file)
        result['data'] = data
        result ['message'] = "The JSON file compilation is successfully completed."

    except (FileNotFoundError, ValueError, TypeError) as e:
        result['status'] = False
        result['message'] = str(e)
    # finally:
    #     print("END FUNCTION - get_json_data -- Finished checking and reading the JSON file")
    #     print (result)
    
    return result


# A function that extracts data from the metadata.json file based on the key provided as an argument.  
def get_metadata(par):
    result = {
       "status": True,
        "message": "",
        "data": {} 
    }
    
    try:
        # Check if the parameter is a valid
        if not isinstance(par, str):
            raise ValueError (f"Error: the '{par}' is not a valid key")
    
        #Extract data frm the metadata.json - if exists
        metadata = get_json_data("scr/", "metadata.json")
    
        if not metadata ['status']:
            raise FileNotFoundError (f"Error: '{metadata['message']}'")
        
        if par not in metadata['data']:
            raise KeyError (f"The key '{par}' does not exist in the JSON object.")
        
        # Get the value associated with the key
        result['data'] = metadata['data'][par]  
        result['message'] = f"Success: the data pertaining to the '{par}' key has been retrieved."
     
        
    except (FileNotFoundError, ValueError, KeyError) as e:
        result['status'] = False
        result['message'] = str(e)
    
    # finally:
    #     print("END FUNCTION - get_metadata --Finished extracting data from metadata.json")
        
    return result
     
# Function that confirms the Figma object structure
def is_figma_data (d):
    
    response = [True, ""]
    
    # Retrieve the Figma blueprint from the FigSass Smart Contract metadata.json
    meta_snipped = get_metadata('figma')
    
    try:  
        # Check the metadata and exit if the blueprint is not configured
        if not meta_snipped['status']:
            raise TypeError (f"Error: '{meta_snipped['message']}")

        else:
            # Extract the blueprint data and begin analysing the Figma object.
            # Confirm that the blueprint data is available; otherwise, raise an exception.
            if 'blueprint' not in meta_snipped ['data']:
                raise ValueError (f"Error: the Figma variable blueprint is not configured")
        
        # Extract the comparison data from the Figma blueprint 
        blueprint = meta_snipped['data']['blueprint']
        blueprint_keys = list(blueprint.keys())
        
        # Confirm that the blueprint parameters are configured; otherwise, raise an exception
        if not len(blueprint_keys)>0:
            raise ValueError (f"Error: the Figma blueprint parameters are missing")
        
        # Analyze each Figma dictionary snippet by comparing its keys with the requirements defined in the blueprint
        for bk in blueprint_keys:
            if bk == '1':
                response = check_figma_data(d, blueprint[bk])
                if not response[0]:
                    break
            elif bk == '2':
                sk =list(blueprint[bk].keys())
                if not sk:
                    raise ValueError("Error: the Figma blueprint configuration is incomplete")
                    
                for ssk in sk:
                    for snippet in d[ssk]:
                        response = check_figma_data(snippet,blueprint[bk][ssk] )
                        if not response[0]:
                            break
    # Manage response in case of exceptions
    except (TypeError, ValueError) as e:
        response = [False, str(e)]
    
    # finally:
    #    print("END FUNCTION - is_figma_data --Finished extracting data from metadata.json")
    
    return response    


# Functions that verifies the object structure against the figma blueprint object
def check_figma_data (o, blueprint):
    
    response = [True, ""]
   
    # Extract the primary keys of the object and compare them with the top_level_keys blueprint
    ojk = list(o.keys())    
    
    # The actual comparison of the data snipped with the blueprint key list 
    try:
        if ojk is None:
            raise ValueError ("The Figma snippet is not valid")
        response = [ojk == blueprint, f"The keys in the snippet {'match' if ojk == blueprint else 'do not match'} the Figma variable object structure."]       
    
    except ValueError as e:
        response = [False, str(e)]
       
    # finally:
    #     print (f"END FUNCTION - check_figma_data - Finished checking the snipped data with response: {response[1]}") 
        
    return response

# A function that extracts and validates the data from the Figma variable JSON file
def get_figma_data(folder, json_file):
    
    # Extract the data from JSON
    fig_data = get_json_data(folder, json_file)
    
    try:
        # Raise an exception if data has not available
        if not fig_data['status']:
            raise ValueError (f"Error: '{fig_data['message']}'")
        
        
        # Validate the json data structure as Figma variable data
        is_valid_fig_data = is_figma_data (fig_data['data'])
        fig_data['message'] = is_valid_fig_data[1]
       
        # Raise an exception if the data extracted is not the a Figma variable data
        if not is_valid_fig_data [0]:
            raise TypeError (f"Error: '{is_valid_fig_data[1]}")
         
    except (ValueError, TypeError) as e:
        fig_data['status'] = False
        fig_data['message'] = str(e)
        
        
    # finally:
    #     print("END FUNCTION - get_figma_data - Finished extracting and validating data from the Figma variable JSON file")        
    
    return fig_data
    
# Convert CSS rgba color from float representation (0.0 to 1.0) to decimal representation (0 to 255).
def css_rgba_to_decimal(rgba):
    rgba = (rgba["r"], rgba["g"], rgba["b"], rgba["a"])
    """
    Convert CSS rgba color from float representation (0.0 to 1.0) to decimal representation (0 to 255).

    Parameters:
    rgba (tuple): A tuple containing 4 float values (r, g, b, a) where r, g, b are between 0 and 1 and a is the alpha value.
    
    
    Parameter may be string programmatically formed through Figma data manipulation. We may need to check and convert the type.
    tuple_rgba = tuple(int(x) for x in rgba.split(','))
    
    color dictionary sample:
    
       rgba_dict = {
          "r": 0.9803921580314636,
          "g": 0.9908496737480164,
          "b": 1,
          "a": 1
        },
        
    The rgba conversion from the dictionary is: rgba = (rgba_dict["r"], rgba_dict["g"], rgba_dict["b"], rgba_dict["a"])
    
    Returns:
    tuple: A tuple containing 4 integer values (r, g, b, a) where r, g, b are between 0 and 255 and a is the alpha value.
    """
    if isinstance(rgba,str):
        rgba = tuple(int(x) for x in rgba.split(',')) 
        
    r, g, b, a = rgba
    return (int(r * 255), int(g * 255), int(b * 255), round(a, 2))

# Get the Figma variable specification
def get_fig_var_spec (fvo, vm, variables):
    
    """
    The format of the variable object is follows:
    {
        'id': 'VariableID:2:7', 
        'name': 'Akin Neutral/akin neutral 0', 
        'description': '', 
        'type': 'COLOR', 
        'valuesByMode': {
            '2:2': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 
            '2:3': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 
            '2:4': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 
            '2:5': {'r': 1, 'g': 1, 'b': 1, 'a': 1}}, 
        'resolvedValuesByMode': {
            '2:2': {'resolvedValue': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'alias': None}, 
            '2:3': {'resolvedValue': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'alias': None}, 
            '2:4': {'resolvedValue': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'alias': None}, 
            '2:5': {'resolvedValue': {'r': 1, 'g': 1, 'b': 1, 'a': 1}, 'alias': None}}, 
            'scopes': ['ALL_SCOPES'], 
            'hiddenFromPublishing': False, 
            'codeSyntax': {}
            }
    Once the object is processed we need to extract the following:
    --  variable name: extracted from the "name". Example: $akin-neutral-0
    --  variable theme: the valueByMode key identifies the theme ids relevant to each theme. 
               The result in this case will be theme name which will indicate later the directory name were 
               the variable will be saved in its respective scss file. If the mode is associated with a generic mode,
               the value will be by default empty string.
               Example: akin_network; akin_martech; akin_gethub; akin_digicraft
    --  variable value: extracted from valuesByMode directory snippet in respective to the theme. 
                        example: "rgba(255,255,255,1)" if the type is COLOR, or
                                 "0px" if the type is FLOAT and the name contain keyword SIZE
    Returns:
    Dictionary: A dictionary data structure containing three parameters: name, value, and theme, 
    prepared for appending to the variable array corresponding to the theme to which the variable belongs.
        
    Example: variables = {
                name: "$akin-neutral-0",
                value: "rgba(255,255,255,1)"
                theme: "akin_network"
                },{
                name: "$akin-neutral-0",
                value: "rgba(255,255,255,1)"
                theme: "akin_network" }
                
    """
  
    variable_name = "$" + fvo['name'].split("/")[-1].replace(" ", "-").replace("--","-")

    if 'valuesByMode' in fvo:
        for key, value in fvo['valuesByMode'].items():
            variable_value = f"rgba{css_rgba_to_decimal(value)}" if fvo['type'] == 'COLOR' else f"{ int(value/16) if (value/16).is_integer() else round(value/16, 3)} rem" if fvo['type'] == 'FLOAT' else ""
            variable_theme = vm[key] if 'mode' not in vm[key].strip() else ""
            v = {
                "name": variable_name,
                "value": variable_value,
                "theme": variable_theme
            }
            variables.append(v)  


# Function that gets the modes which will generate the theme directories
def get_modes (m):
    ft = {}
    for key, value in m.items():
        fv = value.lower().replace(" ", "_").replace("__", "_")
        ft [key] = fv
        
    return ft

# Function that exports the variables in the respective theme paths
def export_to_scss(variables, path="output/scss/"):
    """
    Exports variables to SCSS files.

    Args:
        variables (list of dicts): List of dictionaries where each dictionary contains variable information.
        path (str, optional): Path to the directory where SCSS files will be exported. Defaults to "output/scss/".
    """
    
    path = os.path.abspath(path)
    for v in variables:
        output_dir = os.path.join(path, v["theme"]) if v.get("theme") else path
        # mitigates the directory existence
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output = os.path.join(output_dir, "variables.scss")
        # mitigate the file management - write new file or add to an existing file
        mode = 'a' if os.path.exists(output) else 'w'
        with open(output, mode) as file:
            if mode == 'w':
                file.write(f"// Variables relevant to {v.get('theme', 'default')} theme;\n\n")
            # add the variable to the scss file only if has not been yet added
            if not is_variable_scss(output, v['name']):
                file.write(f"{v['name']}: {v['value']} !default;\n")

def is_variable_scss(file_path, variable_name):
    """
    Checks if a variable already exists in the file.

    Args:
        file_path (str): Path to the file to check.
        variable_name (str): Name of the variable to check.

    Returns:
        bool: True if variable exists, False otherwise.
    """
    return os.path.exists(file_path) and any(line.strip().startswith(variable_name + ":") for line in open(file_path, 'r'))
        
# Main function
def main():
    
    #indicate directory from which the json files shall be processed
    directory ="fig"
    
    #pass through all files available in the directory
    for filename in os.listdir(directory):
        print (f"directory: {directory} and file: {filename}")
        # extract the data from the Figma file
        figma_data = get_figma_data (directory, filename)

        # process te variables from Figma Data
        variables = []

        fm = get_modes (figma_data['data']['modes'])
        for vo in figma_data['data']['variables']:
            get_fig_var_spec (vo, fm, variables) #this function extends the variables array with new processed data
            
            
        # export variables to the respective scss files
        export_to_scss(variables)

if __name__ == "__main__":
    main()