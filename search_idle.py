# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:31:33 2024

@author: panag
"""

import json
import math
from collections import defaultdict, Counter

#Φόρτωση του ανεστραμμένου ευρετηρίου και των άρθρων
with open('inverted_index.json', 'r', encoding='utf-8') as f:
    inverted_index = json.load(f)
    
with open('processed_wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Συνάρτηση για επεξεργασία ερώτησης
def preprocess_question(question):
    return question.lower().split()

#Συνάρτηση για ανάκτηση εγγράφων σύμφωνα με την ερώτηση
def retrieve_docs(question_term):
    doc_scores = defaultdict(float)
    
    for term in question_term:
        if term in inverted_index:
            dhmosieyseis = inverted_index[term]
            doc_counter = len(dhmosieyseis)
            
            for doc_id, position in dhmosieyseis:
                #Υπολογισμός TF-IDF
                term_counter = Counter([pos[0] for pos in dhmosieyseis])[doc_id]
                tf = 1 + math.log(term_counter)
                idf = math.log(len(articles) / (1 + doc_counter))
                doc_scores[doc_id] += tf * idf
                
    #Ταξινόμηση με βάση την κατάταξη του σκορ
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

#Διεπαφή για την εύρεση αποτελεσμάτων σύμφωνα με την ερώτηση
def anazhthsh(question):
    question_term = preprocess_question(question)
    res = retrieve_docs(question_term)
    
    if not res:
        print("Δεν βρέθηκε το έγγραφο.")
    else:
        print(f"Αποτελέσματα '{question}':")
        for doc_id, score in res[:5]:
            print(f"'Εγγραφο {doc_id}, Τίτλος: {articles[doc_id]['title']}, Σκορ: {score:.4f}")
            
question = input("Τι θα αναζητήσεις σήμερα: ")
anazhthsh(question)