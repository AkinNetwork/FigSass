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
    finally:
        print("Finished checking and reading the JSON file")
        #print (result)
    
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
    
    finally:
        print("Finished extracting data from metadata.json")
        
    return result
     
# Function that confirms the Figma object structure
def is_figma_data (d):
    ost = check_figma_data (d)
    if ost[0]:
        for v in d['variables']:
           ost = check_figma_data(v, 'variables')
           if not ost[0]:
               print(f"Error: '{ost[1]}'")
               break

    return ost    


# Functions that verifies the object structure against the figma blueprint object
def check_figma_data (o, p='keys'):
    
    response = [True, ""]
    
    # Retrieve the Figma blueprint from the FigSass Smart Contract metadata.json
    meta_snipped = get_metadata('figma')
   
    # Extract the primary keys of the object and compare them with the top_level_keys blueprint
    ojk= get_keys_list(o)    
  
    # The actual validation/ authentication process   
    try:
        if ojk is None:
            raise ValueError ("The Figma object value is none")
        
        if not meta_snipped['status']:
            raise ValueError (f"Error: '{meta_snipped['message']}")
        
        else:
            if 'blueprint' not in meta_snipped ['data']:
                raise ValueError (f"Error: the Figma variable blueprint is not configured")
  
        response = [ojk == meta_snipped['data']['blueprint'][p], f"The keys in the document {'match' if ojk == meta_snipped['data']['blueprint'][p] else 'do not match'} the Figma variable object structure."]
            
    
    except ValueError as e:
       response = [False, str(e)]
       
    finally:
       print (f"Finished checking the data relevant to the '{p}' key") 
        
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
        
        
    finally:
        print("Finished extracting and validating data from the Figma variable JSON file")        
    
    return fig_data

# Get the Figma object key structure
def get_keys_list (l):
    keys = []
    keys = l.keys()
    keys_list = list(keys)
    return keys_list

    

# Main function
def main():
    # extract the data from the Figma file
    figma_data = get_figma_data ("fig", "Primitives_ Akin Colours_LV.json")
    #print (figma_data)
   
    # validate the json object by comparing the figma variables blueprint
    #vr=is_figma_var(figma_data)
    #print (f"MAIN --> is_figma_var trigger function>-- RESULT: {vr[1]}")

if __name__ == "__main__":
    main()