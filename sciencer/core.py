""" Sciencer Core
"""
from typing import Dict, List, Set, Tuple
from sciencer.collectors.collector import Collector
from sciencer.expanders.expander import Expander
from sciencer.filters.filter import Filter
from sciencer.policies import Policy
from sciencer.models import Paper
from .providers.provider import Provider


def create_handle_on_expand_paper(expander=None, callbacks=None):
    """Creates a new handle for expanding papers
    """
    def handle_expansion(exp_paper: Paper, src_paper: Paper):
        for callback in callbacks:
            callback.on_paper_expanded(
                exp_paper, expander, src_paper)
    return handle_expansion


class Callbacks:
    """Sciencer callbacks wrapper"""

    def on_paper_collected(self, paper: Paper, collector: Collector) -> None:
        """Invoked when a new paper is collected.

        Args:
            paper (Paper): new paper collected.
            collector (Collector): source of the collection
        """

    def on_paper_expanded(self, new_paper: Paper, expander: Expander, source_paper: Paper) -> None:
        """Invoked when a paper is fetched from an expansion.

        Args:
            new_paper (Paper): paper expanded.
            expander (Expander): expander that fetched the paper.
            source_paper (Paper): expanded paper.
        """

    def on_paper_filtered(self, paper: Paper, filter_executed: Filter, result: bool) -> None:
        """Invoked when a paper has been filtered

        Args:
            paper (Paper): paper being tested
            filter_executed (Filter): filters executed
            result (bool): if filter is satisfied, return True. Otherwise, False
        """

    def on_paper_accepted(self, paper: Paper) -> None:
        """Invoked when a new paper has been accepted.

        Args:
            paper (Paper): accepted paper.
        """

    def on_paper_rejected(self, paper: Paper) -> None:
        """Invoked when a paper has been rejected

        Args:
            paper (Paper): rejected paper.
        """


class PaperLog:
    """Log of the paper's lifecycle during a iteration
    """

    def __init__(self, paper: Paper) -> None:
        self.paper: Paper = paper
        self.__collected_from: List[Collector] = []
        self.__expanded_from: List[Tuple[Paper, Expander]] = []
        self.__filtered_by: List[Tuple[Filter, bool]] = []

    def add_collector_source(self, collector: Collector) -> None:
        """Adds a new collector to the log

        Args:
            collector (Collector): collector used to fetch the paper
        """
        self.__collected_from.append(collector)

    def add_expander_source(self, expander: Expander, source_paper: Paper) -> None:
        """Adds a new expander to the log

        Args:
            expander (Expander): expander that fetched this paper
            source_paper (Paper): paper used during the expansion
        """
        self.__expanded_from.append((source_paper, expander))

    def add_filter_tested(self, filter_tested: Filter, result: bool) -> None:
        """Add a new filter to the log

        Args:
            filter_tested (Filter): filter that tested this paper
            result (bool): if the filter was satisfied, it is True. Otherwise, it is False
        """
        self.__filtered_by.append((filter_tested, result))


class LogCallbacks(Callbacks):
    """Logs the history of all the papers
    """

    def __init__(self) -> None:
        self.__paper_logs: Dict[Paper, PaperLog] = {}

    def on_paper_collected(self, paper: Paper, collector: Collector) -> None:
        if paper not in self.__paper_logs:
            self.__paper_logs[paper] = PaperLog(paper)
        self.__paper_logs[paper].add_collector_source(collector)

    def on_paper_expanded(self, new_paper: Paper, expander: Expander, source_paper: Paper) -> None:
        if new_paper not in self.__paper_logs:
            self.__paper_logs[new_paper] = PaperLog(new_paper)
        self.__paper_logs[new_paper].add_expander_source(
            expander, source_paper)

    def on_paper_filtered(self, paper: Paper, filter_executed: Filter, result: bool) -> None:
        if paper not in self.__paper_logs:
            self.__paper_logs[paper] = PaperLog(paper)
        self.__paper_logs[paper].add_filter_tested(filter_executed, result)


class Sciencer:
    """Core component of Sciencer
    Responsible for generating a new collection of paper
    """

    def __init__(self) -> None:
        self.__providers: List[Provider] = []
        self.__collectors: List[Collector] = []
        self.__expanders: List[Expander] = []
        self.__filters: List[Filter] = []
        self.__providers_by_policy: Dict[Policy, List[Provider]] = {}

    def add_provider(self, provider_to_add: Provider) -> None:
        """Add a providers to Sciencer
        Args:
            provider (Provider): Provider to add
        """
        self.__providers.append(provider_to_add)
        for provider_policy in provider_to_add.available_policies:
            if provider_policy not in self.__providers_by_policy:
                self.__providers_by_policy[provider_policy] = []
                self.__providers_by_policy[provider_policy].append(
                    provider_to_add)

    def add_collector(self, collector_to_add: Collector) -> None:
        """Add a collectors to Sciencer
        Args:
            collector (Collector): Collector to add
        """
        self.__collectors.append(collector_to_add)

    def add_expander(self, expander_to_add: Expander) -> None:
        """Add a expanders to Sciencer
        Args:
            expander (Expander): Expander to add
        """
        self.__expanders.append(expander_to_add)

    def add_filter(self, filter_to_add: Filter) -> None:
        """Add a filters to Filter
        Args:
            filter (Filter): Filter to add
        """
        self.__filters.append(filter_to_add)

    def __get_provider(self, needed_policies: List[Policy]) -> List[Provider]:
        """Returns the providers capable of satisfying the given policies

        Args:
            needed_policies (List[Policy]): policies to be satisfied

        Returns:
            List[Provider]: List of providers that satisfy the policies
        """
        return [
            provider
            for policy in needed_policies
            for provider in self.__providers_by_policy[policy]
        ]

    def __filter_papers(self, papers_to_filter: Set[Paper], callbacks: List[Callbacks]):
        accepted_papers = set()

        for paper in papers_to_filter:
            result = True
            for m_filter in self.__filters:
                f_result = m_filter.is_valid(paper)

                if not f_result:
                    result = False

                for callback in callbacks:
                    callback.on_paper_filtered(
                        paper, m_filter, result)
            if result is True:
                accepted_papers.add(paper)

            for callback in callbacks:
                if paper in accepted_papers:
                    callback.on_paper_accepted(paper)
                else:
                    callback.on_paper_rejected(paper)

        return accepted_papers

    def iterate(
        self,
        source_papers=None,
        remove_source_from_results: bool = False,
        callbacks: List[Callbacks] = None,
    ) -> List[Paper]:
        """Iterates the a set of papers and generates a new collection of papers
        When no source_papers are given, uses registered collectors
        Args:
            source_papers (List[Paper], optional): the set of papers to start
            the expansion. Defaults to None.
            remove_source_from_results (bool): remove the source papers from the results

        Returns:
            List[Paper]: the resulting collection of papers
        """
        callbacks = [] if callbacks is None else callbacks
        callbacks.append(LogCallbacks())

        if source_papers is None:
            source_papers = set()

            for collector in self.__collectors:
                collected_papers = collector.execute(self.__get_provider(
                    collector.available_policies
                ))
                source_papers.update(collected_papers)

                for collected_paper in collected_papers:
                    for callback in callbacks:
                        callback.on_paper_collected(collected_paper, collector)

        # Expanders

        paper_after_expansion = set(source_papers)

        for expander in self.__expanders:
            paper_after_expansion.update(expander.execute(
                papers=source_papers,
                providers=self.__get_provider(expander.available_policies),
                on_expanded_paper=create_handle_on_expand_paper(
                    expander, callbacks)
            ))

        # Filters
        resulting_papers = self.__filter_papers(
            paper_after_expansion, callbacks)

        if remove_source_from_results:
            resulting_papers.difference_update(source_papers)

        return list(resulting_papers)
