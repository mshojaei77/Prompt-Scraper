#addsubject.py

import csv
import spacy
import nltk
from nltk import pos_tag, RegexpParser
from nltk.tokenize import word_tokenize

# Download NLTK data (only needed once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define a list of entity labels relevant to image generation prompts
relevant_entity_labels = ["PERSON", "ORG", "GPE", "PRODUCT", "WORK_OF_ART", "FAC", "LOC", "EVENT", "ANIMAL", "CREATURE"]

input_csv_path = 'partial_prompt_texts.csv'
output_csv_path = 'prompts_with_subject.csv'

# Read the input CSV file
print(f"Reading input CSV file: {input_csv_path}")
with open(input_csv_path, 'r', encoding='utf-8') as input_csv:
    reader = csv.reader(input_csv)

    # Skip header if it exists
    header = next(reader, None)

    # Process the data and create a new list of dictionaries
    output_data = []
    for row in reader:
        prompt = row[0]  # Assuming the prompt text is in the first column

        # Use spaCy to extract relevant entities
        doc = nlp(prompt)
        relevant_entities = [ent.text for ent in doc.ents if ent.label_ in relevant_entity_labels]

        # Use NLTK to extract all nouns as potential main subjects if no relevant entities found
        if not relevant_entities:
            tokens = word_tokenize(prompt)
            pos_tags = pos_tag(tokens)
            
            # Define a grammar to capture all nouns
            grammar = "NP: {<NN.*>+}"
            chunk_parser = RegexpParser(grammar)
            
            # Apply the parser to the part-of-speech tagged tokens
            tree = chunk_parser.parse(pos_tags)
            
            # Extract all noun phrases
            all_nouns = [' '.join([token for token, pos in subtree.leaves()]) for subtree in tree.subtrees() if subtree.label() == 'NP']

            # Use the first noun phrase as the main subject, or "No Subject" if none found
            main_subject = all_nouns[0] if all_nouns else "No Subject"
        else:
            # Use the first relevant entity as the main subject
            main_subject = relevant_entities[0]

        # Replace "subject" with the main subject
        transformed_prompt = prompt.replace("subject", main_subject)

        output_data.append({'subject': main_subject, 'prompt': transformed_prompt})

        print(f"Main subject identified: {main_subject}")

# Write the processed data to a new CSV file
fieldnames = ['subject', 'prompt']

print(f"Writing output CSV file: {output_csv_path}")
with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    writer.writerows(output_data)

print(f"CSV data has been transformed and saved to {output_csv_path}.")
