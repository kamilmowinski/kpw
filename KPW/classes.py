__author__ = 'km'
import re
import collections

from django.conf import settings


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


class WordCorrection:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.nwords = self.train(self.words(file(settings.WORDS_LIST).read()))

    def words(self, text):
        return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts = [a + c + b for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.nwords)

    def known(self, words):
        return set(w for w in words if w in self.nwords)

    def correct(self, word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(candidates, key=self.nwords.get)