"""Expands papers by their authors
"""
from typing import List
from sciencer.policies import Policy
from .expander import Expander
from ..providers.provider import Provider
from ..models import Paper


class ExpandByAuthors(Expander):
    """Class that encapsulates the expansion of papers by their authors"""

    def __init__(self) -> None:
        super().__init__(policies=[Policy.BY_AUTHOR])

    def execute(self, papers: List[Paper], providers: List[Provider]) -> List[Paper]:

        resulting_papers = []

        authors_id = set()

        for paper in papers:
            authors_id.update(paper.authors)
             
        for author_id in authors_id:
            for provider in providers:
                author_papers = provider.get_papers_by_author(author_id)
                if len(author_papers) > 0:
                    resulting_papers.extend(author_papers)
                    break

        return resulting_papers
