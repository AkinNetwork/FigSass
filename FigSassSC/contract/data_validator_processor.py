from .json_processor import JSONProcessor

class DataValidatorProcessor:
    def __init__(self, metadata_dir):
        self.metadata_dir = metadata_dir
    
    def get_metadata(self, key):
        result = {
            "status": True,
            "message": "",
            "data": {}
        }
        
        try:
            if not isinstance(key, str):
                raise ValueError(f"Error: the '{key}' is not a valid key")
            
            metadata = JSONProcessor(self.metadata_dir).get_json_data("metadata.json")
            
            if not metadata['status']:
                raise FileNotFoundError(f"Error: '{metadata['message']}'")
            
            if key not in metadata['data']:
                raise KeyError(f"The key '{key}' does not exist in the JSON object.")
            
            result['data'] = metadata['data'][key]
            result['message'] = f"Success: the data pertaining to the '{key}' key has been retrieved."

        except (FileNotFoundError, ValueError, KeyError) as e:
            result['status'] = False
            result['message'] = str(e)
        
        return result
    
    def is_figma_data(self, data):
        response = [True, ""]
        meta_snipped = self.get_metadata('figma')
        
        try:
            if not meta_snipped['status']:
                raise TypeError(f"Error: '{meta_snipped['message']}'")

            if 'blueprint' not in meta_snipped['data']:
                raise ValueError("Error: the Figma variable blueprint is not configured")

            blueprint = meta_snipped['data']['blueprint']
            blueprint_keys = list(blueprint.keys())

            if not len(blueprint_keys) > 0:
                raise ValueError("Error: the Figma blueprint parameters are missing")

            for bk in blueprint_keys:
                if bk == '1':
                    response = self.check_figma_data(data, blueprint[bk])
                    if not response[0]:
                        break
                elif bk == '2':
                    sk = list(blueprint[bk].keys())
                    if not sk:
                        raise ValueError("Error: the Figma blueprint configuration is incomplete")
                    
                    for ssk in sk:
                        for snippet in data[ssk]:
                            response = self.check_figma_data(snippet, blueprint[bk][ssk])
                            if not response[0]:
                                break

        except (TypeError, ValueError) as e:
            response = [False, str(e)]
        
        return response
    
    def check_figma_data(self, obj, blueprint):
        response = [True, ""]
        obj_keys = list(obj.keys())
        
        try:
            if obj_keys is None:
                raise ValueError("The Figma snippet is not valid")
            response = [obj_keys == blueprint, f"The keys in the snippet {'match' if obj_keys == blueprint else 'do not match'} the Figma variable object structure."]
        
        except ValueError as e:
            response = [False, str(e)]
        
        return response

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
    
    def css_rgba_to_decimal(self, rgba):
        rgba = (rgba["r"], rgba["g"], rgba["b"], rgba["a"])
        if isinstance(rgba, str):
            rgba = tuple(int(x) for x in rgba.split(','))
        
        r, g, b, a = rgba
        return (int(r * 255), int(g * 255), int(b * 255), round(a, 2))

    def get_fig_var_spec(self, fvo, vm, variables):
        variable_name = "$" + fvo['name'].split("/")[-1].replace(" ", "-").replace("--", "-")

        if 'valuesByMode' in fvo:
            for key, value in fvo['valuesByMode'].items():
                variable_value = f"rgba{self.css_rgba_to_decimal(value)}" if fvo['type'] == 'COLOR' else f"{int(value / 16) if (value / 16).is_integer() else round(value / 16, 3)} rem" if fvo['type'] == 'FLOAT' else ""
                variable_theme = vm[key] if 'mode' not in vm[key].strip() else ""
                v = {
                    "name": variable_name,
                    "value": variable_value,
                    "theme": variable_theme
                }
                variables.append(v)

    def get_modes(self, m):
        ft = {}
        for key, value in m.items():
            fv = value.lower().replace(" ", "_").replace("__", "_")
            ft[key] = fv
        return ft
