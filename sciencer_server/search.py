from pydantic import BaseModel
from enum import Enum
import threading
import sciencer
from server_models import Filter, Expander, Collector, Paper


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
            print(f"Paper {paper} collected by {collector} !")
            if self.search is not None:
                self.search.results.Collected.append(paper)

        def on_paper_expanded(
            self,
            paper: sciencer.Paper,
            expander: sciencer.expanders.Expander,
            source_paper: sciencer.Paper,
        ) -> None:
            print(f"Paper {paper} was expanded by {expander} from {source_paper}")
            if self.search is not None:
                self.search.results.Expanded.append(paper)

        def on_paper_filtered(
            self,
            paper: sciencer.Paper,
            filter_executed: sciencer.filters.Filter,
            result: bool,
        ) -> None:
            print(f"Paper {paper} was filtered by {filter_executed} and got {result}")
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
            self.thread.stop()
            self.thread = None
            self.status = SearchStatus.cancelled

    def run_thread(self):
        self.status = SearchStatus.running

        # Providers
        s2_provider = sciencer.providers.SemanticScholarProvider(api_key="")

        # Collect
        # col_doi = sciencer.collectors.CollectByDOI("10.1093/mind/LIX.236.433")
        # col_author_id = sciencer.collectors.CollectByAuthorID("2262347")
        col_terms = sciencer.collectors.CollectByTerms(
            terms=[
                "social",
                "intelligence",
                "machines",
                "cognition",
                "emotional",
                "human",
            ],
            max_papers=20,
        )

        # Expanders
        exp_author = sciencer.expanders.ExpandByAuthors()
        # exp_references = sciencer.expanders.ExpandByReferences()
        # exp_citations = sciencer.expanders.ExpandByCitations()

        # Filters
        # After 2010
        filter_year = sciencer.filters.FilterByYear(min_year=2010, max_year=2030)

        # Has 'social' word
        filter_social_in_abstract = sciencer.filters.FilterByAbstract("social")

        # Has 'Computer Science' field of study
        filter_has_computer_science_field_of_study = (
            sciencer.filters.FilterByFieldOfStudy("Computer Science")
        )

        filter_by_large_number_citations = sciencer.filters.FilterByCitations(
            100, 999999
        )

        # Setup sciencer
        s = sciencer.Sciencer()
        s.add_provider(s2_provider)
        # s.add_collector(col_doi)
        # s.add_collector(col_author_id)
        s.add_collector(col_terms)
        s.add_expander(exp_author)
        # s.add_expander(exp_references)
        # s.add_expander(exp_citations)
        s.add_filter(filter_year)
        s.add_filter(filter_social_in_abstract)
        s.add_filter(filter_has_computer_science_field_of_study)
        s.add_filter(filter_by_large_number_citations)

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
