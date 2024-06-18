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
            
            # Reading JSON
            single_execution_time, executions_needed = self.cpu_estimator.estimate_cpu_effort_for_reading(filename)
            print(f"CPU Effort for reading {filename}: {single_execution_time:.6f} seconds for a single execution")
            print(f"Executions needed to achieve 1 second: {executions_needed:.2f}")

            # Validation
            single_execution_time, executions_needed = self.cpu_estimator.estimate_cpu_effort_for_validation(filename)
            print(f"CPU Effort for validating {filename}: {single_execution_time:.6f} seconds for a single execution")
            print(f"Executions needed to achieve 1 second: {executions_needed:.2f}")

            json_data = self.json_processor.get_json_data(filename)
            if json_data['status']:
                # Figma Validation
                single_execution_time, executions_needed = self.cpu_estimator.estimate_cpu_effort_for_figma_validation(json_data['data'])
                print(f"CPU Effort for Figma validation: {single_execution_time:.6f} seconds for a single execution")
                print(f"Executions needed to achieve 1 second: {executions_needed:.2f}")

                # Figma Variable Generation
                single_execution_time, executions_needed = self.cpu_estimator.estimate_cpu_effort_for_figma_variable_generation(json_data['data'])
                print(f"CPU Effort for Figma variable generation: {single_execution_time:.6f} seconds for a single execution")
                print(f"Executions needed to achieve 1 second: {executions_needed:.2f}")

                # Exporting
                variables = []
                fm = self.validator_processor.get_modes(json_data['data']['modes'])
                for vo in json_data['data']['variables']:
                    self.validator_processor.get_fig_var_spec(vo, fm, variables)
                single_execution_time, executions_needed = self.cpu_estimator.estimate_cpu_effort_for_exporting(variables)
                print(f"CPU Effort for exporting: {single_execution_time:.6f} seconds for a single execution")
                print(f"Executions needed to achieve 1 second: {executions_needed:.2f}")

            # Total CPU effort for the whole process
            total_cpu_effort = (single_execution_time + executions_needed)
            print(f"Total CPU Effort for processing {filename}: {total_cpu_effort:.6f} seconds for a single execution")
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
