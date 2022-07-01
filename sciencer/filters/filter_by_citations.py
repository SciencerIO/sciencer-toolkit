"""Filters paper by its number of citations
"""
from .filter import Filter
from ..models import Paper


class FilterByCitations(Filter):
    """Class that encapsulates the filter of a paper by its number of citations"""

    def __init__(self, min_citations: int, max_citations: int, accept_when_empty=False) -> None:
        """Create a filter by number of citations.

        Args:
            min_citations (int): to be accepted, paper's number of citations should be more or \
                equal to this value
            max_citations (int): to be accepted, paper's number of citations should be less or \
                equal to this value
            accept_when_empty (bool, optional): when True, the Filter accepts papers without the \
                necessary properties to check validity. Defaults to False.
        """
        super().__init__(policies=[], accept_when_empty=accept_when_empty)
        self.__min: int = min_citations
        self.__max: int = max_citations
        if self.__min > self.__max:
            raise ValueError

    def is_valid(self, paper: Paper) -> bool:
        if paper.citations_ids is None:
            return self._accept_when_empty

        return self.__min <= len(paper.citations_ids) <= self.__max

    def __str__(self) -> str:
        return f"<FilterByCitations [min: {self.__min}, max: {self.__max}]>"
