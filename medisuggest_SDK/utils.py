import json
import os

TERMS_FILE = "medical_terms.json"

def load_local_terms(file_path=TERMS_FILE):
    """Load terms from a local JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)  # Returns loaded terms if valid
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to decode JSON from {file_path}. Returning empty list.")
            return []  # Return an empty list if JSON is invalid
    return []  # Return empty list if file doesn't exist

def save_term(term, file_path=TERMS_FILE):
    """Save a new term to the local JSON file if it doesn't already exist."""
    terms = load_local_terms(file_path)
    
    # Ensure terms is a list, even if something went wrong with the file
    if not isinstance(terms, list):
        print(f"[ERROR] Expected a list but got {type(terms)}. Initializing a new list.")
        terms = []

    # If term does not already exist in the list, add it
    if term not in terms:
        terms.append(term)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(terms, f, indent=2)
            print(f"[SAVED] '{term}' added to {file_path}.")
        except IOError as e:
            print(f"[ERROR] Failed to write to {file_path}: {e}")
    else:
        print(f"[INFO] Term '{term}' already exists in {file_path}.")
