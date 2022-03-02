import unittest
from sciencer.expanders import ExpandByAuthors
from sciencer import Paper
from tests.utils import FakeProvider

author_1_id = "author_1"
author_2_id = "author_2"

paper_1 = Paper("id_1")
paper_1.add_author(author_1_id)
paper_1.add_author(author_2_id)

paper_2 = Paper("id_2")
paper_2.add_author(author_1_id)

source_paper = Paper("id_s")
source_paper.add_author(author_2_id)


class TestExpanderByAuthor(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.provider = FakeProvider(papers=[source_paper, paper_1, paper_2])

    def test_expander_by_author(self):
        exp = ExpandByAuthors()
        expansion_result = exp.execute([source_paper], providers=[self.provider])

        self.assertIn(source_paper, expansion_result)
        self.assertIn(paper_1, expansion_result)
        self.assertNotIn(paper_2, expansion_result)
