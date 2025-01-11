from bs4 import BeautifulSoup
import requests
import json

#Συνάρτηση για την συλλογή άρθρων από Wikipedia 
def fetch_wikipedia_article(url): 
    response = requests.get(url)
    if response.status_code==200: 
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        
        #Ανάκτηση τίτλου και περιεχομένου
        title = soup.find('h1').text
        paragraphs = [p.text for p in soup.find_all('p')]
        content = ' '.join(paragraphs)
        
        return {'title': title, 'content': content}
    else: 
        print(f"Failed to fetch article: {url}")
        return None
    
#Λίστα με URLs άρθρων από τη Wikipedia
wikipedia_urls =[
    'https://en.wikipedia.org/wiki/Web_scraping',
    'https://en.wikipedia.org/wiki/Data_science',
    'https://en.wikipedia.org/wiki/Information_retrieval',
    'https://en.wikipedia.org/wiki/Data_mining',
    'https://en.wikipedia.org/wiki/Cluster_analysis',
    'https://en.wikipedia.org/wiki/Information_extraction',
    'https://en.wikipedia.org/wiki/Knowledge_extraction',
    'https://en.wikipedia.org/wiki/Search_engine',
    'https://en.wikipedia.org/wiki/Comparison_of_search_engines',
    'https://en.wikipedia.org/wiki/List_of_search_engines',
    'https://en.wikipedia.org/wiki/Search_engine_optimization',
    'https://en.wikipedia.org/wiki/Search_engine_scraping',
    'https://en.wikipedia.org/wiki/Conversion_rate_optimization',
    'https://en.wikipedia.org/wiki/A/B_testing',
    'https://en.wikipedia.org/wiki/Personalization#Web_pages',
    'https://en.wikipedia.org/wiki/Big_data',
    'https://en.wikipedia.org/wiki/Data_engineering',
    'https://en.wikipedia.org/wiki/Software_engineering',
    'https://en.wikipedia.org/wiki/Computer_science',
    'https://en.wikipedia.org/wiki/Software_development',
    'https://en.wikipedia.org/wiki/Systems_analyst',
    'https://en.wikipedia.org/wiki/Data_analysis',
    'https://en.wikipedia.org/wiki/Machine_learning',
    'https://en.wikipedia.org/wiki/Deep_learning',
    'https://en.wikipedia.org/wiki/Open_data'
    ]

#Συλλογή άρθρων
articles = []
for url in wikipedia_urls: 
    article = fetch_wikipedia_article(url)
    if article:
        articles.append(article)
        
#Αποθήκευση δεδομένων σε αρχείο JSON 
with open('wikipedia_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
    
print("Τα άρθρα συλλέχθησαν και αποθηκεύτηκαν επιτυχώς στο αρχειο 'wikipedia_articles.json'.")
