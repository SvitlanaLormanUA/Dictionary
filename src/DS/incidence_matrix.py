from collections import defaultdict
import re

class IncidenceMatrix:
    def __init__(self):
        #використовую set для забезпечення унікальності термінів та документів
        self.terms = set()  
        self.documents = set() 
        self.matrix = defaultdict(dict)  # Матриця: термін -> документ -> 0/1

    def add_term_document(self, term, document):
        self.terms.add(term)
        self.documents.add(document)
        self.matrix[term][document] = 1



    def boolean_search(self, query):
        query = query.replace("(", " ( ").replace(")", " ) ")  
        tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\s+NOT\s+|\s*\(\s*|\s*\)\s*)', query) 
        tokens = [token.strip() for token in tokens if token.strip()]  

        stack = []
        operator = None

        for token in tokens:
            if token == 'AND':
                operator = 'AND'
            elif token == 'OR':
                operator = 'OR'
            elif token == 'NOT':
                operator = 'NOT'
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
                    stack.append(stack.pop() & docs)  # AND
                elif operator == 'OR':
                    stack.append(stack.pop() | docs)  # OR
                elif operator == 'NOT':
                    stack.append(stack.pop() - docs)  # NOT
                else:
                    stack.append(docs)

        # Повертаємо результат, що залишився в стеку
        return stack[0] if stack else set()

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

        return set(self.matrix.get(term, {}).keys())