"""Expands paper by its citations
"""
from typing import List
from ..providers.provider import Provider
from .expander import Expander
from ..models import Paper


class ExpandByCitations(Expander):
    """Class that encapsulates the expansion of a paper by its citation
    """

    def __init__(self) -> None:
        super().__init__([])

    def execute(self, papers: List[Paper], providers: List[Provider]) -> List[Paper]:
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

    def __str__(self) -> str:
        return "<ExpandByCitations>"
