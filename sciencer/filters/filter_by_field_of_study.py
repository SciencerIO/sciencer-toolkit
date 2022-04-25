"""Filters paper by words in abstract
"""
from .filter import Filter
from ..models import Paper


class FilterByFieldOfStudy(Filter):
    """Class that encapsulates the filter of paper by its fields of study"""

    def __init__(self, field_of_study: str, accept_when_empty=False) -> None:
        super().__init__(policies=[])
        self.__field_of_study: str = field_of_study
        self.__accept_when_empty: bool = accept_when_empty

    def is_valid(self, paper: Paper) -> bool:
        if paper.fields_of_study is None:
            return self.__accept_when_empty
        return self.__field_of_study in paper.fields_of_study

    def __str__(self) -> str:
        return f"<FilterByFieldOfStudy [word: {self.__field_of_study}]>"