"""Expands paper by its citations
"""
from typing import Callable,  List

from ..models import Paper
from ..providers.provider import Provider
from .expander import Expander


class ExpandByCitations(Expander):
    """Class that encapsulates the expansion of a paper by its citation
    """

    def __init__(self) -> None:
        super().__init__([])

    def execute(self,
                papers: List[Paper],
                providers: List[Provider],
                on_expanded_paper: Callable[[Paper, Paper], None] = None) -> List[Paper]:
        resulting_papers = set()

        cited_papers_ids = set()
        for paper in papers:
            cited_papers_ids.update(paper.citations)

        for paper_id in cited_papers_ids:
            for provider in providers:
                provider_paper = provider.get_paper_by_id(paper_id)
                if provider_paper is not None:
                    resulting_papers.add(provider_paper)
                    break

        return list(resulting_papers)
