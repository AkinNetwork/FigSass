from contract import MainProcessor

def run_test():
    # Specify the directory containing your Figma JSON files
    directory = "fig"
    
    # Specify the path where the SCSS files will be exported
    export_path = "output/scss/"
    
    # Create an instance of MainProcessor with the directory and export path
    processor = MainProcessor(directory, export_path)
    
    # Run the main process
    processor.main()

if __name__ == "__main__":
    run_test()
