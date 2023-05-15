from pydantic import BaseModel
from typing import Optional
from enum import Enum
import sciencer


class CollectorType(str, Enum):
    doi = "doi"
    author_id = "author_id"
    terms = "terms"


class Collector(BaseModel):
    type: CollectorType
    parameters: dict = {}

class ExpanderType(str, Enum):
    authors = "authors"
    references = "references"
    citations = "citations"


class Expander(BaseModel):
    type: ExpanderType


class FilterType(str, Enum):
    year = "year"
    abstract = "abstract"
    field_of_study = "field_of_study"
    citations = "citations"


class Filter(BaseModel):
    type: FilterType
    parameters: dict = {}


class Paper(BaseModel):
    paper_id: str
    external_ids: dict[sciencer.PaperIDs.LABEL, str] = {}
    authors_ids: set[str] = set()
    references_ids: set[str] = set()
    citations_ids: set[str] = set()
    fields_of_study: set[str] = set()
    abstract: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    
    @staticmethod
    def from_cls(paper: sciencer.Paper) -> "Paper":
        out_paper = Paper(
            paper_id=paper.paper_id,
            external_ids=paper.external_ids._ids,
            abstract=paper.abstract,
            title=paper.title,
            year=paper.year
        )
        if paper.authors_ids:
            out_paper.authors_ids = paper.authors_ids
        if paper.references_ids:
            out_paper.references_ids = paper.references_ids
        if paper.citations_ids:
            out_paper.citations_ids = paper.citations_ids
        if paper.fields_of_study:
            out_paper.fields_of_study = paper.fields_of_study
        return out_paper
