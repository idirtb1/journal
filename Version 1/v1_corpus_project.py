import pandas as pd
import json
import urllib.request
import xmltodict
import praw
from datetime import datetime
import time
import csv

# ======================
# Classe BaseDocument
# ======================
class BaseDocument:
    def __init__(self, title, creator, timestamp, content=""):
        self.title = title
        self.creator = creator
        self.timestamp = timestamp
        self.content = content
        self.doc_type = self.identify_type()

    def identify_type(self):
        return "Generic Document"

    def __str__(self):
        return f"{self.title} created by {self.creator} on {self.timestamp} ({self.doc_type})"

# ======================
# Classe RedditPost
# ======================
class RedditPost(BaseDocument):
    def __init__(self, title, creator, timestamp, comments, content=""):
        super().__init__(title, creator, timestamp, content)
        self.comments = comments

    def identify_type(self):
        return "Reddit Post"

    def __str__(self):
        return super().__str__() + f" | Comments: {self.comments}"

# ======================
# Classe ArxivPaper
# ======================
class ArxivPaper(BaseDocument):
    def __init__(self, title, creators, timestamp, content=""):
        super().__init__(title, creators, timestamp, content)
        self.creators = creators

    def identify_type(self):
        return "Arxiv Paper"

    def __str__(self):
        authors_list = ", ".join(self.creators)
        return super().__str__() + f" | Authors: {authors_list}"

# ======================
# Classe DocumentManager
# ======================
class DocumentManager:
    def __init__(self):
        self.doc_list = []

    def add(self, doc):
        self.doc_list.append(doc)

    def show_all(self):
        for doc in self.doc_list:
            print(doc)

# ======================
# Fonction pour extraire les posts Reddit
# ======================
def reddit_posts_extract():
    reddit = praw.Reddit(client_id='y_jUSZ3PH27WkoD6IY52UQ', client_secret='W1KV3UJjFlxRrDla-ZFIvfc_wGkrmw', user_agent='Redit WebScraping', redirect_uri='http://localhost:8080')
    subreddit_posts = reddit.subreddit('Python').top(limit=10)
    extracted_posts = []

    for post in subreddit_posts:
        post_data = f"{post.title} - {post.selftext}"
        extracted_post = RedditPost(
            title=post.title,
            creator=str(post.author) if post.author else "Unknown",
            timestamp=str(datetime.fromtimestamp(post.created_utc)),
            comments=post.num_comments,
            content=post_data
        )
        extracted_posts.append(extracted_post)
    return extracted_posts

# ======================
# Fonction pour extraire les articles Arxiv
# ======================
def arxiv_papers_extract():
    keyword = "Data%20Science"
    url = f'http://export.arxiv.org/api/query?search_query=all:{keyword}&start=0&max_results=10'
    time.sleep(1)

    with urllib.request.urlopen(url) as response:
        arxiv_data = response.read()

    parsed_arxiv_data = xmltodict.parse(arxiv_data)
    extracted_papers = []

    for entry in parsed_arxiv_data['feed']['entry']:
        authors = [entry['author'][0]['name']] if isinstance(entry['author'], list) else [entry['author']['name']]
        extracted_paper = ArxivPaper(
            title=entry['title'],
            creators=authors,
            timestamp=entry['published'],
            content=entry['summary'].replace("\n", " ")
        )
        extracted_papers.append(extracted_paper)
    return extracted_papers

# ======================
# Exemple d'utilisation
# ======================
if __name__ == "__main__":
    doc_manager = DocumentManager()

    # Extraction des données Reddit et Arxiv
    reddit_data = reddit_posts_extract()
    arxiv_data = arxiv_papers_extract()

    # Ajout des documents au gestionnaire
    for document in reddit_data + arxiv_data:
        doc_manager.add(document)

    # Affichage de tous les documents
    doc_manager.show_all()

    # Sauvegarde des documents dans un fichier CSV
    with open("documents_output.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Title", "Creator", "Date", "Type", "Content"])
        for doc in doc_manager.doc_list:
            csv_writer.writerow([doc.title, doc.creator, doc.timestamp, doc.doc_type, doc.content])

    print("\nLes documents ont été enregistrés dans 'documents_output.csv'")