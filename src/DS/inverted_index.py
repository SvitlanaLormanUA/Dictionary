from collections import defaultdict


import re

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)  # Індекс: термін -> документи, де він зустрічається

    def add_term_document(self, term, document):
        self.index[term].add(document)

    def boolean_search(self, query):
        query = query.replace("(", " ( ").replace(")", " ) ")
       
        tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\s+NOT\s+|\s*\(\s*|\s*\)\s*)', query)
        tokens = [token.strip() for token in tokens if token.strip()]  

        stack = []
        operator = None

        for token in tokens:
            if token == 'AND' or token == 'OR' or token == 'NOT':
                operator = token  
            elif token == '(':
                stack.append('(')  
            elif token == ')':

                temp_stack = []
                while stack and stack[-1] != '(':
                    temp_stack.insert(0, stack.pop())  
                stack.pop()  # Видаляємо '('
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

        return set(self.index.get(term, {}))