# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:33:53 2024

@author: panag
"""

import json

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import string

#Αρχικοποίηση εργαλείων επεξεργασίας κειμένου
nltk.download('punkt')  #tokenization
nltk.download('stopwords')  #stop words
nltk.download('wordnet')  # lemmatization

#Φόρτωση άρθρων από το αρχείο JSON
with open('wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Συνάρτηση για την προεπεξεργασία κειμένου
def preprocess_text(text):
    #Μετατροπή σε πεζά
    text = text.lower()
    
    #Tokenization
    tokens = word_tokenize(text)
    
    #Αφαίρεση σημείων στίξης
    tokens = [token for token in tokens if token not in string.punctuation]
    
    #Αφαίρεση stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    #Κανονικοποίηση με Stemming και Lemmatization
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(stemmer.stem(word)) for word in tokens]
    
    return tokens

#Εφαρμογή της προεπεξεργασίας σε όλα τα άρθρα και υπολογισμός στατιστικών
for article in articles:
    processed_text = preprocess_text(article['content'])
    article['processed_content'] = processed_text
    
    #Υπολογισμός στατιστικών (Κατανομή συχνότητας)
    freq_dist = FreqDist(processed_text)
    article['vocab_richness'] = len(set(processed_text)) / len(processed_text) if len(processed_text) > 0 else 0
    article['freq_dist'] = freq_dist.most_common(10) #Τα 10 πιο κοινά tokens
    
#Αποθήκευση των επεξεργασμένων άρθρων σε νέο αρχείο JSON
with open('processed_wikipedia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
    
print("Η προεπεξεργασία και τα στατιστικά των άρθρων ολοκληρώθηκαν και αποθηκεύτηκαν στο 'processed_wikipedia_articles.json'.")
    