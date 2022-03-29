from unittest import TestCase
from sciencer import Sciencer
from sciencer.models import Paper
from sciencer.collectors import CollectByAuthorID
from tests.utils import FakeProvider

paper_1_doi = "Paper/1"
author_1_id = "author_1_id"
author_1_name = "author_1_name"

paper_1 = Paper("id_1")
paper_1.add_author(author_1_id)
paper_1.set_external_id("DOI",paper_1_doi)


class TestSciencerIterations(TestCase):
    def setUp(self) -> None:
        self.__provider = FakeProvider(papers=[paper_1])

    def test_iterate_empty_sciencer(self):
        sciencer = Sciencer()
        resulting_papers = sciencer.iterate()
        self.assertEqual(len(resulting_papers), 0)

    def test_iterate_with_collector_include_source_from_results(self):
        sciencer = Sciencer()

        sciencer.add_provider(self.__provider)
        sciencer.add_collector(CollectByAuthorID(author_1_id))
        resulting_papers = sciencer.iterate(remove_source_from_results=False)

        self.assertEqual(len(resulting_papers), 1)
        self.assertIn(paper_1, resulting_papers)

    def test_iterate_with_collector_excluding_source_from_results(self):
        sciencer = Sciencer()

        sciencer.add_provider(self.__provider)
        sciencer.add_collector(CollectByAuthorID(author_1_id))
        resulting_papers = sciencer.iterate(remove_source_from_results=True)

        self.assertEqual(len(resulting_papers), 0)

    def test_iterate_with_explicit_sources_include_source_from_results(self):
        sciencer = Sciencer()
        sciencer.add_provider(self.__provider)
        resulting_papers = sciencer.iterate(
            source_papers=[paper_1], remove_source_from_results=False
        )

        self.assertEqual(len(resulting_papers), 1)
        self.assertIn(paper_1, resulting_papers)

    def test_iterate_with_explicit_sources_exclude_source_from_results(self):
        sciencer = Sciencer()

        sciencer.add_provider(self.__provider)
        sciencer.add_collector(CollectByAuthorID(author_1_id))
        resulting_papers = sciencer.iterate(
            source_papers=[paper_1], remove_source_from_results=True
        )

        self.assertEqual(len(resulting_papers), 0)
