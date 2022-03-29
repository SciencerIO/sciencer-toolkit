from unittest import TestCase
from sciencer.collectors import CollectByTerms
from sciencer.models import Paper
from tests.utils import FakeProvider

paper_abstract_term_1 = "term1"
paper_abstract_term_2 = "term2"
paper_abstract_term_3 = "term3"
paper_abstract_non_existent = "termX"

paper_1_abstract = "termR1 termR2 termR3 " + \
    paper_abstract_term_1 + " " + paper_abstract_term_2
paper_2_abstract = "termR1 termR2 termR3 " + \
    paper_abstract_term_3

paper_1 = Paper("")
paper_1.set_abstract(paper_1_abstract)

paper_2 = Paper("")
paper_2.set_abstract(paper_2_abstract)

paper_3 = Paper("")
paper_3.set_abstract(paper_2_abstract)


class TestCollectorByAuthor(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__provider = FakeProvider(papers=[paper_1, paper_2, paper_3])

    def test_collector_using_single_term_when_terms_exist(self):
        collector = CollectByTerms(terms=[paper_abstract_term_3])
        result = collector.execute(providers=[self.__provider])

        self.assertEqual(len(result), 2)
        self.assertIn(paper_2, result)
        self.assertIn(paper_3, result)

    def test_collector_using_multiple_terms_when_terms_exist(self):
        collector = CollectByTerms(
            terms=[paper_abstract_term_1, paper_abstract_term_2])
        result = collector.execute(providers=[self.__provider])

        self.assertEqual(len(result), 1)
        self.assertIn(paper_1, result)

    def test_collector_using_single_term_when_terms_does_not_exist(self):
        collector = CollectByTerms(
            terms=[paper_abstract_non_existent])
        result = collector.execute(providers=[self.__provider])

        self.assertEqual(len(result), 0)

    def test_collector_limiting_results(self):
        collector = CollectByTerms(
            terms=[paper_abstract_term_3], max_papers=1)
        result = collector.execute(providers=[self.__provider])

        self.assertEqual(len(result), 1)

    def test_collector_wrong_maxpapers_value(self):
        with self.assertRaises(Exception):
            CollectByTerms(terms=[paper_abstract_term_3], max_papers=100000)
