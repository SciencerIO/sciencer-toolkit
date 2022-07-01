"""Filters paper by its year
"""
from .filter import Filter
from ..models import Paper


class FilterByYear(Filter):
    """Class that encapsulates the filter of a paper by its year"""

    def __init__(self, min_year: int, max_year: int, accept_when_empty=False) -> None:
        """Create a filter by year.

        Args:
            min_year (int): to be accepted, paper's year should be more or equal to this year
            max_year (int): to be accepted, paper's year should be less or equal to this year
            accept_when_empty (bool, optional): when True, the Filter accepts papers without the \
                necessary properties to check validity. Defaults to False.
        """
        super().__init__(policies=[], accept_when_empty=accept_when_empty)
        self.__min: int = min_year
        self.__max: int = max_year
        if self.__min > self.__max:
            raise ValueError

    def is_valid(self, paper: Paper) -> bool:
        if paper.year is None:
            return self._accept_when_empty

        return self.__min <= paper.year <= self.__max

    def __str__(self) -> str:
        return f"<FilterByYear [min: {self.__min}, max: {self.__max}]>"
