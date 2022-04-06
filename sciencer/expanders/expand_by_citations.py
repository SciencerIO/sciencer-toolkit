"""Expands paper by its citations
"""
from typing import Callable,  List, Dict, Set

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
        resulting_papers: Set[Paper] = set()

        citations_by_cited_paper: Dict[str, Set[Paper]] = {}
        for paper in papers:
            for citation in paper.citations:
                if citation not in citations_by_cited_paper:
                    citations_by_cited_paper[citation] = set()
                citations_by_cited_paper[citation].add(paper)

        for cited_paper_id, citation_papers in citations_by_cited_paper.items():
            for provider in providers:
                provider_paper = provider.get_paper_by_id(cited_paper_id)

                if provider_paper is None:
                    continue

                resulting_papers.add(provider_paper)
                if on_expanded_paper is not None:
                    for citation_paper in citation_papers:
                        on_expanded_paper(provider_paper, citation_paper)

        return list(resulting_papers)

    def __str__(self) -> str:
        return "<ExpandByCitations>"
