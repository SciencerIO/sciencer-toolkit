from typing import List, Optional
from sciencer.policies import Policy
from sciencer.providers.provider import Provider
from sciencer.models import Paper


class FakeProvider(Provider):
    def __init__(self, papers: List[Paper]) -> None:
        super().__init__([Policy.BY_AUTHOR, Policy.BY_DOI])
        self.__papers = papers

    def get_papers_by_author(self, id: str = "") -> List[Paper]:

        return list(filter(lambda x: id in x.authors, self.__papers))

    def get_paper_by_id(self, id) -> Optional[Paper]:
        resulting_papers = list(filter(lambda x: x.doi == id, self.__papers))

        if len(resulting_papers) == 0:
            return None

        return resulting_papers[0]

    def get_paper_by_terms(self, terms: List[Paper], max_papers: int) -> List[Paper]:
        return []
