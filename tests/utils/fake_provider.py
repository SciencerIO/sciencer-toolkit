from typing import List, Optional
from sciencer.policies import Policy
from sciencer.providers.provider import Provider
from sciencer.models import Paper, PaperIDs


class FakeProvider(Provider):
    def __init__(self, papers: List[Paper]) -> None:
        super().__init__([Policy.BY_AUTHOR, Policy.BY_DOI])
        self.__papers = papers

    def get_papers_by_author(self, id: str = "") -> List[Paper]:

        return list(filter(lambda x: id in x.authors_ids, self.__papers))

    def get_paper_by_id(self, id) -> Optional[Paper]:
        resulting_papers = list(filter(lambda x: x.external_ids.get_id(
            PaperIDs.LABEL.DOI) == id or x.paper_id == id, self.__papers))

        if len(resulting_papers) == 0:
            return None

        return resulting_papers[0]

    def get_paper_by_terms(self, terms: List[str], max_papers: int) -> List[Paper]:

        resulting_papers = []
        for paper in self.__papers:
            if paper.abstract is None:
                continue
            elif all(term in paper.abstract for term in terms):
                resulting_papers.append(paper)

        if len(resulting_papers) > max_papers:
            return resulting_papers[max_papers:]

        return resulting_papers

    def update_paper(self, paper: Paper) -> None:
        pass