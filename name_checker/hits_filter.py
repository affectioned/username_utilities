# Python program to filter out OG words based on specific criteria
import os
import string

def is_og_word(word):
    # Check if the word is a single dictionary-like word without prefixes, suffixes, numbers, or underscores
    if any(char.isdigit() or char in string.punctuation for char in word):
        return False

    # Further filter to ensure no prefixes or suffixes
    suffixes = ["ing", "ed", "s"]
    prefixes = ["un", "re", "pre"]  # Add more prefixes as needed

    if any(word.startswith(prefix) for prefix in prefixes):
        return False
    if any(word.endswith(suffix) for suffix in suffixes):
        return False

    # Word should not contain spaces and must be alphabetical
    return word.isalpha()

def filter_words(input_file):
    try:
        # Define output file name in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, "filtered_hits.txt")

        # Read the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Process only the word before the '|' character
        filtered_words = []
        for line in lines:
            if '|' in line:
                word = line.split('|')[0].strip()
                if is_og_word(word.lower()):
                    filtered_words.append(line.strip())

        # Write the filtered lines to the output file
        with open(output_file, 'w') as file:
            file.write("\n".join(filtered_words))

        print(f"Filtered words saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = input("Enter the path to the input .txt file: ").strip()
    filter_words(input_file)