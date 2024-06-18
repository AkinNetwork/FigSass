import timeit
from ...FigSassSC.contract.json_processor import JSONProcessor
from ...FigSassSC.contract.data_validator_processor import DataValidatorProcessor

class FigsassEstimator:
    def __init__(self, directory):
        self.directory = directory
        self.json_processor = JSONProcessor(directory)
        self.validator_processor = DataValidatorProcessor("env/")
    
    def validate_json_as_figma(self, filename):
        json_data = self.json_processor.get_json_data(filename)
        if not json_data['status']:
            raise ValueError(f"Error processing {filename}: {json_data['message']}")
        
        return self.validator_processor.is_figma_data(json_data['data'])

    def estimate_cpu_effort(self, filename, number=10000):
        setup_code = f"""
from contract.json_processor import JSONProcessor
from contract.data_validator_processor import DataValidatorProcessor
json_processor = JSONProcessor("{self.directory}")
validator_processor = DataValidatorProcessor("env/")
filename = "{filename}"
json_data = json_processor.get_json_data(filename)
"""
        test_code = """
if json_data['status']:
    validator_processor.is_figma_data(json_data['data'])
"""
        # Measure execution time
        execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=number)
        
        return execution_time

# Example usage
if __name__ == "__main__":
    estimator = FigsassEstimator("fig")
    filename = "Primitives_ Akin Colours_LV.json"  # Replace with your JSON file name
    try:
        print(f"Validation Result: {estimator.validate_json_as_figma(filename)}")
        cpu_effort = estimator.estimate_cpu_effort(filename, number=10000)
        print(f"CPU Effort for validating {filename}: {cpu_effort} seconds for 10000 executions")
    except ValueError as e:
        print(e)
