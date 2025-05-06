import unittest
from medisuggest_sdk.main import MediSuggest
from medisuggest_sdk.cache import Cache
from unittest.mock import patch

class TestMediSuggest(unittest.TestCase):

    @patch('medisuggest_sdk.cache.Cache.get')
    def test_get_medical_terms_cache(self, mock_get):
        # Mock the cache to return a predefined term
        mock_get.return_value = ['Aspirin', 'Ibuprofen']

        medi_suggest = MediSuggest(cache_file="mock_cache.json")
        terms = medi_suggest.get_medical_terms("Aspirin is a common painkiller.")
        
        self.assertEqual(terms, ['Aspirin', 'Ibuprofen'])
        mock_get.assert_called_once_with("Aspirin is a common painkiller.")

    @patch('medisuggest_sdk.cache.Cache.get')
    @patch('medisuggest_sdk.fetch_wikipedia.get_wiki_suggestions')
    def test_get_medical_terms_fallback(self, mock_get_wiki_suggestions, mock_get_cache):
        # Mock Cache to return None (indicating a cache miss)
        mock_get_cache.return_value = None
        # Mock Wikipedia suggestion
        mock_get_wiki_suggestions.return_value = ['Aspirin', 'Paracetamol']
        
        medi_suggest = MediSuggest(cache_file="mock_cache.json")
        terms = medi_suggest.get_medical_terms("A common painkiller.")
        
        # Ensure Wikipedia suggestions are fetched
        self.assertEqual(terms, ['Aspirin', 'Paracetamol'])
        mock_get_wiki_suggestions.assert_called_once_with("A common painkiller.")
    
    @patch('medisuggest_sdk.db.MediSuggest.get_terms_from_db')
    def test_db_fallback(self, mock_db):
        # Mock DB call to return specific terms
        mock_db.return_value = ['Aspirin']

        medi_suggest = MediSuggest(cache_file="mock_cache.json")
        terms = medi_suggest.suggest("Aspirin")
        
        self.assertEqual(terms, ['Aspirin'])
        mock_db.assert_called_once_with('Aspirin')

if __name__ == "__main__":
    unittest.main()
