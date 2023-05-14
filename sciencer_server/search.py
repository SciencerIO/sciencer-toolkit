from typing import Union
from pydantic import BaseModel
from enum import Enum

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

# create an enum for search status
class SearchStatus(str, Enum):
    created = "created"
    queued = "queued"
    running = "running"
    finished = "finished"
    failed = "failed"
    cancelled = "cancelled"

class SearchConfiguration(BaseModel):
    num_iterations: int
    max_num_papers: int = 100
    filters: list[Filter] = []
    expanders: list[Expander] = []
    collectors: list[Collector] = []

class Search(BaseModel):
    id: int
    status: SearchStatus
    config: SearchConfiguration
    results: list

    class Config:
        orm_mode = True

class SearchCls:
    def __init__(self, *, id: int, status: SearchStatus, config: SearchConfiguration, results: list):
        self.id = id
        self.status = status
        self.config = config
        self.results = results
    
    def run(self):
        self.status = SearchStatus.running
