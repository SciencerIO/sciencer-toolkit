"""Filters paper by its year
"""
from .filter import Filter
from ..models import Paper


class FilterByYear(Filter):
    """Class that encapsulates the filter of a paper by its year"""

    def __init__(self, min_year: int, max_year: int) -> None:
        """Create a filter by year

        Args:
            min_year (int): to be accepted, paper's year should be more or equal to this year
            max_year (int): to be accepted, paper's year should be less or equal to this year
        """
        super().__init__(policies=[])
        self.__min: int = min_year
        self.__max: int = max_year

    def is_valid(self, paper: Paper) -> bool:
        if paper.year is None:
            return False

        return self.__min <= paper.year <= self.__max

    def __str__(self) -> str:
        return f"<FilterByYear [min: {self.__min}, max: {self.__max}]>"
