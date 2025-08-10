# anagram_checker.py

class AnagramChecker:
    def __init__(self, wordlist_file):
        """
        Loads the list of valid words from the given file into memory.
        Stores them in a set for fast lookups.
        """
        with open(wordlist_file, 'r') as f:
            self.words = {line.strip().lower() for line in f}

    def is_valid_word(self, word):
        """
        Returns True if the given word is a valid English word.
        """
        return word.lower() in self.words

    def is_anagram(self, word1, word2):
        """
        Returns True if word1 and word2 are anagrams.
        """
        return sorted(word1.lower()) == sorted(word2.lower()) and word1.lower() != word2.lower()

    def get_anagrams(self, word):
        """
        Returns a list of anagrams for the given word from the dictionary.
        """
        return [w for w in self.words if self.is_anagram(word, w)]
