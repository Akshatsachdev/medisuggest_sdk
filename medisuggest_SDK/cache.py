import json
import os

class Cache:
    def __init__(self, cache_file="medical_terms.json"):
        """Initialize the cache from a file or create a new cache."""
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Load the cache from the file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                try:
                    # Try to load the cache file as JSON
                    loaded_cache = json.load(f)
                    # Check if the loaded cache is a dictionary, else reset to an empty dict
                    if isinstance(loaded_cache, dict):
                        return loaded_cache
                    else:
                        print(f"[ERROR] Cache loaded is not a dictionary. Resetting cache.")
                        return {}
                except json.JSONDecodeError:
                    print(f"[ERROR] Failed to load JSON from {self.cache_file}. Returning empty dictionary.")
                    return {}
        return {}

    def save_cache(self):
        """Save the current cache to the file."""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)
            print(f"[CACHE] Saved to {self.cache_file}")

    def get(self, key):
        """Get a value from the cache."""
        if isinstance(self.cache, dict):  # Ensure it's a dictionary
            return self.cache.get(key, None)
        print(f"[ERROR] Cache is not a dictionary: {self.cache}")
        return None

    def set(self, key, value):
        """Set a value in the cache."""
        if isinstance(self.cache, dict):  # Ensure it's a dictionary
            self.cache[key] = value
            self.save_cache()
        else:
            print(f"[ERROR] Cache is not a dictionary: {self.cache}")
