"""Expands paper by its references
"""
from typing import Callable, List, Dict, Set

from ..models import Paper
from ..providers.provider import Provider
from .expander import Expander


class ExpandByReferences(Expander):
    """Class that encapsulates the expansio of a paper by its references

    Args:
        Expander (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__([])

    def execute(self,
                papers: List[Paper],
                providers: List[Provider],
                on_expanded_paper: Callable[[Paper, Paper], None] = None) -> List[Paper]:
        resulting_papers: Set[Paper] = set()

        references_by_referenced_paper: Dict[str, Set[Paper]] = {}
        for paper in papers:
            for reference in paper.references:
                if reference not in references_by_referenced_paper:
                    references_by_referenced_paper[reference] = set()
                references_by_referenced_paper[reference].add(paper)

        for referenced_paper_id, reference_papers in references_by_referenced_paper.items():
            for provider in providers:
                provider_paper = provider.get_paper_by_id(referenced_paper_id)
                if provider_paper is None:
                    continue

                resulting_papers.add(provider_paper)

                if on_expanded_paper is not None:
                    for citation_paper in reference_papers:
                        on_expanded_paper(provider_paper, citation_paper)

        return list(resulting_papers)

    def __str__(self) -> str:
        return "<ExpanmderByReferences>"
