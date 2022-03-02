"""Models used by Sciencer
"""
from __future__ import annotations
from typing import List, Optional


class Paper:
    """Model for a Paper"""

    def __init__(self, id:str) -> None:
        self.__paper_id: Optional[str] = id
        self.__authors_id: List[str] = []
        self.__title: Optional[str] = None
        self.__id_doi: Optional[str] = None
        self.__id_mag: Optional[str] = None
        self.__id_corpus: Optional[str] = None
        self.__id_pubmed: Optional[str] = None
        self.__id_dblp: Optional[str] = None
        self.__id_arxiv: Optional[str] = None
        self.__id_acl: Optional[str] = None
        self.__abstract: Optional[str] = None
        self.__year: Optional[int] = None

    @property
    def acl(self) -> Optional[str]:
        """Getter for paper's acl

        Returns:
            str: the paper's acl id
        """
        return self.__id_acl

    def set_acl(self, acl_id: str) -> Paper:
        """Setter for paper's acl

        Args:
            acl (str): The new acl

        Returns:
            Paper: the modified paper
        """
        self.__id_acl = acl_id
        return self

    @property
    def arxiv(self) -> Optional[str]:
        """Getter for paper's arxiv

        Returns:
            str: the paper's arxiv id
        """
        return self.__id_arxiv

    def set_arxiv(self, arxiv_id: str) -> Paper:
        """Setter for paper's arxiv

        Args:
            arxiv (str): The new arxiv

        Returns:
            Paper: the modified paper
        """
        self.__id_arxiv = arxiv_id
        return self

    @property
    def dblp(self) -> Optional[str]:
        """Getter for paper's dblp

        Returns:
            str: the paper's dblp id
        """
        return self.__id_dblp

    def set_dblp(self, dblp_id: str) -> Paper:
        """Setter for paper's dblp

        Args:
            dblp (str): The new dblp

        Returns:
            Paper: the modified paper
        """
        self.__id_dblp = dblp_id
        return self

    @property
    def pubmed(self) -> Optional[str]:
        """Getter for paper's pubMed

        Returns:
            str: the paper's pubMed id
        """
        return self.__id_pubmed

    def set_pubmed(self, pubmed_id: str) -> Paper:
        """Setter for paper's pubMed

        Args:
            pubMed (str): The new pubMed

        Returns:
            Paper: the modified paper
        """
        self.__id_pubmed = pubmed_id
        return self

    @property
    def corpus(self) -> Optional[str]:
        """Getter for paper's corpus

        Returns:
            str: the paper's corpus id
        """
        return self.__id_corpus

    def set_corpus(self, corpus_id: str) -> Paper:
        """Setter for paper's corpus

        Args:
            corpus (str): The new corpus

        Returns:
            Paper: the modified paper
        """
        self.__id_corpus = corpus_id
        return self

    @property
    def mag(self) -> Optional[str]:
        """Getter for paper's mag

        Returns:
            str: the paper's mag id
        """
        return self.__id_mag

    def set_mag(self, mag_id: str) -> Paper:
        """Setter for paper's mag

        Args:
            mag (str): The new mag

        Returns:
            Paper: the modified paper
        """
        self.__id_mag = mag_id
        return self

    @property
    def paper_id(self) -> Optional[str]:
        """Getter for paper's s2

        Returns:
            str: the paper's s2 id
        """
        return self.__paper_id

    def set_s2(self, s2_id: str) -> Paper:
        """Setter for paper's s2

        Args:
            s2 (str): The new s2

        Returns:
            Paper: the modified paper
        """
        self.__paper_id = s2_id
        return self

    @property
    def doi(self) -> Optional[str]:
        """Getter for paper's DOI'

        Returns:
            str: the paper's doi
        """
        return self.__id_doi

    def set_doi(self, doi: str) -> Paper:
        """Setter for paper's DOI

        Args:
            doi (str): The new DOI

        Returns:
            Paper: the modified paper
        """
        self.__id_doi = doi
        return self

    @property
    def title(self) -> Optional[str]:
        """Getter for paper's title'

        Returns:
            str: the paper's title
        """
        return self.__title

    def set_title(self, title: str) -> Paper:
        """Setter for paper's title

        Args:
            doi (str): The new title for the paper

        Returns:
            Paper: the modified paper
        """
        self.__title = title
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
        return self.__year

    def set_year(self, year: int) -> Paper:
        """Setter for paper's year

        Args:
            year (int): The new year

        Returns:
            Paper: the modified paper
        """
        self.__year = year
        return self

    @property
    def abstract(self) -> Optional[str]:
        """Getter for paper's abstract

        Returns:
            str: the paper's abstract
        """
        return self.__abstract

    def set_abstract(self, abstract: str) -> Paper:
        """Setter for paper's abstract

        Args:
            abstract (str): The new abstract

        Returns:
            Paper: the modified paper
        """
        self.__abstract = abstract
        return self

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Paper):
           return __o.paper_id == self.paper_id 
        return False

    def __hash__(self) -> int:
        return hash(self.paper_id)

    def __str__(self) -> str:
        return f"<Paper: {self.title}>"
