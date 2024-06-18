import timeit
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
from contract.data_exporter import DataExporter

class CPUEffortEstimator:
    def __init__(self, directory, metadata_dir, export_path):
        self.json_processor = JSONProcessor(directory)
        self.validator_processor = DataValidatorProcessor(metadata_dir)
        self.exporter = DataExporter(export_path)

    def time_single_execution(self, setup_code, test_code):
        return timeit.timeit(stmt=test_code, setup=setup_code, number=1)

    def estimate_executions_needed(self, single_execution_time, target_time=1.0):
        return target_time / single_execution_time if single_execution_time > 0 else float('inf')

    def estimate_cpu_effort_for_reading(self, filename):
        setup_code = f"""
from contract.json_processor import JSONProcessor
json_processor = JSONProcessor("{self.json_processor.directory}")
filename = "{filename}"
"""
        test_code = """
json_processor.get_json_data(filename)
"""
        single_execution_time = self.time_single_execution(setup_code, test_code)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

    def estimate_cpu_effort_for_validation(self, filename):
        setup_code = f"""
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
json_processor = JSONProcessor("{self.json_processor.directory}")
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
filename = "{filename}"
json_data = json_processor.get_json_data(filename)
"""
        test_code = """
if json_data['status']:
    validator_processor.is_figma_data(json_data['data'])
"""
        single_execution_time = self.time_single_execution(setup_code, test_code)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

    def estimate_cpu_effort_for_figma_validation(self, json_data):
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
json_data = {json_data}
"""
        test_code = """
validator_processor.is_figma_data(json_data)
"""
        single_execution_time = self.time_single_execution(setup_code, test_code)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

    def estimate_cpu_effort_for_figma_variable_generation(self, json_data):
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
variables = []
fm = validator_processor.get_modes({json_data['modes']})
"""
        test_code = """
for vo in {json_data['variables']}:
    validator_processor.get_fig_var_spec(vo, fm, variables)
"""
        single_execution_time = self.time_single_execution(setup_code, test_code)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

    def estimate_cpu_effort_for_exporting(self, variables):
        setup_code = f"""
from contract.data_exporter import DataExporter
exporter = DataExporter("{self.exporter.path}")
variables = {variables}
"""
        test_code = """
exporter.export_to_scss(variables)
"""
        single_execution_time = self.time_single_execution(setup_code, test_code)
        executions_needed = self.estimate_executions_needed(single_execution_time)
        return single_execution_time, executions_needed

