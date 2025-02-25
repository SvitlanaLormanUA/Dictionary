import pickle
import time


def load_index():
    try:
        with open("incidence_matrix.pkl", "rb") as f:
            incidence_matrix = pickle.load(f)

        with open("inverted_index.pkl", "rb") as f:
            inverted_index = pickle.load(f)

        return incidence_matrix, inverted_index
    except FileNotFoundError:
        print("Error: Index files not found. Run `build_index.py` first.")
        exit()

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
    incidence_matrix, inverted_index = load_index()

    while True:
        query = input("Enter your query for search (or 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            break
        perform_boolean_search(query, incidence_matrix, inverted_index)
