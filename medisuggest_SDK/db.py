import json
import psycopg2  # PostgreSQL library
import os

class MediSuggest:
    def __init__(self, cache_file="medical_terms.json", db_config=None):
        self.cache_file = cache_file
        self.db_config = db_config if db_config else {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'your_database_name',
            'user': 'your_username',
            'password': 'your_password'
        }
        self.cache = self.load_cache()
        
    def load_cache(self):
        """Load terms from the local cache."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """Save the cache to the local file."""
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=4)

    def connect_db(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            connection = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            return connection
        except Exception as e:
            print("Database connection error:", str(e))
            return None

    def get_terms_from_db(self, query):
        """Fetch terms from the database."""
        connection = self.connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT term FROM medical_terms WHERE term LIKE %s", (f"%{query}%",))
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return [row[0] for row in results]
        return []

    def insert_term_to_db(self, term):
        """Insert a term into the database."""
        connection = self.connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO medical_terms (term) VALUES (%s) ON CONFLICT (term) DO NOTHING", (term,))
            connection.commit()
            cursor.close()
            connection.close()

    def suggest(self, query):
        """Suggest terms from cache and database."""
        terms_from_cache = [term for term in self.cache if query.lower() in term.lower()]
        
        if terms_from_cache:
            return terms_from_cache

        terms_from_db = self.get_terms_from_db(query)
        if terms_from_db:
            return terms_from_db
        
        return []

    def save_term(self, selected_term):
        """Save selected term to both cache and database."""
        self.cache[selected_term] = {"term": selected_term}
        self.save_cache()
        self.insert_term_to_db(selected_term)
