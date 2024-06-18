import timeit
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
from contract.data_exporter import DataExporter

class CPUEffortEstimator:
    def __init__(self, directory, metadata_dir, export_path):
        self.json_processor = JSONProcessor(directory)
        self.validator_processor = DataValidatorProcessor(metadata_dir)
        self.exporter = DataExporter(export_path)

    def estimate_cpu_effort_for_reading(self, filename, number=1000):
        setup_code = f"""
from contract.json_processor import JSONProcessor
json_processor = JSONProcessor("{self.json_processor.directory}")
filename = "{filename}"
"""
        test_code = """
json_processor.get_json_data(filename)
"""
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        return execution_time

    def estimate_cpu_effort_for_validation(self, filename, number=1000):
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
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        return execution_time

    def estimate_cpu_effort_for_figma_validation(self, json_data, number=1000):
        setup_code = f"""
from contract.data_validator_processor import DataValidatorProcessor
validator_processor = DataValidatorProcessor("{self.validator_processor.metadata_dir}")
json_data = {json_data}
"""
        test_code = """
validator_processor.is_figma_data(json_data)
"""
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        return execution_time

    def estimate_cpu_effort_for_figma_variable_generation(self, json_data, number=1000):
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
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        return execution_time

    def estimate_cpu_effort_for_exporting(self, variables, number=1000):
        setup_code = f"""
from contract.data_exporter import DataExporter
exporter = DataExporter("{self.exporter.path}")
variables = {variables}
"""
        test_code = """
exporter.export_to_scss(variables)
"""
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        return execution_time
