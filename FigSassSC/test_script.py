from contract import MainProcessor

def run_test():
    # Specify the directory containing your Figma JSON files
    directory = "fig"
    
    # Create an instance of MainProcessor with the directory
    processor = MainProcessor(directory)
    
    # Run the main process
    processor.main()

if __name__ == "__main__":
    run_test()
