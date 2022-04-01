"""Base class for filter
"""

from abc import ABC, abstractmethod
from ..policies import HasPolicy
from ..models import Paper


class Filter(HasPolicy, ABC):
    """Base class for filters"""

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
