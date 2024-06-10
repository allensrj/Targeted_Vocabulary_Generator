# ==============================================================================
# file: functions.py
# author: Allen Sun
# created date: 2024-06-09
# Copyright: Copyright 2024 Allen Sun. All rights reserved.
# License: MIT License
# Contact me: allensrj@qq.com
# Description: Scripts for storing functions.
# ==============================================================================


import os
import re
from concurrent.futures import ThreadPoolExecutor
import fitz  # PyMuPDF library


def extract_words_from_niujin(path):
    """
    Extract words from a file assumed to be a dictionary, filtering out non-words and duplicates.
    Only words at the beginning of each line are considered.
    """
    with open(path, "r", encoding='latin-1') as file:
        text = file.read()

    pattern = re.compile(r'^[\w-]+(?=\s|$)')
    words = [line.strip().split()[0] for line in text.split('\n') if pattern.match(line)]
    words = list(set(words))  # Remove duplicates
    words.sort(key=len)
    words = [word for word in words if "-" not in word]  # Filter out hyphenated words
    return words


def get_all_txt_files(path):
    """
    Return a list of all .txt files in a directory, including subdirectories.
    """
    return [os.path.join(root, file) for root, dirs, files in os.walk(path)
            for file in files if file.lower().endswith('.txt')]


def get_all_pdf_files(path):
    """
    Return a list of all .pdf files in a directory, including subdirectories.
    """
    return [os.path.join(root, file) for root, dirs, files in os.walk(path)
            for file in files if file.lower().endswith('.pdf')]


def process_text(content):
    """
    Process the given text to remove digits, punctuation (except hyphens),
    convert to lowercase, and split into a sorted list of unique words longer than 3 characters.
    """
    content = content.lower().replace('-', '\n')
    content = re.sub(r'\s+', '\n', content)
    content = re.sub(r'[^\w\s-]', '', content)
    content = re.sub(r'\d', '', content)
    words = [line.strip() for line in content.split('\n') if len(line.strip()) > 3]
    return '\n'.join(sorted(set(words), key=len))


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF.
    """
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text() + "\n"
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' in block:
                for line in block["lines"]:
                    text += " ".join(span["text"] for span in line["spans"]) + "\n"
    document.close()
    return text


def check_word(word, dictionary_words):
    """
    Check if a word is in the dictionary, returning the word if it exists.
    """
    return word if word in dictionary_words else None


def check_target_words_in_oxford(target_words, dictionary_words):
    """
    Check a list of target words against the Oxford dictionary words and write the found words to a file.
    """
    max_workers = max(1, os.cpu_count() - 1)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = [future.result() for future in
                   (executor.submit(check_word, word, dictionary_words) for word in target_words) if future.result()]

    with open("results.txt", "w") as file:
        for word in results:
            file.write(word + "\n")
    print(f"已将自制词汇表输出至：{os.getcwd()}/results.txt")
    print(f"自制词汇表单词数量：{len(results)}")
    return results