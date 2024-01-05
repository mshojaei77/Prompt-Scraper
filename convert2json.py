#convert2json.py

import csv
import json

def convert_csv_to_json(csv_file_path, json_file_path):
    # Open and read the CSV file with specified encoding (UTF-8)
    with open(csv_file_path, 'r', encoding='utf-8', newline='') as csv_file:
        # Read the first line and clean up header names from leading/trailing whitespaces
        header = csv_file.readline().strip().split(',')
        header = [col.strip() for col in header]
        csv_reader = csv.DictReader(csv_file, fieldnames=header)
        data = list(csv_reader)

    # Create a list to store the formatted JSON data
    json_data = []

    # Iterate through each row in the CSV and create JSON structure
    for row in data:
        subject = row['subject']
        prompt = row['prompt']

        # Remove double quotes from the beginning and end of the 'prompt' content and strip any extra spaces
        prompt = prompt.replace('"', '').strip()

        # Create the JSON structure for each subject and prompt
        message = {
            "messages": [
                {"role": "system", "content": "You are a fine-tuned assistant designed to translate user input into optimized Midjourney prompts."},
                {"role": "user", "content": f"{subject}"},
                {"role": "assistant", "content": f"{prompt}"}  # Use the modified prompt
            ]
        }

        # Append the JSON structure to the list
        json_data.append(message)

    # Write the formatted JSON data to a file with specified encoding (UTF-8)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        for entry in json_data:
            json.dump(entry, json_file, ensure_ascii=False)
            json_file.write('\n')

# Example usage with the provided CSV data
csv_file_path = r'prompts_with_subject.csv'  # Replace with your CSV file path
json_file_path = r'prompts_with_subject.jsonl'  # Replace with your desired JSON file path
convert_csv_to_json(csv_file_path, json_file_path)
