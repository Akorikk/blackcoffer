import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
import os
import re
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')

input_df = pd.read_excel("Input.xlsx")


def load_stopwords():
    stopwords = set()
    stopword_dir = "StopWords"

    for file in os.listdir(stopword_dir):
        file_path = os.path.join(stopword_dir, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="ISO-8859-1") as f:
                for line in f:
                    stopwords.add(line.strip().lower())
    return stopwords


STOPWORDS = load_stopwords()


def load_master_dictionary():
    positive = set()
    negative = set()

    for file in os.listdir("MasterDictionary"):
        file_path = os.path.join("MasterDictionary", file)

        if "positive" in file.lower():
            with open(file_path, "r", encoding="ISO-8859-1") as f:
                for line in f:
                    positive.add(line.strip().lower())

        if "negative" in file.lower():
            with open(file_path, "r", encoding="ISO-8859-1") as f:
                for line in f:
                    negative.add(line.strip().lower())

    return positive, negative


POSITIVE_DICT, NEGATIVE_DICT = load_master_dictionary()


def extract_article(url):
    """
    Extract title + article text from the URL using BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        paragraphs = soup.find_all("p")
        article = " ".join(p.get_text(strip=True) for p in paragraphs)

        return title + "\n" + article

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


for index, row in input_df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    print(f"Scraping URL_ID {url_id} ...")

   
    article_text = extract_article(url)

   
    with open(f"Articles/{url_id}.txt", "w", encoding="utf-8") as f:
        f.write(article_text)

    print(f"Saved: Articles/{url_id}.txt")


def clean_text(text, stopwords):
    text = re.sub(r'[^A-Za-z\s]', ' ', text)
    text = text.lower()
    words = text.split()

    cleaned_words = [word for word in words if word not in stopwords]

    return cleaned_words

def load_article(url_id):
    try:
        with open(f"Articles/{url_id}.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""
    
results = []   # will store final results for Output.xlsx

for index, row in input_df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    raw_text = load_article(url_id)

    # Clean the article text
    cleaned_words = clean_text(raw_text, STOPWORDS)

    # Store cleaned_words for metric calculation
    results.append({
        "URL_ID": url_id,
        "URL": url,
        "cleaned_words": cleaned_words,
        "raw_text": raw_text
    })


def get_positive_negative_scores(cleaned_words):
    positive_score = sum(1 for word in cleaned_words if word in POSITIVE_DICT)
    negative_score = sum(1 for word in cleaned_words if word in NEGATIVE_DICT)
    return positive_score, negative_score

def get_polarity_score(pos, neg):
    return (pos - neg) / ((pos + neg) + 0.000001)

def get_subjectivity_score(pos, neg, total_words):
    return (pos + neg) / (total_words + 0.000001)


def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    
    if word.endswith(("es", "ed")):
        word = word[:-2]

    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
                prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False

    return count

def count_complex_words(cleaned_words):
    complex_words = [word for word in cleaned_words if count_syllables(word) > 2]
    return len(complex_words), complex_words


def get_percentage_complex_words(complex_word_count, total_words):
    return complex_word_count / total_words if total_words > 0 else 0


def get_average_sentence_length(raw_text):
    sentences = sent_tokenize(raw_text)
    words = raw_text.split()
    return len(words) / len(sentences) if len(sentences) > 0 else 0


def get_fog_index(avg_sentence_length, percentage_complex_words):
    return 0.4 * (avg_sentence_length + percentage_complex_words)


def get_avg_words_per_sentence(raw_text):
    sentences = sent_tokenize(raw_text)
    words = raw_text.split()
    return len(words) / len(sentences) if len(sentences) > 0 else 0


def get_word_count(cleaned_words):
    return len(cleaned_words)


def count_personal_pronouns(text):
    pronouns = re.findall(r"\b(I|we|us|my|ours|our)\b", text, re.I)
    return len(pronouns)


def get_avg_word_length(cleaned_words):
    if len(cleaned_words) == 0:
        return 0
    total_chars = sum(len(word) for word in cleaned_words)
    return total_chars / len(cleaned_words)


output_rows = []

for item in results:
    url_id = item["URL_ID"]
    url = item["URL"]
    cleaned_words = item["cleaned_words"]
    raw_text = item["raw_text"]

    pos, neg = get_positive_negative_scores(cleaned_words)
    total_words = len(cleaned_words)
    complex_count, complex_words = count_complex_words(cleaned_words)
    percentage_complex_words = get_percentage_complex_words(complex_count, total_words)
    avg_sentence_length = get_average_sentence_length(raw_text)
    fog_index = get_fog_index(avg_sentence_length, percentage_complex_words)
    avg_words_per_sentence = get_avg_words_per_sentence(raw_text)
    syllables_per_word = sum(count_syllables(w) for w in cleaned_words) / (total_words + 0.000001)
    personal_pronouns = count_personal_pronouns(raw_text)
    avg_word_length = get_avg_word_length(cleaned_words)

    output_rows.append([
        url_id,
        url,
        pos,
        neg,
        get_polarity_score(pos, neg),
        get_subjectivity_score(pos, neg, total_words),
        avg_sentence_length,
        percentage_complex_words,
        fog_index,
        avg_words_per_sentence,
        complex_count,
        total_words,
        syllables_per_word,
        personal_pronouns,
        avg_word_length
    ])


output_df = pd.DataFrame(output_rows, columns=[
    "URL_ID",
    "URL",
    "POSITIVE SCORE",
    "NEGATIVE SCORE",
    "POLARITY SCORE",
    "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH",
    "PERCENTAGE OF COMPLEX WORDS",
    "FOG INDEX",
    "AVG NUMBER OF WORDS PER SENTENCE",
    "COMPLEX WORD COUNT",
    "WORD COUNT",
    "SYLLABLE PER WORD",
    "PERSONAL PRONOUNS",
    "AVG WORD LENGTH"
])

output_df.to_excel("Output.xlsx", index=False)
print("Output.xlsx created successfully!")
