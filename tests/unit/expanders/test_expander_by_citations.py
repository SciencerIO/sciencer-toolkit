import unittest
from sciencer.expanders import ExpandByCitations
from sciencer import Paper
from tests.utils import FakeProvider

paper_1_id = "id_1"
paper_1 = Paper(paper_1_id)
paper_2 = Paper("id_2")
source_paper = Paper("id_s")
source_paper.citations_ids.add(paper_1_id)


class TestExpanderByCitations(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.provider = FakeProvider(papers=[source_paper, paper_1, paper_2])

    def test_expander_by_citations(self):
        exp = ExpandByCitations()
        expansion_result = exp.execute(
            [source_paper], providers=[self.provider])

        self.assertEqual(len(expansion_result), 1)
        self.assertIn(paper_1, expansion_result)
