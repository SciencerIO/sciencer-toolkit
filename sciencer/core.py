""" Sciencer Core
"""
from typing import Dict, List
from sciencer.collectors.collector import Collector
from sciencer.expanders.expander import Expander
from sciencer.filters.filter import Filter
from sciencer.policies import Policy
from .providers.provider import Provider
from sciencer.models import Paper


class Callbacks:
    """Sciencer callbacks wrapper"""

    def on_paper_collected(self, paper: Paper) -> None:
        """Invoked when a new paper is collected.

        Args:
            paper (Paper): new paper collected.
        """

    def on_papers_expanded(self, papers: List[Paper], result: List[Paper]) -> None:
        """Invoked when new papers were expanded.

        Args:
            papers (List[Paper]): papers expanded.
            result (List[Paper]): papers resulting from expansion.
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
                self.__providers_by_policy[provider_policy].append(provider_to_add)

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

    def iterate(
        self,
        source_papers = None,
        remove_source_from_results: bool = False,
        callbacks: Callbacks = Callbacks(),
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
        if source_papers is None:
            source_papers = set()

            for collector in self.__collectors:
                providers_for_collector = self.__get_provider(
                    collector.available_policies
                )
                collected_papers = collector.execute(providers_for_collector)
                source_papers.update(collected_papers)
                for collected_paper in collected_papers:
                    callbacks.on_paper_collected(collected_paper)

        # Expanders

        paper_after_expansion = set(source_papers)

        for expander in self.__expanders:
            providers_for_expander = self.__get_provider(expander.available_policies)
            expansion_result = expander.execute(
                papers=source_papers, providers=providers_for_expander
            )
            paper_after_expansion.update(expansion_result)
            callbacks.on_papers_expanded(source_papers, expansion_result)

        # Filters
        papers_to_discard = set()

        for paper_to_filter in paper_after_expansion:
            for m_filter in self.__filters:
                if not m_filter.is_valid(paper_to_filter):
                    papers_to_discard.add(paper_to_filter)

        # Aggregate results
        resulting_papers = set()

        for paper in paper_after_expansion:
            if paper not in papers_to_discard:
                resulting_papers.add(paper)
                callbacks.on_paper_accepted(paper)
            else:
                callbacks.on_paper_rejected(paper)

        if remove_source_from_results:
            resulting_papers.difference_update(source_papers)


        return list(resulting_papers)
