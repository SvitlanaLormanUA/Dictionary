from src.DS.base_ds import BaseIndex
from collections import defaultdict

class IncidenceMatrix(BaseIndex):
    def __init__(self):
        super().__init__()
        self.terms = set()
        self.documents = set()
        self.index = defaultdict(dict)  

    def add_term_document(self, term, document):
        self.terms.add(term)
        self.documents.add(document)
        self.index[term][document] = 1

    def get_documents_for_term(self, term):
        return set(self.index.get(term, {}).keys())
