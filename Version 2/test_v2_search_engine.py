import unittest
from v2_search_engine import BaseDocument, RedditPost, ArxivPaper, DocumentManager, SearchEngine, reddit_posts_extract, arxiv_papers_extract

class TestSearchEngine(unittest.TestCase):
    # ====================
    # Test de la classe BaseDocument
    # ====================
    def test_base_document_creation(self):
        print("[Test] Création d'un BaseDocument...")
        base_doc = BaseDocument("Titre générique", "Auteur Test", "2025-01-01", "Contenu générique")
        self.assertEqual(base_doc.title, "Titre générique")
        self.assertEqual(base_doc.creator, "Auteur Test")
        self.assertEqual(base_doc.timestamp, "2025-01-01")
        self.assertEqual(base_doc.doc_type, "Generic Document")
        print("✔️ BaseDocument créé avec succès.")

    # ====================
    # Test de la classe RedditPost
    # ====================
    def test_reddit_post_creation(self):
        print("[Test] Création d'un RedditPost...")
        reddit_post = RedditPost("Titre Reddit", "Utilisateur Reddit", "2025-01-01", 100, "Contenu Reddit")
        self.assertEqual(reddit_post.title, "Titre Reddit")
        self.assertEqual(reddit_post.creator, "Utilisateur Reddit")
        self.assertEqual(reddit_post.comments, 100)
        self.assertEqual(reddit_post.doc_type, "Reddit Post")
        print("✔️ RedditPost créé avec succès.")

    # ====================
    # Test de la classe ArxivPaper
    # ====================
    def test_arxiv_paper_creation(self):
        print("[Test] Création d'un ArxivPaper...")
        arxiv_paper = ArxivPaper("Titre Arxiv", ["Auteur1", "Auteur2"], "2025-01-01", "Résumé Arxiv")
        self.assertEqual(arxiv_paper.title, "Titre Arxiv")
        self.assertEqual(arxiv_paper.creators, ["Auteur1", "Auteur2"])
        self.assertEqual(arxiv_paper.doc_type, "Arxiv Paper")
        print("✔️ ArxivPaper créé avec succès.")

    # ====================
    # Test de la classe DocumentManager
    # ====================
    def test_document_manager(self):
        print("[Test] Gestion des documents avec DocumentManager...")
        manager = DocumentManager()
        doc1 = RedditPost("Titre1", "Auteur1", "2025-01-01", 10)
        doc2 = ArxivPaper("Titre2", ["Auteur2"], "2025-01-02")
        manager.add(doc1)
        manager.add(doc2)
        self.assertEqual(len(manager.doc_list), 2)
        print("✔️ DocumentManager fonctionne correctement.")

    # ====================
    # Test de l'extraction Reddit
    # ====================
    def test_reddit_posts_extract(self):
        print("[Test] Extraction des posts Reddit...")
        reddit_posts = reddit_posts_extract()
        self.assertGreater(len(reddit_posts), 0)
        self.assertIsInstance(reddit_posts[0], RedditPost)
        print("✔️ Extraction des posts Reddit réussie.")

    # ====================
    # Test de l'extraction Arxiv
    # ====================
    def test_arxiv_papers_extract(self):
        print("[Test] Extraction des articles Arxiv...")
        arxiv_papers = arxiv_papers_extract()
        self.assertGreater(len(arxiv_papers), 0)
        self.assertIsInstance(arxiv_papers[0], ArxivPaper)
        print("✔️ Extraction des articles Arxiv réussie.")

    # ====================
    # Test du moteur de recherche
    # ====================
    def test_search_engine(self):
        print("[Test] Initialisation du moteur de recherche...")
        docs = [
            BaseDocument("Python Tutorial", "John Doe", "2025-01-01", "Learn Python basics"),
            BaseDocument("Advanced Python", "Jane Smith", "2025-02-01", "Master advanced Python techniques"),
            BaseDocument("Data Science", "Alice Brown", "2025-03-01", "Learn data science with Python")
        ]
        search_engine = SearchEngine(docs)
        results = search_engine.search("Python")
        self.assertGreater(len(results), 0)
        print("✔️ Moteur de recherche fonctionne correctement.")

if __name__ == "__main__":
    unittest.main()