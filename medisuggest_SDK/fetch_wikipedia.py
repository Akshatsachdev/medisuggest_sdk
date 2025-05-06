import requests
import spacy
from .utils import save_term

# Load SciSpaCy model
nlp = spacy.load("en_core_sci_sm")

def get_medical_keywords(text):
    """Extract medical keywords using SciSpaCy and TextBlob."""
    if not isinstance(text, str):
        text = str(text)

    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        print(f"[NLP Extracted Entities] {entities}")
        
        keywords = [ent.text for ent in doc.ents if ent.label_]
        print(f"[NLP Extracted Keywords] {keywords}")

        if keywords:
            for kw in keywords:
                print(f"[NER] Extracted: '{kw}'")
                save_term(kw)
            return [str(k) for k in keywords]
        else:
            print("[INFO] No medical terms found by NER.")
            return []
    except Exception as e:
        print(f"[ERROR] spaCy NER failed: {e}")

    # Fallback to TextBlob noun phrases
    blob = TextBlob(text)
    phrases = [str(phrase) for phrase in blob.noun_phrases]
    print(f"[TextBlob Fallback] Extracted phrases: {phrases}")
    return phrases or [text]

def get_wiki_suggestions(query):
    """Fetch medical-related suggestions from Wikipedia."""
    print(f"[QUERY] {query}")
    keywords = get_medical_keywords(query)
    print(f"[EXTRACTED KEYWORDS] {keywords}")

    final_suggestions = set()

    blacklist_keywords = [
        "song", "album", "film", "mixtape", "episode", "band", "character",
        "tv series", "f.c.", "organization", "novel", "book", "movie", "game",
        "fictional", "comics", "soundtrack", "company", "business", "media"
    ]

    for keyword in keywords:
        print(f"[SEARCHING WIKI FOR] {keyword}")
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "opensearch",
                "search": str(keyword),
                "limit": 6,
                "namespace": 0,
                "format": "json"
            }

            res = requests.get(url, params=params, timeout=5)
            res.raise_for_status()

            raw_response = res.json()
            print(f"[WIKI RAW RESPONSE] {raw_response}")

            titles = raw_response[1]
            print(f"[WIKI API RESPONSE] {titles}")

            # Filter non-medical results using blacklist
            filtered_titles = [
                title for title in titles
                if not any(bad in title.lower() for bad in blacklist_keywords)
            ]
            print(f"[WIKI FILTERED TITLES] {filtered_titles}")

            final_suggestions.update(filtered_titles)
        except Exception as e:
            print(f"[ERROR] Wikipedia fetch failed: {e}")

    return list(final_suggestions)
