import pandas as pd
import json
import urllib.request
import xmltodict
import praw
from datetime import datetime
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, messagebox

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
        return "Document générique"

    def __str__(self):
        return f"{self.title} créé par {self.creator} le {self.timestamp} ({self.doc_type})"

# ======================
# Classe RedditPost
# ======================
class RedditPost(BaseDocument):
    def __init__(self, title, creator, timestamp, comments, content=""):
        super().__init__(title, creator, timestamp, content)
        self.comments = comments

    def identify_type(self):
        return "Post Reddit"

    def __str__(self):
        return super().__str__() + f" | Commentaires : {self.comments}"

# ======================
# Classe ArxivPaper
# ======================
class ArxivPaper(BaseDocument):
    def __init__(self, title, creators, timestamp, content=""):
        super().__init__(title, creators, timestamp, content)
        self.creators = creators

    def identify_type(self):
        return "Article Arxiv"

    def __str__(self):
        authors_list = ", ".join(self.creators)
        return super().__str__() + f" | Auteurs : {authors_list}"

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
# Classe SearchEngine
# ======================
class SearchEngine:
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.doc_matrix = self.vectorizer.fit_transform([doc.content for doc in self.documents])

    def search(self, query):
        query_vec = self.vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vec, self.doc_matrix).flatten()
        results = [(self.documents[i], similarity_scores[i]) for i in range(len(self.documents)) if similarity_scores[i] > 0]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

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
            creator=str(post.author) if post.author else "Inconnu",
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
# Interface Graphique (Tkinter)
# ======================
class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moteur de Recherche")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.configure(bg="#e0f7fa")

        self.document_manager = DocumentManager()
        self.search_engine = None

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#004d40", foreground="white", font=("Arial", 10, "bold"))
        style.configure("TFrame", background="#e0f7fa")

        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.text_area = tk.Text(main_frame, wrap=tk.WORD, width=90, height=25, bg="#ffffff", fg="#333333", font=("Arial", 12))
        self.text_area.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        self.query_entry = ttk.Entry(main_frame, width=50, font=("Arial", 12))
        self.query_entry.grid(row=1, column=0, pady=10, sticky="ew")

        search_button = ttk.Button(main_frame, text="🔍 Rechercher", command=self.run_search)
        search_button.grid(row=1, column=1, pady=10, padx=5)

        load_reddit_button = ttk.Button(main_frame, text="📥 Charger Reddit", command=self.load_reddit_data)
        load_reddit_button.grid(row=2, column=0, pady=10, sticky="ew")

        load_arxiv_button = ttk.Button(main_frame, text="📥 Charger Arxiv", command=self.load_arxiv_data)
        load_arxiv_button.grid(row=2, column=1, pady=10, sticky="ew")

        stats_button = ttk.Button(main_frame, text="📊 Statistiques", command=self.show_stats)
        stats_button.grid(row=3, column=0, pady=10, sticky="ew")

        reset_button = ttk.Button(main_frame, text="🧹 Réinitialiser", command=self.reset_text_area)
        reset_button.grid(row=3, column=1, pady=10, sticky="ew")

        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def load_reddit_data(self):
        reddit_data = reddit_posts_extract()
        for document in reddit_data:
            self.document_manager.add(document)
        self.text_area.insert(tk.END, "Données Reddit chargées avec succès.\n")
        self.text_area.see(tk.END)

    def load_arxiv_data(self):
        arxiv_data = arxiv_papers_extract()
        for document in arxiv_data:
            self.document_manager.add(document)
        self.text_area.insert(tk.END, "Données Arxiv chargées avec succès.\n")
        self.text_area.see(tk.END)

    def run_search(self):
        query = self.query_entry.get()
        if not self.search_engine:
            self.search_engine = SearchEngine(self.document_manager.doc_list)
        results = self.search_engine.search(query)
        self.text_area.insert(tk.END, "\n--- Résultats de la Recherche ---\n")
        if results:
            for doc, score in results:
                self.text_area.insert(tk.END, f"{doc} | Score : {score:.4f}\n")
        else:
            self.text_area.insert(tk.END, "Aucun résultat trouvé.\n")
        self.text_area.see(tk.END)

    def show_stats(self):
        num_docs = len(self.document_manager.doc_list)
        num_reddit = sum(1 for doc in self.document_manager.doc_list if doc.doc_type == "Post Reddit")
        num_arxiv = sum(1 for doc in self.document_manager.doc_list if doc.doc_type == "Article Arxiv")

        self.text_area.insert(tk.END, f"\n--- Statistiques ---\n")
        self.text_area.insert(tk.END, f"Nombre total de documents : {num_docs}\n")
        self.text_area.insert(tk.END, f"Documents Reddit : {num_reddit}\n")
        self.text_area.insert(tk.END, f"Documents Arxiv : {num_arxiv}\n")
        self.text_area.see(tk.END)

    def reset_text_area(self):
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()