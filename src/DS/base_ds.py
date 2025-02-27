
from collections import defaultdict
import re
import string

class BaseIndex:
    def __init__(self):
        self.index = defaultdict(set)

    def add_term_document(self, term, document):
        self.index[term].add(document)

    def boolean_search(self, query):
        query = query.replace("(", " ( ").replace(")", " ) ")
        tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\s+NOT\s+|\s*\(\s*|\s*\)\s*)', query)
        tokens = [token.strip() for token in tokens if token.strip()]

        stack = []
        operator = None

        for token in tokens:
            if token in {'AND', 'OR', 'NOT'}:
                operator = token
            elif token == '(':
                stack.append('(')
            elif token == ')':
                temp_stack = []
                while stack and stack[-1] != '(':
                    temp_stack.insert(0, stack.pop())
                stack.pop()  
                stack.append(self.apply_operator(temp_stack))  
            else:
                docs = self.get_documents_for_term(token)
                if operator == 'AND':
                    stack.append(stack.pop() & docs)  
                elif operator == 'OR':
                    stack.append(stack.pop() | docs)  
                elif operator == 'NOT':
                    stack.append(stack.pop() - docs)  
                else:
                    stack.append(docs)  

        return stack[0] if stack else set()
    def clean_word(word):
        word = word.replace("_", "") 
        word = word.strip(string.punctuation) 
        return word.lower() if word and not word.istitle() else word 
    def apply_operator(self, terms):
        result = terms[0]
        for i in range(1, len(terms), 2):
            operator = terms[i]
            term = terms[i + 1]
            if operator == 'AND':
                result &= term
            elif operator == 'OR':
                result |= term
            elif operator == 'NOT':
                result -= term
        return result


    def get_documents_for_term(self, term):
        return self.index.get(term, set())