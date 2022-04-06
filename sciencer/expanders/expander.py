"""Base class for expander
"""
from abc import ABC, abstractmethod
from typing import List, Callable

from ..models import Paper
from ..policies import HasPolicy
from ..providers.provider import Provider


class Expander(HasPolicy, ABC):
    """Generic expansion job"""

    @abstractmethod
    def execute(self,
                papers: List[Paper],
                providers: List[Provider],
                on_expanded_paper: Callable[[Paper, Paper], None] = None) -> List[Paper]:
        """Executes the expansion.

        Args:
            papers (List[Paper]): papers to expand
            providers (List[Provider]): providers used to expand papers.
            on_expanded_paper (Callable[[Paper, Paper], None]): invoked when a new paper is \
                fetched during expansion. The first arg is the new fetched paper. \
                The second arg is the source paper

        Returns:
            List[Paper]: resulting papers from expansion.
        """

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()
