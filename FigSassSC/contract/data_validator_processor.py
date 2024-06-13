from .json_processor import JSONProcessor
from functools import lru_cache

class DataValidatorProcessor:
    def __init__(self, metadata_dir):
        self.metadata_dir = metadata_dir
    
    @lru_cache(maxsize=32)
    def get_metadata(self, key):
        try:
            if not isinstance(key, str):
                raise ValueError(f"Error: the '{key}' is not a valid key")
            
            metadata = JSONProcessor(self.metadata_dir).get_json_data("metadata.json")
            
            if not metadata['status']:
                raise FileNotFoundError(f"Error: '{metadata['message']}'")
            
            if key not in metadata['data']:
                raise KeyError(f"The key '{key}' does not exist in the JSON object.")
            
            return {"status": True, "message": "Success", "data": metadata['data'][key]}
        
        except (FileNotFoundError, ValueError, KeyError) as e:
            return {"status": False, "message": str(e), "data": {}}
    
    def is_figma_data(self, data):
        try:
            meta_snipped = self.get_metadata('figma')
            if not meta_snipped['status']:
                raise TypeError(f"Error: '{meta_snipped['message']}'")

            if 'blueprint' not in meta_snipped['data']:
                raise ValueError("Error: the Figma variable blueprint is not configured")

            blueprint = meta_snipped['data']['blueprint']
            blueprint_keys = list(blueprint.keys())

            if not blueprint_keys:
                raise ValueError("Error: the Figma blueprint parameters are missing")

            for bk in blueprint_keys:
                if bk == '1':
                    response = self.check_figma_data(data, blueprint[bk])
                    if not response[0]:
                        return response
                elif bk == '2':
                    for ssk in blueprint[bk]:
                        for snippet in data.get(ssk, []):
                            response = self.check_figma_data(snippet, blueprint[bk][ssk])
                            if not response[0]:
                                return response

            return [True, "Figma data is valid"]

        except (TypeError, ValueError) as e:
            return [False, str(e)]
    
    @staticmethod
    def check_figma_data(obj, blueprint):
        obj_keys = list(obj.keys())
        return [obj_keys == blueprint, f"The keys in the snippet {'match' if obj_keys == blueprint else 'do not match'} the Figma variable object structure."]

    def get_figma_data(self, folder, json_file):
        fig_data = JSONProcessor(folder).get_json_data(json_file)
        
        try:
            if not fig_data['status']:
                raise ValueError(f"Error: '{fig_data['message']}'")
            
            is_valid_fig_data = self.is_figma_data(fig_data['data'])
            fig_data['message'] = is_valid_fig_data[1]
            
            if not is_valid_fig_data[0]:
                raise TypeError(f"Error: '{is_valid_fig_data[1]}'")
        
        except (ValueError, TypeError) as e:
            fig_data['status'] = False
            fig_data['message'] = str(e)
        
        return fig_data
    
    @staticmethod
    def css_rgba_to_decimal(rgba):
        rgba = (rgba["r"], rgba["g"], rgba["b"], rgba["a"])
        return (int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255), round(rgba[3], 2))

    def get_fig_var_spec(self, fvo, vm, variables):
        variable_name = "$" + fvo['name'].split("/")[-1].replace(" ", "-").replace("--", "-")

        if 'valuesByMode' in fvo:
            for key, value in fvo['valuesByMode'].items():
                variable_value = f"rgba{self.css_rgba_to_decimal(value)}" if fvo['type'] == 'COLOR' else f"{int(value / 16) if (value / 16).is_integer() else round(value / 16, 3)} rem" if fvo['type'] == 'FLOAT' else ""
                variable_theme = vm[key] if 'mode' not in vm[key].strip() else ""
                variables.append({
                    "name": variable_name,
                    "value": variable_value,
                    "theme": variable_theme
                })

    @staticmethod
    def get_modes(m):
        return {key: value.lower().replace(" ", "_").replace("__", "_") for key, value in m.items()}
