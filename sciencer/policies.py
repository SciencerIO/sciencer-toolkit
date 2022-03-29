"""Module with all policy related classes and methods
"""
from enum import Enum
from typing import List, Set


class Policy(Enum):
    """Policies for Sciencer Components"""

    BY_DOI = "By DOI"
    BY_AUTHOR = "By Author"
    BY_QUERY = "By Query"


class HasPolicy:
    """Manages the Policies"""

    def __init__(self, policies: List[Policy]) -> None:
        super().__init__()
        self.__policies: Set[Policy] = set(policies)

    @property
    def available_policies(self) -> List[Policy]:
        """Policies available for this instance

        Returns:
            List[POLICY]: the instance's policies
        """
        return list(self.__policies)

    def add_policy(self, new_policy: Policy) -> None:
        """Adds a new policy

        Args:
            new_policy (Policy): the new policy
        """
        self.__policies.add(new_policy)
