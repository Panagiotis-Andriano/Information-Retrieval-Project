

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi


#Φόρτωση του ανεστραμμένου ευρετηρίου και των άρθρων
with open('inverted_index.json', 'r', encoding='utf-8') as f:
    inverted_index = json.load(f)
    
with open('processed_wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
titles = [article['title'] for article in articles]
corpus = [' '.join(article['processed_content']) for article in articles]

#Υλοποίηση TF-IDF με Scikit-learn
tfidf_vector = TfidfVectorizer(vocabulary=inverted_index.keys())
tfidf_matrix = tfidf_vector.fit_transform(corpus) 

#Υλοποοίηση BM25 με rank_bm25
bm25_model = BM25Okapi([doc.split() for doc in corpus])


#Συνάρτηση για χρήση Boolean Retrieval
def boolean_retrieve_docs(question_term, operator):
    result_docs = set()
    if operator == "AND":
        #Η τομή όλων των εγγραφών που περιέχουν τους όρους
        result_docs = set(range(len(articles)))
        for term in question_term:
            if term in inverted_index:
                doc_ids = {doc_id for doc_id, _ in inverted_index[term]}
                result_docs &= doc_ids
            else:
                result_docs = set() 
                break
        return result_docs
    
    elif operator == "OR":
        #Η ένωση όλων των εγγραφών που περιέχουν τους όρους
         result_docs = set()
         for term in question_term:
             if term in inverted_index:
                 doc_ids = {doc_id for doc_id, _ in inverted_index[term]}
                 result_docs |= doc_ids
             else:
                  print("Μη έγκυρη επιλογή.")
                  return
         return result_docs
     
    elif operator == "NOT":
        #Συμπλήρωμα των εγγραφών που περιέχουν τους όρους
        all_docs = set(range(len(articles)))
        for term in question_term:
            if term in inverted_index:
                doc_ids = {doc_id for doc_id, _ in inverted_index[term]}
                all_docs -= doc_ids
        return all_docs
    
    return set()


#Συνάρτηση για υπολογισμό TF-IDF
def search_tfidf(query):
    query_vector = tfidf_vector.transform([query])
    scores = (tfidf_matrix * query_vector.T).toarray().flatten()
    ranked_docs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(doc_id, score) for doc_id, score in ranked_docs if score > 0]

#Συνάρτηση για υπολογισμό Okapi BM25
def search_bm25(query):
    query_terms = query.split()
    scores = bm25_model.get_scores(query_terms)
    ranked_docs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(doc_id, score) for doc_id, score in ranked_docs if score > 0]
   

#Συνάρτηση για υπολογισμό με Vector Space Model
def search_vsm(query):
    query_vector = tfidf_vector.transform([query]).toarray()
    doc_vectors = tfidf_matrix.toarray()
    scores = [sum(query_vector[0] * doc_vector) for doc_vector in doc_vectors] 
    ranked_docs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(doc_id, score) for doc_id, score in ranked_docs if score > 0]

#Διεπαφή για την εύρεση αποτελεσμάτων σύμφωνα με την ερώτηση
def anazhthsh():
    while True:
        question = input("Τι θα αναζητήσεις σήμερα: ")
        if ":" in question:
            parts = question.split(":", 1)
            telesths = parts[0].strip().upper()
            oroi = parts[1].strip().split()
            res = boolean_retrieve_docs(oroi, telesths)
            if not res:
                print("Δεν βρέθηκαν αποτελέσματα!")
            else:
                print(f"Αποτε΄λέσματα '{question}':")
                for doc_id in res:
                    print(f"Έγγραφο {doc_id}, Τίτλος: {articles[doc_id]['title']}")
        else:
            print("Επέλεξε αλγόριθμο: 1. TF-IDF, 2. Okapi BM25, 3. Vector Space Model(VSM)")
            choice = input("Επιλογή: ")
            if choice == "1":
                res = search_tfidf(question)
            elif choice == "2":
                res = search_bm25(question)
            elif choice == "3":
                res = search_vsm(question)
            else:
                print("Όχι τέτοια επιλογή!")
                continue
    
            if not res:
                print("Δεν βρέθηκε το έγγραφο.")
            else:
                print(f"Αποτελέσματα '{question}':")
                for doc_id, score in res[:5]:
                    print(f"'Εγγραφο {doc_id}, Τίτλος: {articles[doc_id]['title']}, Σκορ: {score:.4f}")
            

if __name__ == "__main__":
    anazhthsh()