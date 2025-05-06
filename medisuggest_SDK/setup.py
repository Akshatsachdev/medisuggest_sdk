from setuptools import setup, find_packages

# Try to read the README file for long description
try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Long description not available."

setup(
    name="medisuggest_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'spacy==3.0.6',  # Specify version for better control
        'textblob==0.18.0',
        'wikipedia==1.4.0',
        'psycopg2-binary==2.9.5',  # Updated for compatibility with psycopg2
    ],
    extras_require={
        'dev': [
            'pytest',  # For testing
            'mock',    # For mocking in tests
        ]
    },
    tests_require=[
        'pytest',
    ],
    author="Akshat Sachdeva",
    author_email="sachdevaakshat2003@gmail.com",
    description="A Python SDK for medical term extraction and suggestion.",
    long_description=long_description,  # Read the README for the long description
    long_description_content_type="text/markdown",
    url="https://github.com/AkshatSachdeva/medisuggest_sdk",  # Your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
