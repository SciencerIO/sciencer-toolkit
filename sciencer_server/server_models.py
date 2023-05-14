from pydantic import BaseModel
from enum import Enum
import sciencer


class CollectorType(str, Enum):
    doi = "doi"
    author_id = "author_id"
    terms = "terms"


class Collector(BaseModel):
    type: CollectorType
    parameters: dict = []
    max_papers: int = 100


class ExpanderType(str, Enum):
    authors = "authors"
    references = "references"
    citations = "citations"


class Expander(BaseModel):
    type: ExpanderType
    max_papers: int = 100


class FilterType(str, Enum):
    year = "year"
    abstract = "abstract"
    field_of_study = "field_of_study"
    citations = "citations"


class Filter(BaseModel):
    type: FilterType
    parameters: dict = []


class Paper(BaseModel):
    paper_id: str
    external_ids: dict[str, str]
    authors_ids: set[str] = []
    references_ids: set[str] = []
    citations_ids: set[str] = []
    fields_of_study: set[str] = []
    abstract: str = None
    title: str = None
    year: int = None
    
    @staticmethod
    def from_cls(paper: sciencer.Paper) -> "Paper":
        return Paper(
            paper_id=paper.paper_id,
            external_ids=paper.external_ids._ids,
            authors_ids=paper.authors_ids,
            references_ids=paper.references_ids,
            citations_ids=paper.citations_ids,
            fields_of_study=paper.fields_of_study,
            abstract=paper.abstract,
            title=paper.title,
            year=paper.year
        )
