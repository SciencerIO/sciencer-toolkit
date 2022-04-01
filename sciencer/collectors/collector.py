"""Base class for collector
"""
from abc import ABC, abstractmethod
from typing import List
from ..policies import HasPolicy
from ..models import Paper
from ..providers.provider import Provider


class Collector(HasPolicy, ABC):
    """Abstract Collector Class"""

    @abstractmethod
    def execute(self, providers: List[Provider]) -> List[Paper]:
        """Executes the collection.

        Args:
            providers (List[Provider]): providers used to collect new papers.

        Returns:
            List[Paper]: papers collected.
        """

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()
