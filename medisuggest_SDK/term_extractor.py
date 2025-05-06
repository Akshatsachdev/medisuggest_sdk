import spacy

nlp = spacy.load("en_core_sci_sm")

def extract_terms(text):
    """Use SpaCy's model to extract terms from a text."""
    doc = nlp(text)
    terms = [ent.text for ent in doc.ents]
    return terms
