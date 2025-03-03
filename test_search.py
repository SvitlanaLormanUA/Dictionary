import unittest
from src.DS.positional_inverted_index import PositionalInvertedIndex
from src.dictionary import Dictionary
from src.DS.incidence_matrix import IncidenceMatrix
from src.DS.inverted_index import InvertedIndex
from src.DS.biword_index import BiwordIndex
import string


class TestPositionalSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dictionary = Dictionary()
        cls.files = [
            "files/01 - The Fellowship Of The Ring.txt",
            "files/Frenkestein.txt",
            "files/Harry Potter and The Half-Blood Prince.txt",
            "files/Little Women.txt",
            "files/Pride and Prejudice.txt",
            "files/The Adventures of Sherlock Holmes.txt",
            "files/The Great Gatsby.txt",
            "files/Book.txt",
            "files/Moby Dick.txt",
            "files/Drakula.txt"
        ]

        cls.incidence_matrix = IncidenceMatrix()
        cls.inverted_index = InvertedIndex()
        cls.positional_index = PositionalInvertedIndex()
        cls.biword_index = BiwordIndex()

        cls._build_index()

    @classmethod
    def _build_index(cls):
        """Допоміжний метод для створення індексу"""
        for file in cls.files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()

                text = text.translate(str.maketrans('', '', string.punctuation))
                words = text.lower().split()

                for position, word in enumerate(words):
                    cls.incidence_matrix.add_term_document(word, file)
                    cls.inverted_index.add_term_document(word, file)
                    cls.positional_index.add_term_document(word, file, position)

                cls.biword_index.add_document(file, text)

            except Exception as e:
                print(f"Помилка під час обробки файлу {file}: {e}")

    def test_exact_phrase_found(self):
        query = "the great gatsby"
        result = self.positional_index.phrase_search(query)
        self.assertIn("files/The Great Gatsby.txt", result)

    def test_phrase_not_found(self):
        query = "hobbit in hogwarts"
        result = self.positional_index.phrase_search(query)
        self.assertEqual(result, set())

    def test_partial_match_not_returned(self):
        query = "ring fellowship"
        result = self.positional_index.phrase_search(query)
        self.assertEqual(result, set())  # Правильний порядок "fellowship of the ring"

    def test_long_phrase(self):
        query = "it was the best of times it was the worst of times"
        result = self.positional_index.phrase_search(query)
        self.assertTrue(isinstance(result, set))

if __name__ == "__main__":
    unittest.main()
