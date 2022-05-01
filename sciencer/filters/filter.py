"""Base class for filter
"""
from typing import List
from abc import ABC, abstractmethod
from ..policies import HasPolicy
from ..models import Paper
from ..policies import Policy


class Filter(HasPolicy, ABC):
    """Base class for filters"""

    def __init__(self,  policies: List[Policy], accept_when_empty: bool = False) -> None:
        super().__init__(policies=policies)
        self._accept_when_empty: bool = accept_when_empty

    @abstractmethod
    def is_valid(self, paper: Paper) -> bool:
        """Verifies if the filter is satisfied.

        Args:
            paper (Paper): tested paper.

        Returns:
            bool: Returns True when the paper satisfies the criteria. Otherwise, returns false.
        """

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()
