"""Base class for filter
"""

from abc import ABC, abstractmethod
from typing import List
from ..policies import HasPolicy, Policy
from ..models import Paper


class Filter(HasPolicy, ABC):
    """Base class for filters"""

    def __init__(self, policies: List[Policy]) -> None:
        """Creates a new Filter

        Args:
            policies (List[Policy]): policies needed for this filter to execute
        """
        super().__init__(policies)

    @abstractmethod
    def is_valid(self, paper: Paper) -> bool:
        """Verifies if the filter is satisfied.

        Args:
            paper (Paper): tested paper.

        Returns:
            bool: Returns True when the paper satisfies the criteria. Otherwise, returns false.
        """
