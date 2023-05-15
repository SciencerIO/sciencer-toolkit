from pydantic import BaseModel
from typing import Optional
from enum import Enum
import threading
import sciencer
from server_models import (
    Filter,
    Expander,
    Collector,
    Paper,
    CollectorType,
    ExpanderType,
    FilterType,
)


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


class Results(BaseModel):
    Collected: list[Paper] = []
    Expanded: list[Paper] = []
    Filtered: list[Paper] = []
    Accepted: list[Paper] = []
    Rejected: list[Paper] = []

    @staticmethod
    def from_cls(results: "ResultsCls") -> "Results":
        return Results(
            Collected=[Paper.from_cls(paper) for paper in results.Collected],
            Expanded=[Paper.from_cls(paper) for paper in results.Expanded],
            Filtered=[Paper.from_cls(paper) for paper in results.Filtered],
            Accepted=[Paper.from_cls(paper) for paper in results.Accepted],
            Rejected=[Paper.from_cls(paper) for paper in results.Rejected],
        )


class ResultsCls:
    def __init__(self):
        self.Collected: list[sciencer.Paper] = []
        self.Expanded: list[sciencer.Paper] = []
        self.Filtered: list[sciencer.Paper] = []
        self.Accepted: list[sciencer.Paper] = []
        self.Rejected: list[sciencer.Paper] = []


class Search(BaseModel):
    id: int
    status: SearchStatus = SearchStatus.created
    config: SearchConfiguration
    results: Results = Results()

    @staticmethod
    def from_cls(search: "SearchCls") -> "Search":
        return Search(
            id=search.id,
            status=search.status,
            config=search.config,
            results=Results.from_cls(search.results),
        )


class SearchCls:
    max_num_threads = 10

    def __init__(self, *, id: int, config: SearchConfiguration):
        self.id: int = id
        self.status: SearchStatus = SearchStatus.created
        self.config: SearchConfiguration = config
        self.results: ResultsCls = ResultsCls()
        self.thread = None
        self.stop_thread = False

        self.run()

    class search_callbacks(sciencer.Callbacks):
        def __init__(self, *, Search: "SearchCls") -> None:
            super().__init__()
            self.search: SearchCls = Search

        def on_paper_collected(
            self, paper: sciencer.Paper, collector: sciencer.collectors.Collector
        ) -> None:
            # print(f"Paper {paper} collected by {collector} !")
            if self.search is not None:
                self.search.results.Collected.append(paper)

        def on_paper_expanded(
            self,
            paper: sciencer.Paper,
            expander: sciencer.expanders.Expander,
            source_paper: sciencer.Paper,
        ) -> None:
            # print(f"Paper {paper} was expanded by {expander} from {source_paper}")
            if self.search is not None:
                self.search.results.Expanded.append(paper)

        def on_paper_filtered(
            self,
            paper: sciencer.Paper,
            filter_executed: sciencer.filters.Filter,
            result: bool,
        ) -> None:
            # print(f"Paper {paper} was filtered by {filter_executed} and got {result}")
            if self.search is not None:
                self.search.results.Filtered.append(paper)

        def on_paper_accepted(self, paper: sciencer.Paper) -> None:
            print(f"Paper {paper} accepted!")
            if self.search is not None:
                self.search.results.Accepted.append(paper)

        def on_paper_rejected(self, paper: sciencer.Paper) -> None:
            print(f"Paper {paper} rejected!")
            if self.search is not None:
                self.search.results.Rejected.append(paper)

    def run(self):
        if self.status == SearchStatus.running:
            return

        if self.thread is not None:
            return

        if self.config is None:
            self.status = SearchStatus.failed
            return

        self.status = SearchStatus.queued

        # TODO: check for thread number limit
        # https://stackoverflow.com/questions/19369724/the-right-way-to-limit-maximum-number-of-threads-running-at-once

        self.thread = threading.Thread(target=self.run_thread)
        self.thread.daemon = True
        self.thread.start()

    def cancel(self):
        if self.thread is not None:
            self.stop_thread = True
            self.thread = None
            self.status = SearchStatus.cancelled

    def run_thread(self):
        self.status = SearchStatus.running

        # Providers
        s2_provider = sciencer.providers.SemanticScholarProvider(api_key="")

        # Collect
        sciencer_collectors = []
        for collector in self.config.collectors:
            match collector.type:
                case CollectorType.author_id:
                    author_id = collector.parameters.get("author_id")
                    if author_id is None:
                        print("No author_id provided for CollectByAuthorID")
                        continue
                    sciencer_collectors.append(
                        sciencer.collectors.CollectByAuthorID(author_id)
                    )
                    pass
                case CollectorType.doi:
                    doi = collector.parameters.get("doi")
                    if doi is None:
                        print("No doi provided for CollectByDOI")
                        continue
                    sciencer_collectors.append(sciencer.collectors.CollectByDOI(doi))
                    pass
                case CollectorType.terms:
                    terms: Optional[list[str]] = collector.parameters.get("terms")
                    if terms is None:
                        print("No terms provided for CollectByTerms")
                        continue
                    max_papers: Optional[int] = collector.parameters.get("max_papers")
                    if max_papers is None:
                        max_papers = 100
                    sciencer_collectors.append(
                        sciencer.collectors.CollectByTerms(
                            terms=terms, max_papers=max_papers
                        )
                    )
                    pass
                case _:
                    pass

        if sciencer_collectors == []:
            print("No collectors provided")
            self.status = SearchStatus.failed
            return

        # Expanders
        sciencer_expanders = []
        for expander in self.config.expanders:
            match expander.type:
                case ExpanderType.authors:
                    sciencer_expanders.append(sciencer.expanders.ExpandByAuthors())
                    pass
                case ExpanderType.references:
                    sciencer_expanders.append(sciencer.expanders.ExpandByReferences())
                    pass
                case ExpanderType.citations:
                    sciencer_expanders.append(sciencer.expanders.ExpandByCitations())
                    pass
                case _:
                    pass
        
        if sciencer_expanders == []:
            sciencer_expanders.append(sciencer.expanders.ExpandByReferences())
            sciencer_expanders.append(sciencer.expanders.ExpandByAuthors())
            sciencer_expanders.append(sciencer.expanders.ExpandByCitations())


        # Filters
        sciencer_filters = []
        for filter in self.config.filters:
            match filter.type:
                case FilterType.year:
                    min_year: Optional[int] = filter.parameters.get("min_year")
                    max_year: Optional[int] = filter.parameters.get("max_year")
                    if (min_year is None) or (max_year is None):
                        print("No min_year or max_year provided for FilterByYear")
                        continue
                    if min_year is None:
                        min_year = 0
                    if max_year is None:
                        max_year = 9999
                    sciencer_filters.append(
                        sciencer.filters.FilterByYear(min_year=min_year, max_year=max_year)
                    )
                    pass
                case FilterType.abstract:
                    term: Optional[str] = filter.parameters.get("term")
                    if term is None:
                        print("No term provided for FilterByAbstract")
                        continue
                    sciencer_filters.append(sciencer.filters.FilterByAbstract(term))
                    pass
                case FilterType.field_of_study:
                    field_of_study: Optional[str] = filter.parameters.get("field_of_study")
                    if field_of_study is None:
                        print("No field_of_study provided for FilterByFieldOfStudy")
                        continue
                    sciencer_filters.append(
                        sciencer.filters.FilterByFieldOfStudy(field_of_study)
                    )
                    pass
                case FilterType.citations:
                    min_citations: Optional[int] = filter.parameters.get("min_citations")
                    max_citations: Optional[int] = filter.parameters.get("max_citations")
                    if (min_citations is None) or (max_citations is None):
                        print(
                            "No min_citations or max_citations provided for FilterByCitations"
                        )
                        continue
                    if min_citations is None:
                        min_citations = 0
                    if max_citations is None:
                        max_citations = 999999
                    sciencer_filters.append(
                        sciencer.filters.FilterByCitations(
                            min_citations=min_citations, max_citations=max_citations
                        )
                    )
                    pass
                case _:
                    pass

        # Setup sciencer
        s = sciencer.Sciencer()
        s.add_provider(s2_provider)

        for col in sciencer_collectors:
            s.add_collector(col)

        for exp in sciencer_expanders:
            s.add_expander(exp)
        
        for fil in sciencer_filters:
            s.add_filter(fil)

        callbacks = self.search_callbacks(Search=self)

        # for each num_iterations
        for i in range(self.config.num_iterations):
            if self.stop_thread:
                print("Exiting loop.")
                break
            print(f"Starting iteration #{i+1}...")
            if i == 0:
                batch = s.iterate(
                    remove_source_from_results=True, callbacks=[callbacks]
                )
            else:
                batch = s.iterate(callbacks=[callbacks])
            print(f" 📜 iteration #{i+1} collected {len(batch)} papers.")

        self.status = SearchStatus.finished
        self.thread = None
