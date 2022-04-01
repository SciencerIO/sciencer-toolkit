"""Models used by Sciencer
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Set, Any


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


class Paper:
    """Model for a Paper"""

    def __init__(self, paper_id: str) -> None:
        self.__authors_id: List[str] = []
        self.__details: Dict[str, Any] = {}
        self.__id: str = paper_id
        self.__external_ids: PaperIDs = PaperIDs()
        self.__references_ids: Set[str] = set()
        self.__citations_ids: Set[str] = set()

    def get_external_id(self, name: PaperIDs.LABEL) -> Optional[str]:
        """Getter for paper's external IDs

        Returns:
            PaperIDs.LABEL: the paper's id. If it does not exist, returns None
        """
        return self.__external_ids.get_id(name)

    def set_external_id(self, name: PaperIDs.LABEL, value: str) -> Paper:
        """Setter for paper's external ID

        Args:
            name (PaperIDs.LABEL): The new external ID name
            value (str): The new external ID value

        Returns:
            Paper: the modified paper
        """
        self.__external_ids.add_id(name, value)
        return self

    @property
    def paper_id(self) -> str:
        """Getter for paper's s2

        Returns:
            str: the paper's s2 id
        """
        return self.__id

    @property
    def title(self) -> Optional[str]:
        """Getter for paper's title'

        Returns:
            str: the paper's title
        """
        if 'title' in self.__details:
            return self.__details['title']
        return None

    def set_title(self, title: str) -> Paper:
        """Setter for paper's title

        Args:
            doi (str): The new title for the paper

        Returns:
            Paper: the modified paper
        """
        self.__details['title'] = title
        return self

    @property
    def authors(self) -> List[str]:
        """Getter for paper's authors'

        Returns:
            str: the paper's authors
        """
        return self.__authors_id

    def add_author(self, author_id: str) -> Paper:
        """Add a new author to the paper

        Args:
            author_id (str): A new author for the paper

        Returns:
            Paper: the modified paper
        """
        if author_id not in self.__authors_id:
            self.__authors_id.append(author_id)

        return self

    def add_authors(self, authors_id: List[str]) -> Paper:
        """Add new authors to the paper

        Args:
            authors_id (List[str]): New authors for the paper

        Returns:
            Paper: the modified paper
        """
        for author_id in authors_id:
            self.add_author(author_id)

        return self

    @property
    def year(self) -> Optional[int]:
        """Getter for paper's year

        Returns:
            int: the paper's year
        """
        if 'year' in self.__details:
            return self.__details['year']
        return None

    def set_year(self, year: int) -> Paper:
        """Setter for paper's year

        Args:
            year (int): The new year

        Returns:
            Paper: the modified paper
        """
        self.__details['year'] = year
        return self

    @property
    def abstract(self) -> Optional[str]:
        """Getter for paper's abstract

        Returns:
            str: the paper's abstract
        """
        if 'abstract' in self.__details:
            return self.__details['abstract']
        return None

    def set_abstract(self, abstract: str) -> Paper:
        """Setter for paper's abstract

        Args:
            abstract (str): The new abstract

        Returns:
            Paper: the modified paper
        """
        self.__details['abstract'] = abstract
        return self

    def add_reference(self, reference_id: str) -> None:
        """Add a new reference to this paper

        Args:
            reference_id (str): the referenced paper id
        """
        self.__references_ids.add(reference_id)

    @property
    def references(self) -> List[str]:
        """Getter for paper's references

        Returns:
            List[str]: the list of referenced papers' ids
        """
        return list(self.__references_ids)

    def add_citation(self, citation_id: str) -> None:
        """Add a new citation to this paper

        Args:
            citation_id (str): the cited paper id
        """
        self.__citations_ids.add(citation_id)

    @property
    def citations(self) -> List[str]:
        """Getter for paper's citations

        Returns:
            List[str]: the list of cited papers' ids
        """
        return list(self.__citations_ids)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Paper):
            return __o.paper_id == self.paper_id
        return False

    def __hash__(self) -> int:
        return hash(self.paper_id)

    def __str__(self) -> str:
        return f"<Paper: {self.title}>"
