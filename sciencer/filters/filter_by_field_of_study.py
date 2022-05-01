"""Filters paper by words in abstract
"""
from .filter import Filter
from ..models import Paper


class FilterByFieldOfStudy(Filter):
    """Class that encapsulates the filter of paper by its fields of study"""

    def __init__(self, field_of_study: str, accept_when_empty=False) -> None:
        """Create a filter by field of study.
           A paper is considered valid when a field of study is included \
           in the paper's fields of study.

        Args:
            field_of_study (str): the field of study that the paper must have
            accept_when_empty (bool, optional): when True, the Filter accepts papers without \
                the necessary properties to check validity. Defaults to False.
        """
        super().__init__(policies=[], accept_when_empty=accept_when_empty)
        self.__field_of_study: str = field_of_study

    def is_valid(self, paper: Paper) -> bool:
        if paper.fields_of_study is None:
            return self._accept_when_empty
        return self.__field_of_study in paper.fields_of_study

    def __str__(self) -> str:
        return f"<FilterByFieldOfStudy [word: {self.__field_of_study}]>"
