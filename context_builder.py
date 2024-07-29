import os
import logging
import argparse
from typing import List

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file_lines(file_path: str) -> List[str]:
    """Reads lines from a file and returns a list of file paths."""
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            logging.info(f'Read {len(lines)} lines from {file_path}')
            return lines
    except Exception as e:
        logging.error(f'Failed to read file {file_path}: {e}')
        return []

def extract_file_content(file_path: str) -> str:
    """Extracts the content of a given file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            logging.info(f'Extracted content from {file_path}')
            return content
    except Exception as e:
        logging.error(f'Failed to read file {file_path}: {e}')
        return ""

def write_markdown_file(output_path: str, file_data: List[str]) -> None:
    """Writes the collected file data into the markdown file."""
    try:
        with open(output_path, 'w') as markdown_file:
            for file_info in file_data:
                markdown_file.write(file_info + "\n")  # Add a newline after each file block
            logging.info(f'Wrote markdown file {output_path}')
    except Exception as e:
        logging.error(f'Failed to write to markdown file {output_path}: {e}')

def generate_markdown_from_files(input_file: str, output_file: str) -> None:
    """Generates markdown content from a list of files given in an input file."""
    file_lines = read_file_lines(input_file)
    file_data = []

    for file_path in file_lines:
        # Resolve the relative path
        resolved_path = os.path.abspath(file_path)  # Convert to absolute path
        if os.path.isfile(resolved_path):  # Input validation for file existence
            content = extract_file_content(resolved_path)
            file_data.append(f"{file_path}\n```python\n{content}\n```\n")
        else:
            logging.warning(f'File does not exist: {file_path}')

    write_markdown_file(output_file, file_data)

def main():
    """Main function to run the script."""
    # Setting up argument parser
    parser = argparse.ArgumentParser(description='Generate markdown from list of file paths.')
    parser.add_argument('input_file', type=str, help='Path to the input text file containing list of file paths.')
    parser.add_argument('output_file', type=str, help='Path to the output markdown file.')

    args = parser.parse_args()

    generate_markdown_from_files(args.input_file, args.output_file)

if __name__ == '__main__':
    main()