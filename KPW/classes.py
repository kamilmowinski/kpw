__author__ = 'km'


class SearchResult:
    def __init__(self, uri, title, content, key_words, probability=1.0):
        self.uri = uri
        self.title = title
        self.content = content
        self.key_words = key_words
        self.probability = probability

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)