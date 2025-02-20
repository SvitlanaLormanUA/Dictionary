
class Word:
    def __init__(self, word):
        self.word = word
        self.count = 1
        self.file_occurrences = set()

    def increment_count(self):
        self.count += 1

    def add_file_occurrence(self, file_name):
        self.file_occurrences.add(file_name)

    def get_files(self):
        return ', '.join(self.file_occurrences)
