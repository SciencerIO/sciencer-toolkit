import unittest

from sciencer.filters import FilterByFieldOfStudy
from sciencer.models import Paper

CORRECT_WORD = "correct"
INCORRECT_WORD = "incorrect"

FIELDS_OF_STUDY_WITH_CORRECT = [CORRECT_WORD]
FIELDS_OF_STUDY_WITHOUT_CORRECT = [INCORRECT_WORD]

paper_with_correct_fields_of_study = Paper("id_wc")
paper_with_correct_fields_of_study.add_field_of_study(CORRECT_WORD)

paper_without_correct_fields_of_study = Paper("id_woc")
paper_without_correct_fields_of_study.add_field_of_study(
    INCORRECT_WORD)

paper_with_default_fields_of_study = Paper("wc_da")


class TestYearFilter(unittest.TestCase):
    def test_correct_field_in_fields_of_study_with_correct(self):
        filter = FilterByFieldOfStudy(field_of_study=CORRECT_WORD)
        result = filter.is_valid(paper_with_correct_fields_of_study)
        self.assertTrue(result)

    def test_incorrect_field_in_fields_of_study_with_correct(self):
        filter = FilterByFieldOfStudy(field_of_study=INCORRECT_WORD)
        result = filter.is_valid(paper_with_correct_fields_of_study)
        self.assertFalse(result)

    def test_correct_field_in_fields_of_study_without_correct(self):
        filter = FilterByFieldOfStudy(field_of_study=CORRECT_WORD)
        result = filter.is_valid(paper_without_correct_fields_of_study)
        self.assertFalse(result)

    def test_incorrect_field_in_fields_of_study_without_correct(self):
        filter = FilterByFieldOfStudy(field_of_study=INCORRECT_WORD)
        result = filter.is_valid(paper_without_correct_fields_of_study)
        self.assertTrue(result)

    def test_field_in_default_fields_of_study(self):
        filter = FilterByFieldOfStudy(field_of_study=CORRECT_WORD)
        result = filter.is_valid(paper_with_default_fields_of_study)
        self.assertFalse(result)

    def test_field_in_empty_fields_of_study(self):
        filter = FilterByFieldOfStudy(field_of_study=CORRECT_WORD)
        result = filter.is_valid(paper_with_default_fields_of_study)
        self.assertFalse(result)
