"""Filters paper by words in abstract
"""
from .filter import Filter
from ..models import Paper


class FilterByAbstract(Filter):
    """Class that encapsulates the filter of paper by its abstract words"""

    def __init__(self, word: str) -> None:
        super().__init__(policies=[])
        self.__word: str = word

    def is_valid(self, paper: Paper) -> bool:
        if paper.abstract is None:
            return False
        return self.__word in paper.abstract

    def __str__(self) -> str:
        return f"<FilterByAbstract [word: {self.__word}]>"
