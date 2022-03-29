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

    @abstractmethod
    def get_paper_by_terms(self, terms: List[str], max_papers: int) -> List[Paper]:
        """Fetches the papers that have the following terms.

        Args:
            terms (List[str]): terms included in the papers to be retrieved
            max_paper (int): the maximum number of papers to retrieve

        Returns:
            List[Paper]: The list of papers that include the terms
        """
