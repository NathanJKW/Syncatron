import argparse
import logging
from src.main import main

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the repository puller script.')
    parser.add_argument('--rf', type=int, help='Run frequency in seconds.')
    parser.add_argument('--pf', type=str, help='Path to the project folder.')
    parser.add_argument('--ak', type=str, help='Access key for git operations.')
    parser.add_argument('--sr', type=bool, default=True, help='Indicates whether to keep running.')

    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(should_run=args.sr, run_frequency=args.rf, project_folder=args.pf, access_key=args.ak)