# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:21:11 2024

@author: panag
"""

import json
from collections import defaultdict

#Φόρτωση των προεπεξεργασμένων κειμένων
with open('processed_wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Δημιουργία ανεστραμμένου ευρετηρίου
inverted_index = defaultdict(list)

#Συμπλήρωση του ανεστραμμένου ευρετηρίου
for doc_id, article in enumerate(articles):
    for position, word in enumerate(article['processed_content']):
        #Πρσθήκη του doc_id και της θέσης λέξης στο ευρετήριο για κάθε λέξη
        inverted_index[word].append((doc_id, position))
        
#Αποθήκευση του ευρετήριου σε JSON
with open('inverted_index.json', 'w', encoding='utf-8') as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=4)
    
print("Το ανεστραμμένο ευρετήριο αποθηκεύτηκε στο inverted_index.json.")