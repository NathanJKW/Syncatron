import argparse
import asyncio
import logging
from src.main import main

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the repository puller script.')
    parser.add_argument('--rf', type=int, default=None, help='Run frequency in seconds. Default is 5 seconds.')
    parser.add_argument('--pf', type=str, default=None, help='Path to the project folder. Default is "/default/project/folder".')
    parser.add_argument('--ak', type=str, default=None, help='Access key for git operations. Default is "your_access_key".')

    args = parser.parse_args()
    try:
    # Call the main function with the parsed arguments
        asyncio.run(main(run_frequency=args.rf, project_folder=args.pf, access_key=args.ak))
    except KeyboardInterrupt:
        logging.info("Program interrupted. Exiting gracefully.")