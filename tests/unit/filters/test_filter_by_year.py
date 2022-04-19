import unittest

from sciencer.filters import FilterByYear
from sciencer.models import Paper

PAPER_YEAR = 2010

paper_with_year = Paper("id_wy")
paper_with_year.year = PAPER_YEAR

paper_without_year = Paper("id_woy")


class TestYearFilter(unittest.TestCase):
    def test_year_filter_incorrect_min_and_max(self):
        filter = FilterByYear(PAPER_YEAR + 1, PAPER_YEAR - 1)
        self.assertRaises(Exception)

    def test_year_filter_outside(self):
        filter = FilterByYear(PAPER_YEAR - 2, PAPER_YEAR - 1)
        result = filter.is_valid(paper_with_year)
        self.assertFalse(result)

    def test_year_filter_in_between(self):
        filter = FilterByYear(PAPER_YEAR - 1, PAPER_YEAR + 1)
        result = filter.is_valid(paper_with_year)
        self.assertTrue(result)

    def test_year_filter_with_equal_min_max_and_paper_year(self):
        filter = FilterByYear(PAPER_YEAR, PAPER_YEAR)
        result = filter.is_valid(paper_with_year)
        self.assertTrue(result)

    def test_year_filter_with_equal_min_max_diff_paper_year(self):
        filter = FilterByYear(PAPER_YEAR + 1, PAPER_YEAR + 1)
        result = filter.is_valid(paper_with_year)
        self.assertFalse(result)

    def test_year_filter_with_empty_paper(self):
        filter = FilterByYear(PAPER_YEAR - 1, PAPER_YEAR + 1)
        result = filter.is_valid(paper_without_year)
        self.assertFalse(result)

    def test_paper_with_miminum_year(self):
        filter = FilterByYear(PAPER_YEAR, PAPER_YEAR + 1)
        result = filter.is_valid(paper_with_year)
        self.assertTrue(result)

    def test_paper_with_maximum_year(self):
        filter = FilterByYear(PAPER_YEAR - 1, PAPER_YEAR)
        result = filter.is_valid(paper_with_year)
        self.assertTrue(result)
