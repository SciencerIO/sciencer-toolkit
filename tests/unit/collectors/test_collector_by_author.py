from unittest import TestCase
from sciencer.models import Paper
from sciencer.collectors import CollectByAuthorID
from tests.utils import FakeProvider

author_1_id = "author_1"

author_2_id = "author_2"

paper_1 = Paper("id_1")
paper_1.authors_ids.add(author_1_id)
paper_1.authors_ids.add(author_2_id)

paper_2 = Paper("id_2")
paper_2.authors_ids.add(author_1_id)


class TestCollectorByAuthor(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.__provider = FakeProvider(
            papers=[paper_1, paper_2],
        )

    def test_collector_by_author_id(self):
        collector = CollectByAuthorID(author_2_id)
        collection_result = collector.execute([self.__provider])

        self.assertIn(paper_1, collection_result)
        self.assertNotIn(paper_2, collection_result)
