from .cache import Cache
import spacy
from .utils import save_term
import wikipedia
import requests


class MediSuggest:
    def __init__(self, cache_file="medical_terms.json"):
        self.nlp = spacy.load("en_core_sci_sm")
        self.cache = Cache(cache_file)

    def get_medical_terms(self, text):
        cached_terms = self.cache.get(text)
        if cached_terms:
            print(f"[CACHE] Found terms in cache: {cached_terms}")
            return cached_terms

        doc = self.nlp(text)
        print(f"[NLP Entities] Detected entities:")
        for ent in doc.ents:
            print(f"Entity: {ent.text}, Label: {ent.label_}")

        # Relaxed condition to include any labeled entity
        terms = [ent.text for ent in doc.ents if ent.label_]

        if not terms:
            print(f"[INFO] No medical terms found, trying Wikipedia fallback.")
            try:
                summary = wikipedia.summary(text, sentences=1)
                terms = self.extract_terms_from_wikipedia(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                summary = wikipedia.summary(e.options[0], sentences=1)
                terms = self.extract_terms_from_wikipedia(summary)

        for term in terms:
            save_term(term)

        self.cache.set(text, terms)
        print(f"[CACHE] Saved terms to cache: {terms}")
        return terms

    def extract_terms_from_wikipedia(self, summary):
        doc = self.nlp(summary)
        return [ent.text for ent in doc.ents if ent.label_]

    def suggest(self, query):
        medical_terms = self.get_medical_terms(query)
        wiki_suggestions = self.get_wiki_suggestions(query)

        all_suggestions = list(set(medical_terms + wiki_suggestions))
        return [{"term": suggestion} for suggestion in all_suggestions]

    def get_wiki_suggestions(self, query):
        print(f"[QUERY] {query}")
        keywords = [query]  # Use raw query only to avoid recursion
        final_suggestions = set()

        blacklist_keywords = ["song", "album", "film", "mixtape", "episode", "band", "character"]

        for keyword in keywords:
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

                print(f"[WIKI REQUEST] {res.url}")
                raw_response = res.json()
                print(f"[WIKI RAW RESPONSE] {raw_response}")

                titles = raw_response[1]
                filtered_titles = [
                    title for title in titles
                    if not any(bad in title.lower() for bad in blacklist_keywords)
                ]
                print(f"[WIKI FILTERED TITLES] {filtered_titles}")

                final_suggestions.update(filtered_titles)
            except Exception as e:
                print(f"[ERROR] Wikipedia fetch failed: {e}")

        print(f"[WIKI SUGGESTIONS] {final_suggestions}")
        return list(final_suggestions)
