#text_analysis.py

import string
import re


class Text:
    def __init__(self, text):
        self.text = text

    def word_frequency(self, word):
        words = self.text.lower().split()
        count = words.count(word.lower())
        return count if count > 0 else f"'{word}' not found."

    def most_common_word(self):
        words = self.text.lower().split()
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        if not freq:
            return None
        return max(freq, key=freq.get)

    def unique_words(self):
        words = self.text.lower().split()
        return list(set(words))

    @classmethod
    def from_file(cls, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return cls(content)
        except FileNotFoundError:
            print("File not found.")
            return cls("")


class TextModification(Text):
    def remove_punctuation(self):
        translator = str.maketrans('', '', string.punctuation)
        cleaned = self.text.translate(translator)
        return cleaned

    def remove_stop_words(self):
        stop_words = set([
            "a", "an", "the", "is", "are", "in", "on", "and", "of", "to", "that", "this", "for", "with", "as", "by",
            "was", "were", "be", "been", "it"
        ])
        words = self.text.split()
        filtered = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered)

    def remove_special_characters(self):
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)
        return cleaned


# Optional: quick test
if __name__ == "__main__":
    sample_text = "This is a simple sentence, with punctuation! And some special #characters$ too..."
    txt = TextModification(sample_text)

    print("Original:", txt.text)
    print("No punctuation:", txt.remove_punctuation())
    print("No stop words:", txt.remove_stop_words())
    print("No special characters:", txt.remove_special_characters())
