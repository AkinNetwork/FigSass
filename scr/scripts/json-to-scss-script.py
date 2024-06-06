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
        print("END FUNCTION - get_json_data -- Finished checking and reading the JSON file")
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
        print("END FUNCTION - get_metadata --Finished extracting data from metadata.json")
        
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
        blueprint_keys = get_keys_list (blueprint)
        
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
                sk = get_keys_list(blueprint[bk])
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
    
    finally:
       print("END FUNCTION - is_figma_data --Finished extracting data from metadata.json")
    
    return response    


# Functions that verifies the object structure against the figma blueprint object
def check_figma_data (o, blueprint):
    
    response = [True, ""]
   
    # Extract the primary keys of the object and compare them with the top_level_keys blueprint
    ojk= get_keys_list(o)    
    
    # The actual comparison of the data snipped with the blueprint key list 
    try:
        if ojk is None:
            raise ValueError ("The Figma snippet is not valid")
        response = [ojk == blueprint, f"The keys in the snippet {'match' if ojk == blueprint else 'do not match'} the Figma variable object structure."]       
    
    except ValueError as e:
        response = [False, str(e)]
       
    finally:
        print (f"END FUNCTION - check_figma_data - Finished checking the snipped data with response: {response[1]}") 
        
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
        print("END FUNCTION - get_figma_data - Finished extracting and validating data from the Figma variable JSON file")        
    
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