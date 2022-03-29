import unittest
from sciencer.models import Paper, PaperIDs


correct_text_value = "CORRECT_VALUE"
correct_number_value = 2000
author_1_id = "XXX"
author_2_id = "YYY"


class TestPaperModel(unittest.TestCase):
    def test_get_id(self):
        paper = Paper(correct_text_value)

        resulting__id = paper.paper_id
        self.assertEqual(resulting__id, correct_text_value)
        
    def test_get_title_after_setting(self):
        paper = Paper("id_1")
        paper.set_title(correct_text_value)

        resulting_title = paper.title
        self.assertEqual(resulting_title, correct_text_value)

    def test_get_title_without_setting(self):
        paper = Paper("id_1")
        resulting_title = paper.title

        self.assertIsNone(resulting_title)

    def test_get_id_doi_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.DOI,correct_text_value)

        resulting_id_doi = paper.get_external_id(PaperIDs.LABEL.DOI)
        self.assertEqual(resulting_id_doi, correct_text_value)

    def test_get_id_doi_without_setting(self):
        paper = Paper("id_1")
        resulting_id_doi = paper.get_external_id(PaperIDs.LABEL.DOI)

        self.assertIsNone(resulting_id_doi)

    def test_get_id_mag_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.MAG,correct_text_value)

        resulting_id_mag = paper.get_external_id(PaperIDs.LABEL.MAG)
        self.assertEqual(resulting_id_mag, correct_text_value)

    def test_get_id_mag_without_setting(self):
        paper = Paper("id_1")
        resulting_id_mag = paper.get_external_id(PaperIDs.LABEL.MAG)

        self.assertIsNone(resulting_id_mag)

    def test_get_id_corpus_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.CORPUS,correct_text_value)

        resulting_id_corpus = paper.get_external_id(PaperIDs.LABEL.CORPUS)
        self.assertEqual(resulting_id_corpus, correct_text_value)

    def test_get_corpus_without_setting(self):
        paper = Paper("id_1")
        resulting_id_corpus = paper.get_external_id(PaperIDs.LABEL.CORPUS)

        self.assertIsNone(resulting_id_corpus)

    def test_get_id_pubmed_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.PUBMED,correct_text_value)

        resulting_id_pubmed = paper.get_external_id(PaperIDs.LABEL.PUBMED)
        self.assertEqual(resulting_id_pubmed, correct_text_value)

    def test_get_pubmed_without_setting(self):
        paper = Paper("id_1")
        resulting_id_pubmed = paper.get_external_id(PaperIDs.LABEL.PUBMED)

        self.assertIsNone(resulting_id_pubmed)

    def test_get_id_dblp_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.DBLP,correct_text_value)

        resulting_id_dblp = paper.get_external_id(PaperIDs.LABEL.DBLP)
        self.assertEqual(resulting_id_dblp, correct_text_value)

    def test_get_dblp_without_setting(self):
        paper = Paper("id_1")
        resulting_id_dblp = paper.get_external_id(PaperIDs.LABEL.DBLP)

        self.assertIsNone(resulting_id_dblp)

    def test_get_id_arxiv_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.ARXIV,correct_text_value)

        resulting_id_arxiv = paper.get_external_id(PaperIDs.LABEL.ARXIV)
        self.assertEqual(resulting_id_arxiv, correct_text_value)

    def test_get_arxiv_without_setting(self):
        paper = Paper("id_1")
        resulting_id_arxiv = paper.get_external_id(PaperIDs.LABEL.ARXIV)

        self.assertIsNone(resulting_id_arxiv)

    def test_get_id_acl_after_setting(self):
        paper = Paper("id_1")
        paper.set_external_id(PaperIDs.LABEL.ACL,correct_text_value)

        resulting_id_acl = paper.get_external_id(PaperIDs.LABEL.ACL)
        self.assertEqual(resulting_id_acl, correct_text_value)

    def test_get_acl_without_setting(self):
        paper = Paper("id_1")
        resulting_id_acl = paper.get_external_id(PaperIDs.LABEL.ACL)

        self.assertIsNone(resulting_id_acl)

    def test_get_abstract_after_setting(self):
        paper = Paper("id_1")
        paper.set_abstract(correct_text_value)

        resulting_abstract = paper.abstract
        self.assertEqual(resulting_abstract, correct_text_value)

    def test_get_abstract_without_setting(self):
        paper = Paper("id_1")
        resulting_abstract = paper.abstract

        self.assertIsNone(resulting_abstract)

    def test_get_year_after_setting(self):
        paper = Paper("id_1")
        paper.set_year(correct_number_value)

        resulting_year = paper.year
        self.assertEqual(resulting_year, correct_number_value)

    def test_get_year_without_setting(self):
        paper = Paper("id_1")
        resulting_year = paper.year

        self.assertIsNone(resulting_year)

    def test_get_authors_after_adding_single_author(self):
        paper = Paper("id_1")
        paper.add_author(author_1_id)

        resulting_authors = paper.authors

        self.assertIn(author_1_id, resulting_authors)

    def test_get_authors_after_adding_multiple_authors(self):
        paper = Paper("id_1")
        paper.add_author(author_1_id)
        paper.add_author(author_2_id)

        resulting_authors = paper.authors

        self.assertIn(author_1_id, resulting_authors)
        self.assertIn(author_2_id, resulting_authors)

    def test_get_authors_after_adding_multiple_authors_single_call(self):
        paper = Paper("id_1")
        paper.add_authors([author_1_id, author_2_id])

        resulting_authors = paper.authors

        self.assertIn(author_1_id, resulting_authors)
        self.assertIn(author_2_id, resulting_authors)

    def test_get_authors_wuthout_adding(self):
        paper = Paper("id_1")

        resulting_authors = paper.authors

        self.assertEqual(len(resulting_authors), 0)

    def test_paper_to_string_with_title(self):
        paper = Paper("id_1")
        paper.set_title(correct_text_value)

        expects = f"<Paper: {correct_text_value}>"

        self.assertEqual(str(paper), expects)
