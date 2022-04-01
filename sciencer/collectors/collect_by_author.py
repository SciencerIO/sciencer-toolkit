"""Collect Papers by Author ID
"""
from typing import List
from ..policies import Policy
from .collector import Collector
from ..models import Paper
from ..providers.provider import Provider


class CollectByAuthorID(Collector):
    """Class that encapsulates the collection of an author by its ID"""

    def __init__(self, author_id: str) -> None:
        super().__init__(policies=[Policy.BY_AUTHOR])
        self.__author_id: str = author_id

    def execute(self, providers: List[Provider]) -> List[Paper]:

        papers = []
        for provider in providers:
            provider_papers = provider.get_papers_by_author(self.__author_id)
            papers.extend(provider_papers)
            if len(provider_papers) > 0:
                break

        return papers

    def __str__(self) -> str:
        return f"<CollectorByAuthorID [author id: {self.__author_id}]>"
