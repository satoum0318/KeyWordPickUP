import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
import pdfplumber
from janome.tokenizer import Tokenizer
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages[:2]  # 最初の2ページを取得
        for page in pages:
            page_text = page.extract_text() if page.extract_text() else ''
            text += page_text + ' '  # ページ間でテキストを区切るためにスペースを追加
    return text

def custom_tokenizer(text, min_gram):
    t = Tokenizer()
    tokens = t.tokenize(text)
    noun_phrases = []
    current_phrase = []

    for token in tokens:
        if token.part_of_speech.startswith('名詞'):
            # 日本語の不要な記号とcidを除去
            cleaned_surface = re.sub(r'[,.()<>;:{}\[\]\"\'\`~!@#$%^&*_|+=/?-》。]', '', token.surface)
            cleaned_surface = re.sub(r'\bcid\b', '', cleaned_surface, flags=re.IGNORECASE)
            if cleaned_surface:
                current_phrase.append(cleaned_surface)
        else:
            if current_phrase and len(current_phrase) >= min_gram:
                joined_phrase = "".join(current_phrase)
                noun_phrases.append(joined_phrase)
            current_phrase = []

    # 英語の単語を抽出し、連続する単語をスペースで連結
    english_words = re.findall(r'\b[a-zA-Z]+\b', text)
    english_words_cleaned = [re.sub(r'\bcid\b', '', word, flags=re.IGNORECASE) for word in english_words if word.isalpha()]
    english_phrases = []
    current_english_phrase = []

    for word in english_words_cleaned:
        if word:
            current_english_phrase.append(word)
            if len(current_english_phrase) >= min_gram:
                joined_phrase = " ".join(current_english_phrase)
                english_phrases.append(joined_phrase)
                current_english_phrase = []  # フレーズをリセット

    return noun_phrases + english_phrases

def analyze_text(text, min_gram):
    keywords = custom_tokenizer(text, min_gram)
    return Counter(keywords)

def analyze_pdfs_in_folder(folder_path, min_gram):
    files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    keyword_frequency = Counter()
    for filename in files:
        pdf_path = os.path.join(folder_path, filename)
        text = extract_text_from_pdf(pdf_path)
        file_keywords = analyze_text(text, min_gram)  # min_gramを渡す
        keyword_frequency.update(file_keywords)
    return keyword_frequency

def load_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        min_gram = int(gram_spinbox.get())  # スピンボックスから最小グラム数を取得
        keywords = analyze_pdfs_in_folder(folder_path, min_gram)  # 最小グラム数を引数として渡す
        most_common_keywords = keywords.most_common(10)
        result_text = "Most common keywords:\n"
        for keyword, frequency in most_common_keywords:
            result_text += f"{keyword}: {frequency}\n"
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result_text)
        text_area.config(state=tk.DISABLED)
        progress_var.set(0)  # Reset the progress bar after completion

# 一文字のアルファベットとスペースのみで構成されるキーワードを除外する関数
def filter_keywords(keywords):
    filtered_keywords = Counter()
    for keyword, count in keywords.items():
        # アルファベットとスペースのみで構成されているかチェック
        if not re.match(r'^([A-Za-z]\s)+[A-Za-z]?$', keyword):
            filtered_keywords[keyword] = count
    return filtered_keywords

# GUI setup
root = tk.Tk()
root.title("PDF Keyword Extractor")

frame = tk.Frame(root)
frame.pack(pady=20)

# グラム数の設定用スピンボックス
gram_label = tk.Label(frame, text="グラム数:")
gram_label.pack(side=tk.LEFT)
gram_spinbox = tk.Spinbox(frame, from_=1, to=10, width=5)
gram_spinbox.pack(side=tk.LEFT, padx=10)

load_button = tk.Button(frame, text="Load PDF Folder", command=load_folder)
load_button.pack(side=tk.LEFT, padx=10)

text_area = scrolledtext.ScrolledText(frame, width=60, height=10, state=tk.DISABLED)
text_area.pack(padx=10, pady=10)

progress_var = tk.DoubleVar()  # Variable to update the progressbar
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=20)

root.mainloop()

# Example usage
text = "二慣性系の振動抑制制御について研究しています。モータの高効率化を目指しています。"
min_gram_value = 2  # 適切なmin_gram値を設定
keywords = analyze_text(text, min_gram_value)
filtered_keywords = filter_keywords(keywords)
print(filtered_keywords)

