import time
from src.DS.incidence_matrix import IncidenceMatrix  
from src.DS.inverted_index import InvertedIndex
from src.DS.positional_inverted_index import PositionalInvertedIndex
from src.DS.biword_index import BiwordIndex

def load_index_from_file(filename, index_obj, parse_func):
    try:
        with open(filename, "r") as f:
            for line in f:
                parse_func(line, index_obj)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return False
    return True

def parse_incidence_matrix(line, index_obj):
    term, docs = line.strip().split(": ")
    for doc in docs.split(", "):
        index_obj.add_term_document(term, doc)

def parse_inverted_index(line, index_obj):
    term, docs = line.strip().split(": ")
    for doc in docs.split(", "):
        index_obj.add_term_document(term, doc)

def parse_positional_index(line, index_obj):
    if ":" in line and not line.startswith("  "):
        index_obj.current_term = line.strip().split(":")[0]
    elif ":" in line and line.startswith("  "):
        doc, positions = line.strip().split(": ")
        for pos in positions.split(", "):
            index_obj.add_term_document(index_obj.current_term, doc, int(pos))

def parse_biword_index(line, index_obj):
    biword, docs = line.strip().split(": ")
    biword = biword[1:-1].split()
    for doc in docs.split(", "):
        index_obj.add_document(doc, " ".join(biword))

def load_index():
    incidence_matrix = IncidenceMatrix()
    inverted_index = InvertedIndex()
    positional_index = PositionalInvertedIndex()
    biword_index = BiwordIndex()

    if not all([
        load_index_from_file("incidence_matrix.txt", incidence_matrix, parse_incidence_matrix),
        load_index_from_file("inverted_index.txt", inverted_index, parse_inverted_index),
        load_index_from_file("positional_index.txt", positional_index, parse_positional_index),
        load_index_from_file("biword_index.txt", biword_index, parse_biword_index),
    ]):
        return None, None, None, None

    return incidence_matrix, inverted_index, positional_index, biword_index

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

def perform_positional_index_search(query, positional_index):
    print(f"\nPhrase Search Results for query: {query}")

    start_time = time.time()
    result_docs_exact = positional_index.phrase_search(query)  
    end_time = time.time()
    print(f"Exact Phrase Search Results: {result_docs_exact}. Search time: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    result_docs_distance = positional_index.phrase_search_with_distance(query, max_distance=2)
    end_time = time.time()
    print(f"Phrase Search with Distance Results: {result_docs_distance}. Search time: {end_time - start_time:.4f} seconds")

def perform_biword_search(query, biword_index):
    print(f"\nBiword Search Results for query: {query}")

    start_time = time.time()
    result_biword = biword_index.search_phrase(query)
    end_time = time.time()
    
    if result_biword:
        print(f"Biword Search Results: {result_biword}. Search time: {end_time - start_time:.4f} seconds")
    else:
        print(f"No documents found for query: {query}. Search time: {end_time - start_time:.4f} seconds")

def main():
    indices = load_index()
    if any(index is None for index in indices):
        print("Unable to load indices. Exiting...")
        exit()
    incidence_matrix, inverted_index, positional_index, biword_index = indices

    while True:
        search_type = input(
            "Choose search type:\n"
            "1. Boolean Search\n"
            "2. Phrase Search\n"
            "3. Biword Search\n"
            "4. Exit\n"
            "Enter your choice (1/2/3/4): "
        ).strip()

        if search_type == "4":
            print("Exiting...")
            break

        query = input("Enter your query for search: ").strip()

        if search_type == "1":
            perform_boolean_search(query, incidence_matrix, inverted_index)
        elif search_type == "2":
            perform_positional_index_search(query, positional_index)
        elif search_type == "3":
            perform_biword_search(query, biword_index)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

