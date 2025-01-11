
import json
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score
from search_idle import search_tfidf, search_bm25, search_vsm

#Υποθετική λίστα φράσεων για κάθε ερώτημα
relevant_docs = {
    "web scraping": [0],
    "data science": [1], 
    "information retrieval": [2],
    "data mining": [3],
    "cluster analysis": [4],
    "information extraction": [5],
    "knowledge extraction": [6],
    "machine learning": [7],
    "deep learning": [8],
    "big data": [9]
    }

#Φόρτωση των άρθρων και της μηχανής αναζήτησης
with open('processed_wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Συνάρτηση για τον υπολογισμό της ακρίβειας, ανάκλησης και του F1-score
def aksiologisi_question(relevant, retrieved_docs):
    #Βρίσκουμε τα έγγραφα που σχετίζονται απο την ανάκτηση
    y_true = [1 if doc in relevant else 0 for doc in range(len(articles))]
    y_pred = [1 if doc in retrieved_docs else 0 for doc in range(len(articles))]
    
    #Υπολογισμός της ακρίβειας, ανάκλησης και F1-score
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    #MAP
    ap = average_precision_score(y_true, y_pred)
    
    return precision, recall, f1, ap

#Συνάρτηση για την αξιολόγηση της μηχανής αναζήτησης
def aksiologisi_mixanis_anazitisis():
    for retrieval_name, retrieval_function in {
            "TF-IDF": search_tfidf,
            "Okapi BM25": search_bm25,
            "Vector Space Model (VSM)": search_vsm}.items():
        print(f"Αξιολόγηση με {retrieval_name}")
        total_prec, total_rec, total_f1, total_ap = 0, 0, 0, 0
    
        for question, relevant in relevant_docs.items():
            question_term = " ".join(question.split())
            #Ανάκτηση εγγράφων
            retrieved = retrieval_function(question_term) 
            retrieved_docs = [doc_id for doc_id, _ in retrieved[:10]]
            
            precision, recall, f1_score, ap = aksiologisi_question(relevant, retrieved_docs)
            total_prec += precision
            total_rec += recall
            total_f1 += f1_score
            total_ap += ap
        
            print(f"Ακρίβεια: {precision:.2f}, Ανάκληση: {recall:.2f}, F1-score: {f1_score:.2f}, AP: {ap:.2f}.")
        
    
    #Μέσοι όροι
    avg_prec = total_prec / len(relevant_docs)
    avg_rec = total_rec / len(relevant_docs)
    avg_f1  = total_f1 / len(relevant_docs)
    avg_ap = total_ap / len(relevant_docs)
    
    print(f"Μέση Ακρίβεια: {avg_prec:.2f}, Μέση Ανάκληση: {avg_rec:.2f}, Μέσο F1-score: {avg_f1:.2f}, Μέσο MAP: {avg_ap:.2f}\n")
    
    
#Εκτέλεση της αξιολόγησης
aksiologisi_mixanis_anazitisis()
