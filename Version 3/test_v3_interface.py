import unittest
from v3_interface import BaseDocument, RedditPost, ArxivPaper, DocumentManager, SearchEngine

class TestDocumentClasses(unittest.TestCase):
    # ====================
    # Test de la classe BaseDocument
    # ====================
    def test_base_document_creation(self):
        print("[Test] Création d'un BaseDocument...")
        base_doc = BaseDocument("Titre générique", "Auteur Test", "2025-01-01", "Contenu générique")
        self.assertEqual(base_doc.title, "Titre générique")
        self.assertEqual(base_doc.creator, "Auteur Test")
        self.assertEqual(base_doc.timestamp, "2025-01-01")
        self.assertEqual(base_doc.doc_type, "Document générique")
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
        self.assertEqual(reddit_post.doc_type, "Post Reddit")
        print("✔️ RedditPost créé avec succès.")

    # ====================
    # Test de la classe ArxivPaper
    # ====================
    def test_arxiv_paper_creation(self):
        print("[Test] Création d'un ArxivPaper...")
        arxiv_paper = ArxivPaper("Titre Arxiv", ["Auteur1", "Auteur2"], "2025-01-01", "Résumé Arxiv")
        self.assertEqual(arxiv_paper.title, "Titre Arxiv")
        self.assertEqual(arxiv_paper.creators, ["Auteur1", "Auteur2"])
        self.assertEqual(arxiv_paper.doc_type, "Article Arxiv")
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
    # Test du moteur de recherche
    # ====================
    def test_search_engine(self):
        print("[Test] Fonctionnement du moteur de recherche...")
        doc1 = BaseDocument("Python Basics", "Auteur1", "2025-01-01", "Apprendre Python")
        doc2 = BaseDocument("Machine Learning", "Auteur2", "2025-01-02", "Apprentissage automatique")
        search_engine = SearchEngine([doc1, doc2])

        results = search_engine.search("Python")
        self.assertGreater(len(results), 0)
        self.assertIn(doc1, [doc for doc, _ in results])
        print("✔️ Moteur de recherche fonctionne correctement.")

if __name__ == "__main__":
    unittest.main()