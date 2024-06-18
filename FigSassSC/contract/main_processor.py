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

    def estimate_cpu_effort(self, filename):
        try:
            print(f"Estimating CPU effort for processing {filename}...\n")

            # Initialize variables
            cpu_effort_json = 0
            cpu_effort_validation = 0
            cpu_effort_figma_validation = 0
            cpu_effort_figma_variable_generation = 0
            cpu_effort_exporting = 0
            
            # Reading JSON
            cpu_effort_json = self.cpu_estimator.estimate_cpu_effort_for_reading(filename)
            print(f"CPU Effort for reading {filename}: {cpu_effort_json:.6f} seconds for 1000 executions")

            # Validation
            cpu_effort_validation = self.cpu_estimator.estimate_cpu_effort_for_validation(filename)
            print(f"CPU Effort for validating {filename}: {cpu_effort_validation:.6f} seconds for 1000 executions")

            json_data = self.json_processor.get_json_data(filename)
            if json_data['status']:
                # Figma Validation
                cpu_effort_figma_validation = self.cpu_estimator.estimate_cpu_effort_for_figma_validation(json_data['data'])
                print(f"CPU Effort for Figma validation: {cpu_effort_figma_validation:.6f} seconds for 1000 executions")

                # Figma Variable Generation
                cpu_effort_figma_variable_generation = self.cpu_estimator.estimate_cpu_effort_for_figma_variable_generation(json_data['data'])
                print(f"CPU Effort for Figma variable generation: {cpu_effort_figma_variable_generation:.6f} seconds for 1000 executions")

                # Exporting
                variables = []
                fm = self.validator_processor.get_modes(json_data['data']['modes'])
                for vo in json_data['data']['variables']:
                    self.validator_processor.get_fig_var_spec(vo, fm, variables)
                cpu_effort_exporting = self.cpu_estimator.estimate_cpu_effort_for_exporting(variables)
                print(f"CPU Effort for exporting: {cpu_effort_exporting:.6f} seconds for 1000 executions")

            # Total CPU effort for the whole process
            total_cpu_effort = (cpu_effort_json + cpu_effort_validation +
                                cpu_effort_figma_validation + cpu_effort_figma_variable_generation +
                                cpu_effort_exporting)
            print(f"Total CPU Effort for processing {filename}: {total_cpu_effort:.6f} seconds for 1000 executions")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    processor = MainProcessor("fig", "output/scss/")
    filename = "sample.json"  # Replace with your JSON file name
    try:
        print(f"Validation Result: {processor.validate_json_as_figma(filename)}")
        processor.estimate_cpu_effort(filename)
    except ValueError as e:
        print(e)
