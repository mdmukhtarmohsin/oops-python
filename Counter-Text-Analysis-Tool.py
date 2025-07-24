from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        self.original_text = text
        self.text = text.lower()  # For case-insensitive analysis

    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        if include_spaces:
            chars = self.text
        else:
            chars = self.text.replace(' ', '')
        return Counter(chars)

    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        words = re.findall(r'\b\w+\b', self.text)
        filtered_words = [w for w in words if len(w) >= min_length]
        return Counter(filtered_words)

    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        # Split sentences by . ! ?
        sentences = re.split(r'[.!?]+', self.original_text)
        sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if s.strip()]
        lengths_counter = Counter(sentence_lengths)
        if sentence_lengths:
            average = sum(sentence_lengths) / len(sentence_lengths)
            longest = max(sentence_lengths)
            shortest = min(sentence_lengths)
        else:
            average = longest = shortest = 0
        return {
            'lengths': lengths_counter,
            'average': average,
            'longest': longest,
            'shortest': shortest
        }

    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                        'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
                        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        words = re.findall(r'\b\w+\b', self.text)
        if exclude_common:
            words = [w for w in words if w not in common_words]
        freq = Counter(words)
        return freq.most_common(n)

    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                  average_word_length, reading_time_minutes (assume 200 WPM)
        """
        words = re.findall(r'\b\w+\b', self.original_text)
        word_count = len(words)
        char_count = len(self.original_text)
        sentences = re.split(r'[.!?]+', self.original_text)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_word_length = sum(len(w) for w in words) / word_count if word_count else 0
        reading_time = word_count / 200 if word_count else 0
        return {
            'character_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': avg_word_length,
            'reading_time_minutes': reading_time
        }

    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
        words1 = set(re.findall(r'\b\w+\b', self.text))
        words2 = set(re.findall(r'\b\w+\b', other_text.lower()))
        common = words1 & words2
        unique1 = words1 - words2
        unique2 = words2 - words1
        similarity = len(common) / max(len(words1 | words2), 1)
        return {
            'common_words': list(common),
            'similarity_score': similarity,
            'unique_to_first': list(unique1),
            'unique_to_second': list(unique2)
        }

# Test your implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is simple, easy to learn
syntax emphasizes readability and therefore reduces the cost of program maintenance.
Python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequency (top 5):", analyzer.get_character_frequency()[:5])
print("Word frequency (top 5):", analyzer.get_word_frequency()[:5])
print("Common words:", analyzer.find_common_words(5))
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)
