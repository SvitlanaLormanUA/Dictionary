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

    def add_term_document(self, term, document):
        if term not in self.root.children:
            self.root.add_child(term)
        self.root.children[term].add_child(document)

    def search(self, pattern):
        results = {}
        for term, term_node in self.root.children.items():
            if fnmatchcase(term, pattern):  
                results[term] = list(term_node.children.keys())
        return results

    def __str__(self):
        return str(self.root)

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            data = str(self)
            if not data.strip():
                logging.warning("ForwardTree is empty. Nothing to save.")
            f.write(data)