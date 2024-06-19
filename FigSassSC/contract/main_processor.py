import os
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
from contract.data_exporter import DataExporter
from contract.cpu_effort_estimator import CPUEffortEstimator

class MainProcessor:
    def __init__(self, directory, export_path):
        self.directory = directory
        self.export_path = export_path
        self.json_processor = JSONProcessor(directory)
        self.validator_processor = DataValidatorProcessor("env/")
        self.exporter = DataExporter(export_path)
        self.cpu_estimator = CPUEffortEstimator(directory, "env/", export_path)

    def main(self):
        json_files_data = self.json_processor.validate_json_files()
        
        for data in json_files_data:
            variables = []
            fm = self.validator_processor.get_modes(data['modes'])
            for vo in data['variables']:
                self.validator_processor.get_fig_var_spec(vo, fm, variables)
            self.exporter.export_to_scss(variables)

    def validate_json_as_figma(self, filename):
        json_data = self.json_processor.get_json_data(filename)
        if not json_data['status']:
            raise ValueError(f"Error processing {filename}: {json_data['message']}")
        
        return self.validator_processor.is_figma_data(json_data['data'])

    def estimate_total_cpu_effort(self, filename):
        try:
            print(f"Estimating CPU effort for processing {filename}...\n")

            # Total CPU effort for the whole process
            total_cpu_effort = self.cpu_estimator.estimate_total_cpu_effort(filename)
            print(f"Total CPU Effort for processing {filename}: {total_cpu_effort:.6f} seconds for a single execution")

        except ValueError as e:
            print(e)

if __name__ == "__main__":
    processor = MainProcessor("fig", "output/scss/")
    filename = "sample.json"  # Replace with your JSON file name
    try:
        print(f"Validation Result: {processor.validate_json_as_figma(filename)}")
        processor.estimate_total_cpu_effort(filename)
    except ValueError as e:
        print(e)
