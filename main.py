# ==============================================================================
# file: main.py
# author: Allen Sun
# created date: 2024-06-09
# Copyright: Copyright 2024 Allen Sun. All rights reserved.
# License: MIT License
# Contact me: allensrj@qq.com
# Description: This script is used to extract English words from documents and compare with the Oxford Dictionary.
# ==============================================================================

from pathlib import Path

from functions import get_all_txt_files, get_all_pdf_files, extract_words_from_niujin, extract_text_from_pdf, process_text, check_target_words_in_oxford

working_dir = Path().cwd()
oxford_dictionary_path = working_dir / "oxford_dictionary"
target_path = working_dir / "target"

def extract_words(oxford_dictionary_path, target_path):
    """
    Extract words from Oxford dictionary files and target PDF files.
    """
    # Extract words from Oxford dictionary files
    oxford_dictionary_files = get_all_txt_files(oxford_dictionary_path)
    oxford_dictionary_words = []
    for file in oxford_dictionary_files:
        oxford_dictionary_words.extend(extract_words_from_niujin(file))
    oxford_dictionary_words = list(set(oxford_dictionary_words))
    oxford_dictionary_words.sort(key=len)
    print("Oxford dictionary words extraction completed.")

    # Extract words from target PDF files
    pdf_files = get_all_pdf_files(target_path)
    target_words = []
    for file in pdf_files:
        text_content = extract_text_from_pdf(file)
        processed_text = process_text(text_content).split("\n")
        target_words.extend(list(set(processed_text)))
    target_words = list(set(target_words))
    target_words.sort(key=len)
    print("Target folder words extraction completed.")

    return oxford_dictionary_words, target_words


if __name__ == "__main__":

    oxford_dictionary_words, target_words = extract_words(oxford_dictionary_path, target_path)
    results = check_target_words_in_oxford(target_words, oxford_dictionary_words)