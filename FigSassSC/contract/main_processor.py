import os
from .data_validator_processor import DataValidatorProcessor
from .data_exporter import DataExporter

class MainProcessor:
    def __init__(self, directory, export_path):
        self.directory = directory
        self.export_path = export_path

    def main(self):
        validator_processor = DataValidatorProcessor("env/")
        exporter = DataExporter(self.export_path)

        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                print(f"Processing directory: {self.directory}, file: {filename}")
                figma_data = validator_processor.get_figma_data(self.directory, filename)
                if not figma_data['status']:
                    print(f"Error processing {filename}: {figma_data['message']}")
                    continue

                variables = []
                fm = validator_processor.get_modes(figma_data['data']['modes'])
                for vo in figma_data['data']['variables']:
                    validator_processor.get_fig_var_spec(vo, fm, variables)
                exporter.export_to_scss(variables)