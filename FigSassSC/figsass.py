import argparse
from contract.main_processor import MainProcessor

def run():
    parser = argparse.ArgumentParser(description="Process Figma JSON files and export SCSS variables.")
    parser.add_argument('directory', type=str, help='The directory containing the Figma JSON files')
    parser.add_argument('--output', type=str, default='output/scss/', help='The output path for the SCSS files')
    parser.add_argument('--estimate-cpu', action='store_true', help='Estimate the CPU effort for processing the files')
    parser.add_argument('--filename', type=str, help='The JSON file name to estimate CPU effort', default='sample.json')

    args = parser.parse_args()

    processor = MainProcessor(args.directory, args.output)

    if args.estimate_cpu:
        processor.estimate_total_cpu_effort(args.filename)
    else:
        processor.main()

if __name__ == "__main__":
    run()
