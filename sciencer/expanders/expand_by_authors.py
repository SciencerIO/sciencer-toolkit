"""Expands papers by their authors
"""
from typing import Callable,  List, Dict, Set

from sciencer.policies import Policy

from ..models import Paper
from ..providers.provider import Provider
from .expander import Expander


class ExpandByAuthors(Expander):
    """Class that encapsulates the expansion of papers by their authors"""

    def __init__(self) -> None:
        super().__init__(policies=[Policy.BY_AUTHOR])

    def execute(self,
                papers: List[Paper],
                providers: List[Provider],
                on_expanded_paper: Callable[[Paper, Paper], None] = None) -> List[Paper]:

        resulting_papers: Set[Paper] = set()

        papers_by_authors: Dict[str, Set[Paper]] = {}

        for paper in papers:
            for author_id in paper.authors:
                if author_id not in papers_by_authors:
                    papers_by_authors[author_id] = set()
                papers_by_authors[author_id].add(paper)

        for author_id, author_papers in papers_by_authors.items():
            for provider in providers:
                retrieved_author_papers = provider.get_papers_by_author(
                    author_id)

                if len(retrieved_author_papers) == 0:
                    continue

                resulting_papers.update(retrieved_author_papers)

                if on_expanded_paper is not None:
                    for paper in retrieved_author_papers:
                        for author_paper in author_papers:
                            on_expanded_paper(paper, author_paper)

        return list(resulting_papers)

    def __str__(self) -> str:
        return "<ExpandByAuthors>"
