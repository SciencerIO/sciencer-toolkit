"""Collect Papers by Dkeywords
"""
from typing import List

from ..providers.provider import Provider
from ..policies import Policy
from .collector import Collector
from ..models import Paper


class CollectByTerms(Collector):
    """Class that encapsulates the collection of a papers with certain terms"""

    def __init__(self, terms: List[str], max_papers: int = 100) -> None:
        if max_papers > 9999:
            raise Exception(
                f"Collector by terms can only return a maxiumum of 9999. \
                    {max_papers} were requested.")

        super().__init__([Policy.BY_QUERY, Policy.BY_DOI])
        self.__terms: List[str] = terms
        self.__max_papers = max_papers

    def execute(self, providers: List[Provider]) -> List[Paper]:

        papers: List[Paper] = []
        for provider in providers:
            provider_papers = provider.get_paper_by_terms(
                self.__terms, self.__max_papers)

            if len(provider_papers) > 0:
                for paper in provider_papers:
                    resulting_paper = provider.get_paper_by_id(paper.paper_id)
                    if resulting_paper is not None:
                        papers.append(resulting_paper)
                break

        return papers

    def __str__(self) -> str:
        return f"<CollectorByTerms \
            [terms: { ''.join([str(term) + ', ' for term in self.__terms])}]>"
