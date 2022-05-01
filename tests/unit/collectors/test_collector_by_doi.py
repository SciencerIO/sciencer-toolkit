from enum import auto
from unittest import TestCase
from sciencer.models import Paper, PaperIDs
from sciencer.collectors import CollectByDOI
from tests.utils import FakeProvider

paper_1_doi = "Paper/1/"
paper_2_doi = "Paper/2/"
invalid_doi = "Invalid/DOI"

paper_1 = Paper("id_1")
paper_1.external_ids.add_id(PaperIDs.LABEL.DOI, paper_1_doi)

paper_2 = Paper("id_2")
paper_2.external_ids.add_id(PaperIDs.LABEL.DOI, paper_2_doi)


class TestCollectorByAuthor(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.__provider = FakeProvider(papers=[paper_1, paper_2])

    def test_collector_by_paper_doi(self):
        collector = CollectByDOI(doi=paper_1_doi)
        collection_result = collector.execute([self.__provider])

        self.assertIn(paper_1, collection_result)
        self.assertNotIn(paper_2, collection_result)

    def test_collector_by_paper_doi_with_invalid_doi(self):
        collector = CollectByDOI(doi=invalid_doi)
        collection_result = collector.execute([self.__provider])

        self.assertEqual(len(collection_result), 0)
