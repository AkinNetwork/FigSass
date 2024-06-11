import os

class DataExporter:
    def export_to_scss(self, variables, path="output/scss/"):
        path = os.path.abspath(path)
        for v in variables:
            output_dir = os.path.join(path, v["theme"]) if v.get("theme") else path
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output = os.path.join(output_dir, "variables.scss")
            mode = 'a' if os.path.exists(output) else 'w'
            with open(output, mode) as file:
                if mode == 'w':
                    file.write(f"// Variables relevant to {v.get('theme', 'default')} theme;\n\n")
                if not self.is_variable_scss(output, v['name']):
                    file.write(f"{v['name']}: {v['value']} !default;\n")

    def is_variable_scss(self, file_path, variable_name):
        return os.path.exists(file_path) and any(line.strip().startswith(variable_name + ":") for line in open(file_path, 'r'))
