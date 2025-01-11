

import json


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string


#Αρχικοποίηση εργαλείων
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

#Φόρτωση άρθρων από το αρχείο JSON
with open('wikipedia_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    
#Συνάρτηση για την προεπεξεργασία κειμένου
def preprocess_text(text):
    #Μετατροπή σε πεζά και Tokenization
    tokens = word_tokenize(text.lower())
    
    #Αφαίρεση σημείων στίξης
    tokens = [word for word in tokens if word not in string.punctuation]
    
    #Αφαίρεση stop words 
    fil_tokens = [word for word in tokens if word not in stop_words]
    
    #Lemmatization
    lem_tokens = [lemmatizer.lemmatize(word) for word in fil_tokens]
    
    return lem_tokens
    
#Δημιουργία του επεξεργασμένου αρχείου
processed_articles = []

#Εφαρμογή της προεπεξεργασίας σε όλα τα άρθρα και υπολογισμός στατιστικών
for article in articles:
    processed_content = preprocess_text(article['content'])
    processed_articles.append({
        'title': article['title'],
        'processed_content': processed_content})
    
    
#Αποθήκευση των επεξεργασμένων άρθρων σε νέο αρχείο JSON
with open('processed_wikipedia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(processed_articles, f, ensure_ascii=False, indent=4)
    
print("Η προεπεξεργασία και τα στατιστικά των άρθρων ολοκληρώθηκαν και αποθηκεύτηκαν στο 'processed_wikipedia_articles.json'.")
    