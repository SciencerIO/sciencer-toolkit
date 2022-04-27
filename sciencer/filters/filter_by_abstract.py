"""Filters paper by words in abstract
"""
from .filter import Filter
from ..models import Paper


class FilterByAbstract(Filter):
    """Class that encapsulates the filter of paper by its abstract words"""

    def __init__(self, word: str, accept_when_empty=False) -> None:
        """Creates a filter by abstract.
           This filter considers a paper valid if it includes a word in its abstract.

        Args:
            word (str): the word that the paper's abstract must have
            accept_when_empty (bool, optional): when True, the Filter accepts papers \
                without the necessary properties to check validity. Defaults to False.
        """
        super().__init__(policies=[], accept_when_empty=accept_when_empty)
        self.__word: str = word

    def is_valid(self, paper: Paper) -> bool:
        if paper.abstract is None:
            return self._accept_when_empty
        return self.__word in paper.abstract

    def __str__(self) -> str:
        return f"<FilterByAbstract [word: {self.__word}]>"
