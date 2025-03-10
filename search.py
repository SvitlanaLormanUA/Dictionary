import time
from src.DS.incidence_matrix import IncidenceMatrix  
from src.DS.inverted_index import InvertedIndex
from src.DS.positional_inverted_index import PositionalInvertedIndex
from src.DS.biword_index import BiwordIndex
from src.DS.forward_tree import ForwardTree, TreeNode

def load_index_from_file(filename, index_obj, parse_func):
    try:
        with open(filename, "r") as f:
            for line in f:
                parse_func(line, index_obj)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return False
    return True

def parse_forward_tree(line, index_obj):
    line = line.rstrip()  # Remove trailing whitespace/newlines
    if line == "Root":
        index_obj.root = TreeNode("Root")
        index_obj.current_term_node = None  
    elif line.startswith("  ") and not line.startswith("    "):
        # Term level (2 spaces): Create a new TreeNode under Root
        term = line.strip()
        new_node = TreeNode(term)
        index_obj.root.add_child(new_node)
        index_obj.current_term_node = new_node  # Track the current term node
    elif line.startswith("    "):
        # Document level (4 spaces): Add document to the current term node
        doc_path = line.strip()
        if index_obj.current_term_node:
            index_obj.current_term_node.add_child(TreeNode(doc_path))
        else:
            print(f"Error: Document '{doc_path}' found before any term.")

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
    forward_tree = ForwardTree()

    if not all([
        load_index_from_file("incidence_matrix.txt", incidence_matrix, parse_incidence_matrix),
        load_index_from_file("inverted_index.txt", inverted_index, parse_inverted_index),
        load_index_from_file("positional_index.txt", positional_index, parse_positional_index),
        load_index_from_file("biword_index.txt", biword_index, parse_biword_index),
        load_index_from_file("forward_tree.txt", forward_tree, parse_forward_tree),
    ]):
        return None, None, None, None

    return incidence_matrix, inverted_index, positional_index, biword_index, forward_tree


def  perform_forward_tree_search(query, forward_tree):
    print(f"\nForward Tree Search Results for query: {query}")

    start_time = time.time()
    result_forward = forward_tree.search(query)
    end_time = time.time()
    
    if result_forward:
        print(f"Forward Tree Search Results: {result_forward}. Search time: {end_time - start_time:.4f} seconds")
    else:
        print(f"No documents found for query: {query}. Search time: {end_time - start_time:.4f} seconds")

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

    print("As was discussed on the lecture, realisation of phrase search with distance on positional index is impossible :)")

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
    incidence_matrix, inverted_index, positional_index, biword_index, forward_tree = indices

    while True:
        search_type = input(
            "Choose search type:\n"
            "1. Boolean Search\n"
            "2. Phrase Search\n"
            "3. Biword Search\n"
            "4. Forward Tree\n"
            "0. Exit\n"
            "Enter your choice (0/1/2/3/4): "
        ).strip()

        if search_type == "0":
            print("Exiting...")
            break

        query = input("Enter your query for search: ").strip()

        if search_type == "1":
            perform_boolean_search(query, incidence_matrix, inverted_index)
        elif search_type == "2":
            perform_positional_index_search(query, positional_index)
        elif search_type == "3":
            perform_biword_search(query, biword_index)
        elif search_type == "4":
            perform_forward_tree_search(query, forward_tree)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
