"""Module with all policy related classes and methods
"""
from enum import Enum
from typing import List


class Policy(Enum):
    """Policies for Sciencer Components"""

    BY_DOI = "By DOI"
    BY_AUTHOR = "By Author"


class HasPolicy:
    """Manages the Policies"""

    def __init__(self, policies: List[Policy]) -> None:
        super().__init__()
        self.__policies: List[Policy] = policies

    @property
    def available_policies(self) -> List[Policy]:
        """Policies available for this instance

        Returns:
            List[POLICY]: the instance's policies
        """
        return self.__policies
