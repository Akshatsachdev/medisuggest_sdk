# MediSuggest SDK

`medisuggest_sdk` is a Python SDK for suggesting and extracting medical terms from text using Natural Language Processing (NLP) techniques. It uses **SciSpaCy** for extracting medical entities, integrates with **Wikipedia** for term suggestions, and allows caching of terms for efficient reuse.

## Features

* **Medical Term Extraction**: Extract medical terms from text using SciSpaCy.
* **Wikipedia Integration**: Fetch medical-related suggestions from Wikipedia for terms that are not in the local cache.
* **Local Caching**: Save terms to a local JSON file to avoid redundant processing.
* **PostgreSQL Database Integration**: Store terms in a PostgreSQL database for persistent storage.

## Installation

You can install `medisuggest_sdk` via `pip` directly from PyPI:

```bash
pip install medisuggest-sdk
```

Or, if you want to install from the source, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/medisuggest_sdk.git
   cd medisuggest_sdk
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Requirements

* Python 3.6 or higher
* `spacy` and `scispacy` for NLP processing
* `requests` for making API calls to Wikipedia
* `psycopg2-binary` for PostgreSQL database support

## Usage

### Initialize the SDK

To start using the SDK, you need to initialize the `MediSuggest` class:

```python
from medisuggest_sdk import MediSuggest

# Initialize the SDK
medisuggest = MediSuggest()

# Example usage: Extracting medical terms from a text
text = "The patient was diagnosed with hypertension and diabetes."
medical_terms = medisuggest.get_medical_terms(text)

print(medical_terms)
```

### Suggest Medical Terms

To get medical term suggestions from a query, use the `suggest` method:

```python
# Suggest terms related to a query
query = "heart disease"
suggestions = medisuggest.suggest(query)

for suggestion in suggestions:
    print(suggestion)
```

### Caching Terms

The SDK automatically caches terms in a local file (`medical_terms.json`). If you want to manage the cache manually, use the following methods:

* `load_cache()`: Load terms from the cache file.
* `save_cache()`: Save terms to the cache.

### Working with PostgreSQL

The SDK supports integrating with a PostgreSQL database. Make sure to configure your database settings in the `db.py` file before using it.

## Testing

To test the SDK, you can run the test suite. The tests are located in the `test/` directory.

1. Ensure that you have all dependencies installed:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:

   ```bash
   pytest test/
   ```

## Contributing

If you would like to contribute to the project, please fork the repository and create a pull request with your changes. Ensure that your code passes all tests and adheres to the coding style guidelines.

### How to Contribute

1. Fork the repository on GitHub.
2. Create a new branch for your feature or fix.
3. Make your changes.
4. Commit your changes with meaningful commit messages.
5. Push to your forked repository.
6. Open a pull request from your fork to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE].

---