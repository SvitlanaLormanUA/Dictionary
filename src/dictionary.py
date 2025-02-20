
import nltk
from collections import defaultdict
import pickle
from src.word import Word
from src.utils import detect_language

class Dictionary:
    def __init__(self):
        self.dictionary = defaultdict(Word)

    def read_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read()
                language = detect_language(text)
                print(f"Detected language of {file_name}: {language}")
                if language == 'en':
                     text = self.lemmatize_text(text)

                for line in text.splitlines():
                    words = self._split_line(line)
                    for word in words:
                        if word and not self._contains_digit(word):
                            cleaned_word = word.replace("_", "").lower()
                            self.add_word(cleaned_word, file_name)
        except Exception as e:
            print(f"Error reading file: {e}")

    def lemmatize_text(self, text):

        words = nltk.word_tokenize(text)
        lemmatized_words = [nltk.WordNetLemmatizer().lemmatize(word.lower()) for word in words]
        return ' '.join(lemmatized_words)

    def _split_line(self, line):
        return [word for word in line.split() if word.isalpha()]

    def _contains_digit(self, word):
        return any(char.isdigit() for char in word)

    def add_word(self, word, file_name):
        if word not in self.dictionary:
            self.dictionary[word] = Word(word)
        self.dictionary[word].increment_count()
        self.dictionary[word].add_file_occurrence(file_name)

    def save_words_to_file(self, output_file_name):
        sorted_words = sorted(self.dictionary.values(), key=lambda w: w.word)
        try:
            with open(output_file_name, 'w', encoding='utf-8') as file:
                for word in sorted_words:
                    file.write(f"{word.word}: {word.count} {word.get_files()}\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def save_to_binary_file(self, file_name):
        try:
            with open(file_name, 'wb') as file:
                pickle.dump(self, file)
        except Exception as e:
            print(f"Error saving dictionary: {e}")

    @staticmethod
    def load_from_binary_file(file_name):
        try:
            with open(file_name, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return None

    def print_statistics(self):
        total_words = sum(word.count for word in self.dictionary.values())
        print(f"Collection size (Total unique words): {len(self.dictionary)}")
        print(f"Total amount of words: {total_words}")
