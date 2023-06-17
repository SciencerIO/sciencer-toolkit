"""Collect Papers by DOI
"""
from typing import List

from ..providers.provider import Provider
from ..policies import Policy
from .collector import Collector
from ..models import Paper


class CollectByDOI(Collector):
    """Class that encapsulates the collection of a paper by its DOI"""

    def __init__(self, doi: str) -> None:
        super().__init__([Policy.BY_DOI])
        self.__doi: str = doi
        self._stop: bool = False

    def execute(self, providers: List[Provider]) -> List[Paper]:

        papers = []
        for provider in providers:
            if self._stop:
                return papers
            provider_paper = provider.get_paper_by_id(self.__doi)
            if provider_paper is not None:
                papers.append(provider_paper)
                break

        return papers

    def __str__(self) -> str:
        return f"<CollectorByDOI [doi: {self.__doi}]>"

    def stop(self) -> None:
        self._stop = True