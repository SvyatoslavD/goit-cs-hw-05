import requests
import re

from multiprocessing import Pool
from collections import Counter

import matplotlib.pyplot as plt


def text_to_words(text):
    words = re.findall(r'\w+', text.lower())
    return [(word, 1) for word in words]


def map_reduce(text, chunk_size=1000):
    text_chunks = [text[i:i+chunk_size]
                   for i in range(0, len(text), chunk_size)]

    pool = Pool()
    mapped = pool.map(text_to_words, text_chunks)

    reduced = sum((Counter(dict(chunk)) for chunk in mapped), Counter())

    return reduced


def visualize_top_words(word_counts, top=10):
    top_words = word_counts.most_common(top)

    words, counts = zip(*top_words)
    words = words[::-1]
    counts = counts[::-1]

    plt.barh(words, counts)
    plt.ylabel('Words')
    plt.xlabel('Counts')
    plt.title(f'Top 10 words')
    plt.show()


url = "https://www.rfc-editor.org/rfc/rfc7348.txt"
response = requests.get(url)
text = response.text

word_counts = map_reduce(text)

visualize_top_words(word_counts, top=10)