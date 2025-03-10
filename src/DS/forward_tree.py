import logging
from fnmatch import fnmatchcase

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = {}

    def add_child(self, child_value):
        if child_value not in self.children:
            self.children[child_value] = TreeNode(child_value)
    
    def __str__(self, level=0):
        result = "  " * level + f"{self.value}\n"
        for child in self.children.values():
            result += child.__str__(level + 1)
        return result

class ForwardTree:
    def __init__(self):
        self.root = TreeNode("Root")
        self.current_term = None  # For parsing purposes

    def add_term_document(self, term, document):
        if term not in self.root.children:
            self.root.add_child(term)
        self.root.children[term].add_child(document)

    def add_document(self, document, term):
        """Alternative method for adding documents during parsing"""
        self.add_term_document(term, document)

    def search(self, query):
        if not self.root:
            return []
        results = []

        # Handle wildcard-only query: return all documents under all terms
        if query == "*":
            for term_node in self.root.children:
                results.extend([child.value for child in term_node.children])
            return results

        # Handle queries with wildcards (e.g., "lord*")
        if "*" in query:
            query_prefix = query.rstrip("*").lstrip("*")  # Remove leading/trailing *
            if query.startswith("*") and query.endswith("*"):
                # Middle match (e.g., "*or*") - not very useful here, but possible
                for term_node in self.root.children:
                    if query_prefix in term_node.value:
                        results.extend([child.value for child in term_node.children])
            elif query.endswith("*"):
                # Prefix match (e.g., "lord*")
                for term_node in self.root.children:
                    if term_node.value.startswith(query_prefix):
                        results.extend([child.value for child in term_node.children])
            elif query.startswith("*"):
                # Suffix match (e.g., "*ing")
                for term_node in self.root.children:
                    if term_node.value.endswith(query_prefix):
                        results.extend([child.value for child in term_node.children])
        else:
            # Exact match (original behavior)
            for term_node in self.root.children:
                if term_node.value == query:
                    results.extend([child.value for child in term_node.children])

        return results

    def __str__(self):
        return str(self.root)

    def save_to_file(self, filename):
        """Save the forward tree to a file"""
        with open(filename, "w") as f:
            data = str(self)
            if not data.strip():
                logging.warning("ForwardTree is empty. Nothing to save.")
            f.write(data)
