import nltk
from collections import Counter
import re

with open("19_test_inputs.txt") as f:
    texts = f.readlines()

with open("American Oxford 5000.txt") as f:
    words = [w.lower().strip() for w in f.readlines()]
    words = sorted(words, key=lambda a: len(a), reverse=True)
    words = [w for w in words if len(w) > 1 or w in ["i", "a"]]

REQUIRED_TAGS = {"NOUN", "ADJ", "VERB"}

def process_input(input: str) -> str:
    return re.sub(r"[^a-z ]", "", input.lower())

def rearrange_letters(input: str) -> str:
    input = process_input(input)
    ignored_words = [word for word in input.split() if len(word) > 3]

    input_freqs = Counter(input)
    del input_freqs[" "]

    new_sentence = []


    while True:
        for word in words:
            if word in ignored_words: continue
            word_freqs = Counter(word)

            # Test if the word is usable
            for char,freq in word_freqs.items():
                if input_freqs[char] < freq:
                    break
            # If it never broke, it is
            else:
                new_sentence.append(word)
                # Removes the frequencies
                for char,freq in word_freqs.items():
                    input_freqs[char] -= freq

        # Tests if all characters are used
        if input_freqs.most_common()[0][1] > 0:
            # If not, deletes the longest word and tries again
            word_remove = max(new_sentence, key=len)
            ignored_words.append(word_remove)
            new_sentence.remove(word_remove)

            word_freqs = Counter(word_remove)
            for char,freq in word_freqs.items():
                input_freqs[char] += freq

            continue

        # Tests if all REQUIRED_TAGS are present
        tags = nltk.pos_tag(new_sentence, tagset="universal")
        tags_set = set(t[1] for t in tags)
        if not REQUIRED_TAGS.issubset(tags_set):
            missing = REQUIRED_TAGS.difference(tags_set)
            most_common = Counter(t[1] for t in tags).most_common()[0][0]

            # If not, deletes the longest word of the most common POS and tries again
            word_remove = max([t[0] for t in tags if t[1] == most_common], key=len)
            ignored_words.append(word_remove)
            new_sentence.remove(word_remove)

            word_freqs = Counter(word_remove)
            for char,freq in word_freqs.items():
                input_freqs[char] += freq
        else:
            # If here, both conditions are passed and the sentence works
            break

    return " ".join(new_sentence)

def test_freq_match(a: str, b: str) -> bool:
    a_freq = Counter(a)
    b_freq = Counter(b)
    # Ignore number of spaces
    del a_freq[" "]
    del b_freq[" "]

    return a_freq == b_freq

def test_pos_match(a: str) -> bool:
    tags = nltk.pos_tag(a.split(), tagset="universal")
    tags_set = set(t[1] for t in tags)
    return REQUIRED_TAGS.issubset(tags_set)
    
# print(rearrange_letters("Mary had a little lamb."))
for text in texts:
    original = process_input(text)
    rearranged = rearrange_letters(text)

    print(original)
    print(rearranged)
    print()
    print(test_freq_match(original, rearranged))
    print(test_pos_match(rearranged))
