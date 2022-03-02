import unittest

from sciencer.filters import FilterByAbstract
from sciencer.models import Paper

CORRECT_WORD = "correct"
INCORRECT_WORD = "incorrect"

ABSTRACT_WITH_CORRECT = "Hello " + CORRECT_WORD + " world"
ABSTRACT_WITHOUT_CORRECT = "Hello empty world"

paper_with_abstract_with_correct = Paper("id_wc")
paper_with_abstract_with_correct.set_abstract(ABSTRACT_WITH_CORRECT)

paper_with_abstract_without_correct = Paper("id_woc")
paper_with_abstract_without_correct.set_abstract(ABSTRACT_WITHOUT_CORRECT)

paper_with_default_abstract = Paper("wc_da")

paper_with_empty_abstract = Paper("wc_em")
paper_with_empty_abstract.set_abstract("")


class TestYearFilter(unittest.TestCase):
    def test_correct_word_in_abstract_with_correct(self):
        filter = FilterByAbstract(word=CORRECT_WORD)
        result = filter.is_valid(paper_with_abstract_with_correct)
        self.assertTrue(result)

    def test_incorrect_word_in_abstract_with_correct(self):
        filter = FilterByAbstract(word=INCORRECT_WORD)
        result = filter.is_valid(paper_with_abstract_with_correct)
        self.assertFalse(result)

    def test_correct_word_in_abstract_without_correct(self):
        filter = FilterByAbstract(word=CORRECT_WORD)
        result = filter.is_valid(paper_with_abstract_without_correct)
        self.assertFalse(result)

    def test_incorrect_word_in_abstract_without_correct(self):
        filter = FilterByAbstract(word=INCORRECT_WORD)
        result = filter.is_valid(paper_with_abstract_without_correct)
        self.assertFalse(result)

    def test_word_in_default_abstract(self):
        filter = FilterByAbstract(word=CORRECT_WORD)
        result = filter.is_valid(paper_with_default_abstract)
        self.assertFalse(result)

    def test_word_in_empty_abstract(self):
        filter = FilterByAbstract(word=CORRECT_WORD)
        result = filter.is_valid(paper_with_empty_abstract)
        self.assertFalse(result)
