import nltk
import ast
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.DS.base_ds import BaseIndex

import time
nltk.download("punkt")
nltk.download("stopwords")

class BiwordIndex(BaseIndex):
    def __init__(self):
        super().__init__()
        self.positions = {}

    def add_document(self, document_name, text):
        """Add a document to the biword index."""
        words = self.tokenize_and_clean(text)
        for i in range(len(words) - 1):
            biword = (words[i], words[i + 1])
            self.add_term_document(biword, document_name)
            
            if biword not in self.positions:
                self.positions[biword] = {}
            if document_name not in self.positions[biword]:
                self.positions[biword][document_name] = []
            self.positions[biword][document_name].append(i)

    @staticmethod
    def tokenize_and_clean(text):
        """Tokenize and clean the text."""
        words = word_tokenize(text.lower())  # Приводимо все до нижнього регістру
        words = [word for word in words if word.isalnum()]
        words = [word for word in words if word not in stopwords.words('english')]
        return words

    def phrase_search(self, phrase):
        """Search for an exact phrase in the documents."""
        terms = self.tokenize_and_clean(phrase)
        if len(terms) < 2:
            return set()

        biword_pairs = [(terms[i], terms[i + 1]) for i in range(len(terms) - 1)]

        result_docs = None
        for biword in biword_pairs:
            docs = self.get_documents_for_term(biword)
            print(f"Searching for biword: {biword}, found in: {docs}")
            if docs:
                if result_docs is None:
                    result_docs = docs.copy()
                else:
                    result_docs &= docs
            else:
                return set()
        return result_docs if result_docs else set()


def parse_biword_index(line, index_obj):
    """Properly parse biword index from file."""
    try:
        biword, docs = line.strip().split(": ")
        biword = ast.literal_eval(biword)  # Правильний парсинг кортежу
        for doc in docs.split(", "):
            index_obj.add_term_document(biword, doc)
    except ValueError:
        print(f"Error parsing line: {line}")

# Оновлення функції perform_biword_search
def perform_biword_search(query, biword_index):
    print(f"\nBiword Search Results for query: {query}")

    query_terms = query.split()
    if len(query_terms) < 2:
        print("Query must contain at least two words.")
        return
    
    query_tuple = tuple(query_terms[:2])

    start_time = time.time()
    result_biword = biword_index.phrase_search(" ".join(query_tuple))
    end_time = time.time()
    print(f"Biword Search Results: {result_biword}. Search time: {end_time - start_time:.4f} seconds")
