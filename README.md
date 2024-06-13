# FigSass Smart Contract

Project name: _FigSass Smart Contract_

This endeavor revolves around transforming Figma JSON variables into a SCSS variable framework. We'll employ a smart contract to streamline the process of converting Figma variable JSON exports into a corresponding array of variables, which will then be integrated into a SCSS file.

Author's note: While we draw upon the principles of Ethereum smart contracts, this project does not pertain to blockchain Ethereum smart contracts. Instead, it operates as a mini-application based on smart contract principles.

## The Algorithm

1. Set-up Python environment.
   1. Check the and update the installed Python version.
   2. requisites: Homebrew: <https://brew.sh/> - installed with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)`
2. FigSass Smart Contract **algorithm:**
   1. Read the Figma JSON file using a python data object
   2. Export data into a file with extension .scss
   3. Check and validate the imported JSON file as Figma variable JSON file
   4. Format the variables as SCSS variables and save them into \_variables.scss file

## Testing

To properly test the package, you should:

1. Prepare Test Data: Ensure you have the necessary Figma JSON files in the specified directory (fig).
2. Check Output: Verify that the output SCSS files are generated correctly in the output/scss/ directory as specified in the DataExporter class.
3. Debug and Verify: If the output is not as expected, add print statements or use a debugger to step through the code and verify that each part is functioning correctly.

### Directory setup

FigSassSC/
│
├── contract/
│ ├── **init**.py
│ ├── json_processor.py
│ ├── data_validator_processor.py
│ ├── data_exporter.py
│ └── main_processor.py
│
├── fig/
│ ├── file1.json
│ └── file2.json
│
└── test_script.py
└── metadata.json

### Running the Test Script

1. Navigate to Your Project Directory: Open a terminal and navigate to the root directory of your project (your_project/).
2. Install Any Dependencies: If your package requires any external libraries (e.g., json), make sure they are installed. You can use pip to install them. For example:

`pip install -r requirements.txt`

3. Run the Test Script: Execute the test script using Python.

`python test_script.py`

This will run the MainProcessor's main function, which processes the JSON files in the specified directory (fig), validates them, processes them, and exports the results.

### Running FigSass as CLI

You can now run the script from the command line and provide the directory and output path:

`python figsass.py fig --output custom_output/scss/`

This will:

1. Use the fig directory for input files.
2. Export the SCSS files to custom_output/scss/.
