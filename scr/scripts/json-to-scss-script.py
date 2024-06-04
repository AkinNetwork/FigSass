# Akin Network License
# Author: Margareta Sandor
#         margareta.sandor@akin.network

# Project: FigSass Conversion Smart Contract


# Objective 1: Read the Figma JSON file using a python data object

import os
import json

# Function to return the data from the json external file.
def get_json_data (file_path, file_name):
    
    # Define the path to the JSON file
    file = os.path.abspath (file_path) + "/" + file_name
  
    # Open and read the Figma file
    with open (file, 'r') as the_file:
        data = json.load (the_file)

    # Print data as test
    # print (figma_data)
    
    # Return the data as object
    return data


# Function that confirms the Figma object structure
def is_figma_var (d): #is the data provided a figma variable object?
    ost = check_figma(d)
    if ost[0] == True:
        for v in d['variables']:
           ost = check_figma(v, "variables")
           if not ost[0]:
               print(f"3 ----> BREAKING THE FOR LOOP -- {ost[0]} --> {ost[1]}")
               break
    else:
        print (f"1 --> is_figma_var trigger function>-- RESULT: {ost[1]}")
    return ost    


# Functions that verifies the object structure against the figma blueprint object
def check_figma (o, p="keys"):
    # Retrieve the Figma blueprint from the FigSass Smart Contract metadata.json
    metadata = get_json_data("scr/", "metadata.json")
    #print (metadata['figma']['blueprint'][p])
    # TODO - mitigate the risk of not having a blueprint at all
    
    # Extract the primary keys of the object and compare them with the top_level_keys blueprint
    ojk= get_keys_list(o)    
    #print(ojk)
 
    # The actual validation/ authentication process
    response = [True, ""]
    try:
        if ojk is None:
            response=[False, f"The document is None and can not be processed"]
            raise ValueError ("The Figma object value is none")
        else:
            response = [ojk == metadata['figma']['blueprint'][p], f"The keys in the document {'match' if ojk == metadata['figma']['blueprint'][p] else 'do not match'} the Figma variable object structure."]
            
    
    except ValueError as e:
       response = [False, str(e)]
       
    except TypeError as e:
        response = [False, f"Type error: {e}"]
       
    else:
        response = [ojk == metadata['figma']['blueprint'][p], f"The keys in the document {'match' if ojk == metadata['figma']['blueprint'][p] else 'do not match'} the Figma variable object structure."]    
    
    #finally:
       # print (f"0 --> check_figma function<-- Check completed with result: {response[1]}") 
        
    return response
    
   

# Get the Figma object key structure
def get_keys_list (l):
    keys = []
    keys = l.keys()
    keys_list = list(keys)
    return keys_list

    

# Main function
def main():
    # extract the data from the Figma file
    figma_data = get_json_data ("fig", "Primitives_ Akin Colours_LV.json")
    # print (figma_data)
   
    # validate the json object by comparing the figma variables blueprint
    vr=is_figma_var(figma_data)
    print (f"MAIN --> is_figma_var trigger function>-- RESULT: {vr[1]}")


if __name__ == "__main__":
    main()