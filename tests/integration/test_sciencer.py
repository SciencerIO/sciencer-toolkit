from unittest import TestCase
from sciencer.collectors.collect_by_doi import CollectByDOI
from sciencer.models import Paper, PaperIDs
from sciencer.expanders import ExpandByAuthors
from sciencer.filters import FilterByYear
from sciencer import Sciencer
from tests.utils import FakeProvider

class TestSciencer(TestCase):
    def setUp(self) -> None:
        self.__author = "author_name"
        self.__paper_1_doi = "Paper/DOI/1"
        self.__paper_2_year = 2010
        self.__paper_3_year = self.__paper_2_year - 50

        self.__paper_1 = Paper("id_1")
        self.__paper_1.add_author(self.__author)
        self.__paper_1.set_external_id(PaperIDs.LABEL.DOI, self.__paper_1_doi)

        self.__paper_2 = Paper("id_2")
        self.__paper_2.add_author(self.__author)
        self.__paper_2.set_external_id(PaperIDs.LABEL.DOI,"Paper/DOI/2")
        self.__paper_2.set_year(self.__paper_2_year)

        self.__paper_3 = Paper("id_3")
        self.__paper_3.add_author(self.__author)
        self.__paper_3.set_external_id(PaperIDs.LABEL.DOI,"Paper/DOI/3")
        self.__paper_3.set_year(self.__paper_3_year)

        self.__provider = FakeProvider(
            papers=[self.__paper_1, self.__paper_2, self.__paper_3]
        )

    def test_scenario_1(self):
        s = Sciencer()
        s.add_provider(self.__provider)
        s.add_collector(CollectByDOI(self.__paper_1_doi))
        s.add_expander(ExpandByAuthors())
        s.add_filter(
            FilterByYear(
                min_year=self.__paper_2_year - 1, max_year=self.__paper_2_year + 1
            )
        )

        results = s.iterate()

        self.assertEqual(len(results), 1)
        self.assertIn(self.__paper_2, results)
