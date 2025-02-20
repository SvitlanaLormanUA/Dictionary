
from src.dictionary import Dictionary 

if __name__ == "__main__":
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
    
    for file in files:
        dictionary.read_file(file)
    
    dictionary.save_words_to_file("dictionary.txt")
    dictionary.save_to_binary_file("dictionary.dat")

    loaded_dict = Dictionary.load_from_binary_file("dictionary.dat")
    if loaded_dict:
        loaded_dict.print_statistics()
