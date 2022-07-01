import unittest

from sciencer.filters import FilterByCitations
from sciencer.models import Paper

PAPER_CITATIONS = 100

paper_with_citations = Paper("id_with_citations")
for i in range(0,PAPER_CITATIONS):
    paper_with_citations.citations_ids.add(f"cited_paper_{i}")

paper_without_citations = Paper("id_without_citations")

class TestCitationsFilter(unittest.TestCase):
    def test_citations_filter_incorrect_min_and_max(self):
        filter = FilterByCitations(PAPER_CITATIONS + 1, PAPER_CITATIONS - 1)
        self.assertRaises(Exception)

    def test_citations_filter_outside(self):
        filter = FilterByCitations(PAPER_CITATIONS - 2, PAPER_CITATIONS - 1)
        result = filter.is_valid(paper_with_citations)
        self.assertFalse(result)

    def test_citations_filter_in_between(self):
        filter = FilterByCitations(PAPER_CITATIONS - 1, PAPER_CITATIONS + 1)
        result = filter.is_valid(paper_with_citations)
        self.assertTrue(result)

    def test_citations_filter_with_equal_min_max_and_paper_citations(self):
        filter = FilterByCitations(PAPER_CITATIONS, PAPER_CITATIONS)
        result = filter.is_valid(paper_with_citations)
        self.assertTrue(result)

    def test_citations_filter_with_equal_min_max_diff_paper_citations(self):
        filter = FilterByCitations(PAPER_CITATIONS + 1, PAPER_CITATIONS + 1)
        result = filter.is_valid(paper_with_citations)
        self.assertFalse(result)

    def test_citations_filter_with_empty_paper(self):
        filter = FilterByCitations(PAPER_CITATIONS - 1, PAPER_CITATIONS + 1)
        result = filter.is_valid(paper_without_citations)
        self.assertFalse(result)

    def test_paper_with_miminum_year(self):
        filter = FilterByCitations(PAPER_CITATIONS, PAPER_CITATIONS + 1)
        result = filter.is_valid(paper_with_citations)
        self.assertTrue(result)

    def test_paper_with_maximum_year(self):
        filter = FilterByCitations(PAPER_CITATIONS - 1, PAPER_CITATIONS)
        result = filter.is_valid(paper_with_citations)
        self.assertTrue(result)
