import os
from .json_processor import JSONProcessor
from .data_validator_processor import DataValidatorProcessor
from .data_exporter import DataExporter

class MainProcessor:
    def __init__(self, directory, export_path):
        self.directory = directory
        self.export_path = export_path

    def main(self):
        json_processor = JSONProcessor(self.directory)
        validator_processor = DataValidatorProcessor("env/")
        exporter = DataExporter(self.export_path)

        json_files_data = json_processor.validate_json_files()
        
        for data in json_files_data:
            variables = []
            fm = validator_processor.get_modes(data['modes'])
            for vo in data['variables']:
                validator_processor.get_fig_var_spec(vo, fm, variables)
            exporter.export_to_scss(variables)

if __name__ == "__main__":
    processor = MainProcessor("fig", "output/scss/")
    processor.main()
