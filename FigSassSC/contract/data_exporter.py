import os

class DataExporter:
    def __init__(self, path="output/scss/"):
        self.path = os.path.abspath(path)
    
    def export_to_scss(self, variables):
        for v in variables:
            output_dir = os.path.join(self.path, v["theme"]) if v.get("theme") else self.path
            os.makedirs(output_dir, exist_ok=True)
            output = os.path.join(output_dir, "variables.scss")
            mode = 'a' if os.path.exists(output) else 'w'
            with open(output, mode) as file:
                if mode == 'w':
                    file.write(f"// Variables relevant to {v.get('theme', 'default')} theme;\n\n")
                if not self.is_variable_scss(output, v['name']):
                    file.write(f"{v['name']}: {v['value']} !default;\n")

    @staticmethod
    def is_variable_scss(file_path, variable_name):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as file:
            return any(line.strip().startswith(variable_name + ":") for line in file)
