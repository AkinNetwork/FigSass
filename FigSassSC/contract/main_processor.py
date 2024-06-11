import os
from .json_processor import JSONProcessor
from .data_validator_processor import DataValidatorProcessor
from .data_exporter import DataExporter

class MainProcessor:
    def __init__(self, directory):
        self.directory = directory

    def main(self):
        json_processor = JSONProcessor(self.directory)
        validator_processor = DataValidatorProcessor("scr/")
        exporter = DataExporter()

        for filename in os.listdir(self.directory):
            print(f"directory: {self.directory} and file: {filename}")
            figma_data = validator_processor.get_figma_data(self.directory, filename)
            variables = []
            fm = validator_processor.get_modes(figma_data['data']['modes'])
            for vo in figma_data['data']['variables']:
                validator_processor.get_fig_var_spec(vo, fm, variables)
            exporter.export_to_scss(variables)

if __name__ == "__main__":
    processor = MainProcessor("fig")
    processor.main()
