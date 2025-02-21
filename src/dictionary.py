import nltk
import string
from collections import defaultdict
import pickle
from src.word import Word
from src.utils import detect_language

class Dictionary:
    def __init__(self):
        self.dictionary = defaultdict(Word)
        self.lemmatizer = nltk.WordNetLemmatizer()

    def read_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read()
                language = detect_language(text)
                print(f"Detected language of {file_name}: {language}")
                if language == 'en':
                    text = self.lemmatize_text(text)  # Лематизація + NER

                for line in text.splitlines():
                    words = self._split_line(line)
                    for word in words:
                        cleaned_word = self._clean_word(word) 
                        if cleaned_word and not self._contains_digit(cleaned_word):
                            self.add_word(cleaned_word, file_name)
        except Exception as e:
            print(f"Error reading file: {e}")

    def lemmatize_text(self, text):
        words = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        named_entities = nltk.ne_chunk(pos_tags, binary=False)

        lemmatized_words = []
        named_entity_words = set()

        for chunk in named_entities:
            if hasattr(chunk, 'label'):  
                entity = " ".join(c[0] for c in chunk) 
                named_entity_words.add(entity) 
                lemmatized_words.append(entity)  
            else:
                word = chunk[0]
                lemmatized_word = self.lemmatize_word(word.lower())  
                lemmatized_words.append(lemmatized_word)

        return ' '.join(lemmatized_words)

    def lemmatize_word(self, word):
        return self.lemmatizer.lemmatize(word)

    def _split_line(self, line):
        return nltk.word_tokenize(line)

    def _clean_word(self, word):
        word = word.replace("_", "")  
        word = word.strip(string.punctuation)  
        return word

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
