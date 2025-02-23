import string
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import requests
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
    
async def get_text(url):
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching URL: {e}")
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def reduce_function(word_counts):
    counter = Counter()
    for word, count in word_counts:
        counter[word] += count
    return counter

def map_reduce(text, search_words=None):
    words = text.split()
    if search_words:
        words = [word for word in words if word in search_words]
    with ThreadPoolExecutor() as executor:
        word_counts = list(executor.map(map_function, words))
    return reduce_function(word_counts)

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.barh(words, counts)
    plt.ylabel('Words')
    plt.xlabel('Frequency')
    plt.title('Top Words by Frequency')
    plt.gca().invert_yaxis()
    plt.show()

async def main():
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = await get_text(url)
    if text:
        text = remove_punctuation(text)  # Remove punctuation from the text
        search_words = ['war', 'peace', 'love']  # specify words to search
        word_counts = map_reduce(text, search_words)  # add second argument search_words for specific words
        visualize_top_words(word_counts)
        logging.info("Результат підрахунку слів: %s", word_counts)
    else:
        logging.info("Помилка: Не вдалося отримати вхідний текст.")


if __name__ == '__main__':
    asyncio.run(main())
