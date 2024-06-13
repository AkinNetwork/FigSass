import argparse
from contract import MainProcessor

def run():
    parser = argparse.ArgumentParser(description="Process Figma JSON files and export SCSS variables.")
    parser.add_argument('directory', type=str, help='The directory containing the Figma JSON files')
    parser.add_argument('--output', type=str, default='output/scss/', help='The output path for the SCSS files')

    args = parser.parse_args()

    processor = MainProcessor(args.directory, args.output)
    processor.main()

if __name__ == "__main__":
    run()
