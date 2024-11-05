# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:56:24 2024

@author: panag
"""

import json
from search_idle import retrieve_docs

#Υποθετική λίστα φράσεων για κάθε ερώτημα
relevant_docs = {
    "web scraping": [0],
    "data science": [1], 
    "information retrieval": [2],
    "data mining": [3],
    "cluster analysis": [4],
    "information extraction": [5],
    "knowledge extraction": [6]
    }

#Φόρτωση των άρθρων και της μηχανής αναζήτησης
with open('processed_wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Συνάρτηση για τον υπολογισμό της ακρίβειας, ανάκλησης και του F1-score
def aksiologisi_question(question, retrieved_docs):
    relevant = relevant_docs.get(question, [])
    
    
    #Βρίσκουμε τα έγγραφα που σχετίζονται απο την ανάκτηση
    true_pos = [doc for doc in retrieved_docs if doc[0] in relevant]
    false_pos = [doc for doc in retrieved_docs if doc[0] not in relevant]
    false_neg = [doc for doc in relevant if doc not in [doc[0] for doc in retrieved_docs]]
    
    
    #Υπολογισμός της ακρίβειας, ανάκλησης και F1-score
    precision = len(true_pos) / len(retrieved_docs) if retrieved_docs else 0
    recall = len(true_pos) / len(relevant) if relevant else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score

#Συνάρτηση για την αξιολόγηση της μηχανής αναζήτησης
def aksiologisi_mixanis_anazitisis():
    total_prec, total_rec, total_f1 = 0, 0, 0
    question_count = len(relevant_docs)
    
    for question in relevant_docs:
        print(f"Αξιολόγηση για το ερώτημα: '{question}'")
        question_term = question.split()
        retrieved_docs = retrieve_docs(question_term)[:5]
        precision, recall, f1_score = aksiologisi_question(question, retrieved_docs)
        total_prec += precision
        total_rec += recall
        total_f1 += f1_score
        
        print(f"Ακρίβεια: {precision:.2f}, Ανάκληση: {recall:.2f}, F1-score: {f1_score:.2f}.")
        
    
    #Μέσοι όροι
    avg_prec = total_prec / question_count
    avg_rec = total_rec / question_count
    avg_f1  = total_f1 / question_count
    
    print(f"Μέση Ακρίβεια: {avg_prec:.2f}, Μέση Ανάκληση: {avg_rec:.2f}, Μέσο F1-score: {avg_f1:.2f}.")
    
    
#Εκτέλεση της αξιολόγησης
aksiologisi_mixanis_anazitisis()
