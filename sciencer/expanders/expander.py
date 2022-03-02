"""Base class for expander
"""
from abc import ABC, abstractmethod
from typing import List
from ..policies import HasPolicy
from ..models import Paper
from ..providers.provider import Provider


class Expander(HasPolicy, ABC):
    """Generic expansion job"""

    @abstractmethod
    def execute(self, papers: List[Paper], providers: List[Provider]) -> List[Paper]:      
        """Executes the expansion.

        Args:
            papers (List[Paper]): papers to expand
            providers (List[Provider]): providers used to expand papers.

        Returns:
            List[Paper]: resulting papers from expansion.
        """
