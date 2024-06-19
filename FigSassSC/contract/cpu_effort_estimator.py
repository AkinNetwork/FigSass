import timeit
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
from contract.data_exporter import DataExporter

class CPUEffortEstimator:
    TDP = 28  # Thermal Design Power in watts

    def __init__(self, directory, metadata_dir, export_path):
        self.json_processor = JSONProcessor(directory)
        self.validator_processor = DataValidatorProcessor(metadata_dir)
        self.exporter = DataExporter(export_path)

    def time_single_execution(self, setup_code, test_code, globals_dict=None):
        return timeit.timeit(stmt=test_code, setup=setup_code, number=1, globals=globals_dict)

    def estimate_executions_needed(self, single_execution_time, target_time=1.0):
        return target_time / single_execution_time if single_execution_time > 0 else float('inf')

    def estimate_cpu_effort(self, setup_code, test_code, globals_dict=None):
        single_execution_time = self.time_single_execution(setup_code, test_code, globals_dict)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

    def estimate_cpu_effort_for_reading(self, filename):
        setup_code = f"""
from contract.json_processor import JSONProcessor
json_processor = JSONProcessor("{self.json_processor.directory}")
filename = "{filename}"
"""
        test_code = "json_processor.get_json_data(filename)"
        return self.estimate_cpu_effort(setup_code, test_code)

    def estimate_cpu_effort_for_validation(self, filename):
        json_data = self.json_processor.get_json_data(filename)['data']
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
"""
        test_code = "validator_processor.is_figma_data(json_data)"
        return self.estimate_cpu_effort(setup_code, test_code, globals_dict={'json_data': json_data})

    def estimate_cpu_effort_for_figma_validation(self, json_data):
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
"""
        test_code = "validator_processor.is_figma_data(json_data)"
        return self.estimate_cpu_effort(setup_code, test_code, globals_dict={'json_data': json_data})

    def estimate_cpu_effort_for_figma_variable_generation(self, json_data):
        variables = []
        fm = self.validator_processor.get_modes(json_data['modes'])
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
variables = []
fm = {fm}
"""
        test_code = f"""
for vo in json_data['variables']:
    validator_processor.get_fig_var_spec(vo, fm, variables)
"""
        return self.estimate_cpu_effort(setup_code, test_code, globals_dict={'json_data': json_data, 'variables': variables})

    def estimate_cpu_effort_for_exporting(self, variables):
        setup_code = f"""
from contract.data_exporter import DataExporter
exporter = DataExporter("{self.exporter.path}")
"""
        test_code = "exporter.export_to_scss(variables)"
        return self.estimate_cpu_effort(setup_code, test_code, globals_dict={'variables': variables})

    def estimate_total_cpu_effort(self, filename):
        total_time = 0.0

        # Reading JSON
        reading_time, _ = self.estimate_cpu_effort_for_reading(filename)
        total_time += reading_time
        print(f"CPU Effort for reading JSON: {reading_time:.6f} seconds")

        # Validation
        json_data = self.json_processor.get_json_data(filename)['data']
        validation_time, _ = self.estimate_cpu_effort_for_validation(filename)
        total_time += validation_time
        print(f"CPU Effort for JSON validation: {validation_time:.6f} seconds")

        if json_data:
            # Figma Validation
            figma_validation_time, _ = self.estimate_cpu_effort_for_figma_validation(json_data)
            total_time += figma_validation_time
            print(f"CPU Effort for Figma validation: {figma_validation_time:.6f} seconds")

            # Figma Variable Generation
            figma_variable_generation_time, _ = self.estimate_cpu_effort_for_figma_variable_generation(json_data)
            total_time += figma_variable_generation_time
            print(f"CPU Effort for Figma variable generation: {figma_variable_generation_time:.6f} seconds")

            # Exporting
            variables = []
            fm = self.validator_processor.get_modes(json_data['modes'])
            for vo in json_data['variables']:
                self.validator_processor.get_fig_var_spec(vo, fm, variables)
            exporting_time, _ = self.estimate_cpu_effort_for_exporting(variables)
            total_time += exporting_time
            print(f"CPU Effort for exporting variables: {exporting_time:.6f} seconds")

        print(f"Total CPU Effort: {total_time:.6f} seconds")
        return total_time

    def calculate_average_power_consumption(self, total_time):
        """
        Calculate the average power consumption based on the TDP and total execution time.

        :param total_time: The total execution time in seconds
        :return: The average power consumption in watt-seconds (joules)
        """
        average_power_consumption = self.TDP * total_time  # TDP is in watts, time is in seconds
        print(f"Average Power Consumption: {average_power_consumption:.2f} joules")
        return average_power_consumption

