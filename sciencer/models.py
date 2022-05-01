"""Models used by Sciencer
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Set


class PaperIDs:
    """Paper IDs wrapper
    """

    class LABEL(Enum):
        """External IDs label """
        DOI = "DOI"
        MAG = "MAG"
        CORPUS = "CorpusId"
        PUBMED = "PubMed"
        DBLP = "DBLP"
        ARXIV = "ArXiv"
        ACL = "ACL"

    def __init__(self) -> None:
        """Creates a model to store Paper IDs

        Args:
            paper_id (str): the main ID of the paper
        """
        self.__ids: Dict[PaperIDs.LABEL, str] = {}

    def add_id(self, name: PaperIDs.LABEL, value: str) -> None:
        """Adds an id. If it already exists, overrites it

        Args:
            name (PaperIDs.LABEL): name of the id
            value (str): value of the id
        """
        self.__ids[name] = value

    def get_id(self, name: PaperIDs.LABEL) -> Optional[str]:
        """Gets an ID by its name

        Args:
            name (PaperIDs.LABEL): name of the ID

        Returns:
            Optional[str]: The value of the ID. If it does not exist, returns None
        """
        if name not in self.__ids:
            return None

        return self.__ids[name]


@dataclass
class Paper:
    """Model for a Paper"""
    # pylint: disable=too-many-instance-attributes

    paper_id: str
    external_ids: PaperIDs = field(default_factory=PaperIDs)
    authors_ids: Set[str] = field(default_factory=set)
    references_ids: Set[str] = field(default_factory=set)
    citations_ids: Set[str] = field(default_factory=set)
    fields_of_study: Set[str] = field(default_factory=set)
    abstract: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    year: Optional[int] = field(default=None)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Paper):
            return __o.paper_id == self.paper_id
        return False

    def __hash__(self) -> int:
        return hash(self.paper_id)

    def __str__(self) -> str:
        return f"<Paper: {self.title}>"
