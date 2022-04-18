import unittest
from sciencer.models import PaperIDs
from sciencer.providers import SemanticScholarProvider
from sciencer.providers.provider import Provider

# Author: Oren Etzioni
# Visited on 25/03/2022
author_id = "40603865"
author_number_papers = 380

# Papers:
# Visited on 18/03/2022
paper_1_id = "649def34f8be52c8b66281af98ae884c09aef38b"
paper_1_externalIds = {
    "MAG": "2952867657",
    "ACL": "N18-3011",
    "ArXiv": "1805.02262",
    "DBLP": "journals/corr/abs-1805-02262",
    "DOI": "10.18653/v1/N18-3011",
    "CorpusId": 19170988,
}
paper_2_id = "5e85252690f51f2e9f209a69961ee9d079413ca0"
paper_2_externalIds = {
    "PubMedCentral": "2323736",
    "CorpusId": 7078715,
    "PubMed": "19872477",
}

# Terms:
# Visited on 29/03/2022
search_terms = ["literature", "graph", "semantic", "scholar"]
search_result_title = "Construction of the Literature Graph in Semantic Scholar"


class TestSemanticScholarProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.__provider: Provider = SemanticScholarProvider()

    def test_author_papers(self):

        papers = self.__provider.get_papers_by_author(author_id)

        self.assertEqual(len(papers), author_number_papers)

    def test_retrieved_paper_externalIds_when_fetching_papers_by_id(self):

        paper_1_result = self.__provider.get_paper_by_id(paper_1_id)
        self.assertIsNotNone(paper_1_result)

        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.MAG), paper_1_externalIds["MAG"])
        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.ACL), paper_1_externalIds["ACL"])
        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.ARXIV), paper_1_externalIds["ArXiv"])
        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.DBLP), paper_1_externalIds["DBLP"])
        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.DOI), paper_1_externalIds["DOI"])
        self.assertEqual(paper_1_result.get_external_id(
            PaperIDs.LABEL.CORPUS), paper_1_externalIds["CorpusId"])

        paper_2_result = self.__provider.get_paper_by_id(paper_2_id)
        self.assertIsNotNone(paper_2_result)

        self.assertEqual(paper_2_result.get_external_id(
            PaperIDs.LABEL.PUBMED), paper_2_externalIds["PubMed"])
        self.assertEqual(paper_2_result.get_external_id(
            PaperIDs.LABEL.CORPUS), paper_2_externalIds["CorpusId"])
