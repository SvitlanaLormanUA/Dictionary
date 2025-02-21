import time
import logging
import string
from src.dictionary import Dictionary
from src.DS.incidence_matrix import IncidenceMatrix  
from src.DS.inverted_index import InvertedIndex

def read_file_with_encoding(file_name):
    encodings = ['utf-8', 'latin-1', 'windows-1252'] 
    for encoding in encodings:
        try:
            with open(file_name, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue 
    raise ValueError(f"Unable to decode file {file_name} with tried encodings.")

def clean_word(word):
    word = word.replace("_", "") 
    word = word.strip(string.punctuation) 
    return word.lower() if word and not word.istitle() else word 

def process_file(file_name, dictionary, incidence_matrix, inverted_index):
    try:
        dictionary.read_file(file_name) 
        text = read_file_with_encoding(file_name)
        
        processed_text = dictionary.lemmatize_text(text)
        words = processed_text.split()

        for word in words:
            cleaned_word = clean_word(word)
            if cleaned_word and not any(char.isdigit() for char in cleaned_word):
                incidence_matrix.add_term_document(cleaned_word, file_name)
                inverted_index.add_term_document(cleaned_word, file_name)

    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")

def build_dictionary():
    dictionary = Dictionary()
    files = [
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

    incidence_matrix = IncidenceMatrix()
    inverted_index = InvertedIndex()

    for file in files:
        process_file(file, dictionary, incidence_matrix, inverted_index)

    dictionary.save_words_to_file("dictionary.txt")
    dictionary.save_to_binary_file("dictionary.dat")

    loaded_dict = Dictionary.load_from_binary_file("dictionary.dat")
    if loaded_dict:
        loaded_dict.print_statistics()

    query = "ring OR fellowship"
    perform_boolean_search(query, incidence_matrix, inverted_index)

def perform_boolean_search(query, incidence_matrix, inverted_index):
    print(f"\nBoolean Search Results for query: {query}")
    
    start_time = time.time()
    result_incidence = incidence_matrix.boolean_search(query)
    end_time = time.time()
    print(f"Incidence Matrix Results: {result_incidence}. Search time: {end_time - start_time:.4f} seconds")
    
    start_time = time.time()
    result_inverted = inverted_index.boolean_search(query)
    end_time = time.time()
    print(f"Inverted Index Results: {result_inverted}. Search time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    build_dictionary()
