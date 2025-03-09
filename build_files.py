import logging
import string

from src.dictionary import Dictionary
from src.DS.incidence_matrix import IncidenceMatrix  
from src.DS.inverted_index import InvertedIndex
from src.DS.positional_inverted_index import PositionalInvertedIndex
from src.DS.biword_index import BiwordIndex
from src.DS.forward_tree import ForwardTree

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

def process_file_for_incidence_matrix(file_name, incidence_matrix, words):
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word and not any(char.isdigit() for char in cleaned_word):
            incidence_matrix.add_term_document(cleaned_word, file_name)

def process_file_for_inverted_index(file_name, inverted_index, words):
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word and not any(char.isdigit() for char in cleaned_word):
            inverted_index.add_term_document(cleaned_word, file_name)

def process_file_for_positional_index(file_name, positional_index, words):
    for position, word in enumerate(words):
        cleaned_word = clean_word(word)
        if cleaned_word and not any(char.isdigit() for char in cleaned_word):
            positional_index.add_term_document(cleaned_word, file_name, position)

def process_file_for_biword_index(file_name, biword_index, processed_text):
    biword_index.add_document(file_name, processed_text)

def process_file_for_forward_tree(file_name, forward_tree, words):
    for word in words:
        cleaned_word = clean_word(word)
        if cleaned_word and not any(char.isdigit() for char in cleaned_word):
            forward_tree.add_term_document(cleaned_word, file_name)

def process_file(file_name, dictionary):
    try:
        dictionary.read_file(file_name) 
        text = read_file_with_encoding(file_name)
        text = text.translate(str.maketrans('', '', string.punctuation))
        processed_text = dictionary.lemmatize_text(text)
        words = processed_text.split()
        return processed_text, words 
    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
        return None, None

def build_index():
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
    positional_index = PositionalInvertedIndex()
    biword_index = BiwordIndex()
    forward_tree = ForwardTree()

    for file in files:
        processed_text, words = process_file(file, dictionary)
        if words is not None:  # Only process if file was read successfully
            process_file_for_incidence_matrix(file, incidence_matrix, words)
            process_file_for_inverted_index(file, inverted_index, words)
            process_file_for_positional_index(file, positional_index, words)
            process_file_for_biword_index(file, biword_index, processed_text)
            process_file_for_forward_tree(file, forward_tree, words)

    dictionary.save_words_to_file("dictionary.txt")
    dictionary.save_to_binary_file("dictionary.dat")

    with open("incidence_matrix.txt", "w") as f:
        for term, docs in incidence_matrix.index.items():
            f.write(f"{term}: {', '.join(docs)}\n")

    with open("inverted_index.txt", "w") as f:
        for term, docs in inverted_index.index.items():
            f.write(f"{term}: {', '.join(docs)}\n")

    with open("positional_index.txt", "w") as f:
        for term, doc_positions in positional_index.positional_index.items():
            f.write(f"{term}:\n")
            for doc, positions in doc_positions.items():
                f.write(f"  {doc}: {', '.join(map(str, positions))}\n")

    biword_index.save_to_file("biword_index.txt")
    forward_tree.save_to_file("forward_tree.txt")
   
    print("Index building completed. Now we can search :_).")

    print("Forward Tree (Terms -> Documents):")
    print(forward_tree)

    print("\nForward Tree Search Examples:")
    print("Exact search 'the':", forward_tree.search("the"))
    print("Wildcard 'run*':", forward_tree.search("run*"))
    print("Wildcard '*ing':", forward_tree.search("*ing"))

if __name__ == "__main__":
    build_index()