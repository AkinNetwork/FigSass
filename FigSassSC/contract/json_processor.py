import os
import json

class JSONProcessor:
    def __init__(self, directory):
        self.directory = directory
    
    def get_json_data(self, filename):
        result = {
            "status": True,
            "message": "",
            "data": {}
        }
        try:
            if not os.path.isdir(self.directory):
                raise ValueError(f"Error: '{self.directory}' is not a valid directory")
            
            if not filename.endswith('.json'):
                raise ValueError(f"Error: '{filename}' is not a JSON file")
            
            fullpath = os.path.join(self.directory, filename)
            
            if not os.path.exists(fullpath):
                raise FileNotFoundError(f"File not found: '{fullpath}'")
            
            with open(fullpath, 'r') as file:
                data = json.load(file)
            result['data'] = data
            result['message'] = "The JSON file compilation is successfully completed."

        except (FileNotFoundError, ValueError, TypeError) as e:
            result['status'] = False
            result['message'] = str(e)
        
        return result

    def validate_json_files(self):
        json_files_data = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                json_data = self.get_json_data(filename)
                if json_data['status']:
                    json_files_data.append(json_data['data'])
                else:
                    print(f"Error processing {filename}: {json_data['message']}")
        return json_files_data
