class BiwordIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, file_name, text):
        words = text.split()
        for i in range(len(words) - 1):
            biword = (words[i], words[i + 1])  
            if biword not in self.index:
                self.index[biword] = {}
            if file_name not in self.index[biword]:
                self.index[biword][file_name] = []
            self.index[biword][file_name].append(i)  

    def search_phrase(self, phrase):
        words = phrase.split()
        if len(words) < 2:
            return set() 

        first_biword = (words[0], words[1])
        if first_biword not in self.index:
            return set()

        result_docs = set(self.index[first_biword].keys())

        for i in range(1, len(words) - 1):
            biword = (words[i], words[i + 1])
            if biword not in self.index:
                return set()
            result_docs &= set(self.index[biword].keys())  

        return result_docs 

    def search_with_distance(self, word1, word2, max_distance=2):
        result_files = set()
        
        for biword, doc_positions in self.index.items():
            for file_name, positions in doc_positions.items():
                if biword[0] == word1 and biword[1] == word2:
                    result_files.add(file_name)
                elif word1 in biword or word2 in biword:
                    for pos in positions:
                        if any(abs(pos - other_pos) <= max_distance for other_pos in positions):
                            result_files.add(file_name)

        return result_files

    def save_to_file(self, file_name):
        with open(file_name, "w") as f:
            for biword, docs in sorted(self.index.items()):
                formatted_biword = f"({biword[0]} {biword[1]})"
                doc_list = ', '.join(docs.keys())
                f.write(f"{formatted_biword}: {doc_list}\n")