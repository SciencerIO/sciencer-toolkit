"""Base class for providers
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..policies import HasPolicy
from ..models import Paper


class Provider(HasPolicy, ABC):
    """Base class for a provider"""

    @abstractmethod
    def get_paper_by_id(self, paper_id: str) -> Optional[Paper]:
        """Fetches a paper by its id. It works with DOIs too

        Args:
            id (_type_): id of the paper to be retrieved

        Returns:
            Optional[Paper]: When available, returns the Paper with the given id. \
                             Otherwise, returns None
        """

    @abstractmethod
    def get_papers_by_author(self, author_id: str = "") -> List[Paper]:
        """Fetches the papers associated with an authors.

        Args:
            id (str, optional): The author's id. Defaults to "".

        Returns:
            List[Paper]: The list of papers associated with an author.
        """
