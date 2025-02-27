from collections import defaultdict
from src.DS.base_ds import BaseIndex
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class PositionalInvertedIndex(BaseIndex):
    def __init__(self):
        super().__init__()
        self.positional_index = defaultdict(self._create_document_dict)

    @staticmethod
    def _create_document_dict():
        return defaultdict(list)

    def add_term_document(self, term, document, position):
        super().add_term_document(term, document)
        self.positional_index[term][document].append(position)

    @staticmethod
    def tokenize_and_clean(text):
        words = word_tokenize(text.lower()) 
        words = [PositionalInvertedIndex.clean_word(word) for word in words]  # Очищаємо слова від пунктуації
        words = [word for word in words if word and word not in stopwords.words('english')]  # Видаляємо стоп-слова
        return words
    
    def phrase_search(self, phrase):
        """
        Шукає точну фразу в документах.
        Повертає множину документів, де фраза зустрічається.
        """
        terms = self.tokenize_and_clean(phrase)
        if not terms:
            return set()
        
    
        first_term = terms[0]
        documents = self.get_documents_for_term(first_term)

        result_docs = set()
        for doc in documents:
            positions = []
            for i, term in enumerate(terms):
                term_positions = self.get_positions_for_term(term, doc)
                if not term_positions:
                    break  # Якщо термін не знайдено, виходимо
                
                if i == 0:
                    positions = term_positions
                else:
                  
                    new_positions = []
                    for pos in term_positions:
                        if pos - 1 in positions:
                            new_positions.append(pos)
                    positions = new_positions
                    if not positions:
                        break 
            else:
                result_docs.add(doc)

        return result_docs

    def phrase_search_with_distance(self, phrase, max_distance=2):
        terms = self.tokenize_and_clean(phrase)
        if not terms:
            return set()
        

        first_term = terms[0]
        documents = self.get_documents_for_term(first_term)

        result_docs = set()
        for doc in documents:
            positions = []
            for i, term in enumerate(terms):
                term_positions = self.get_positions_for_term(term, doc)
                if not term_positions:
                    break  
                
                if i == 0:
                    positions = term_positions
                else:
                 
                    new_positions = []
                    for pos in term_positions:
                        for prev_pos in positions:
                            if 0 < pos - prev_pos <= max_distance:
                                new_positions.append(pos)
                                break
                    positions = new_positions
                    if not positions:
                        break  
            else:
              
                result_docs.add(doc)

        return result_docs

    def get_positions_for_term(self, term, document):
        return self.positional_index.get(term, {}).get(document, [])