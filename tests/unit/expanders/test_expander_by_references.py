import unittest
from sciencer.expanders import ExpandByReferences
from sciencer import Paper
from tests.utils import FakeProvider

paper_1 = Paper("id_1")
paper_2 = Paper("id_2")
source_paper = Paper("id_s")
source_paper.add_reference(paper_1.paper_id)


class TestExpanderByReferences(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.provider = FakeProvider(papers=[source_paper, paper_1, paper_2])

    def test_expander_by_references(self):
        exp = ExpandByReferences()
        expansion_result = exp.execute(
            [source_paper], providers=[self.provider])

        self.assertEqual(len(expansion_result), 1)
        self.assertIn(paper_1, expansion_result)


if __name__ == "__main__":
    t = TestExpanderByReferences()
    t.setUp()
    t.test_expander_by_references()
