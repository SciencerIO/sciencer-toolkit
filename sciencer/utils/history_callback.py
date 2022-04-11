"""Callbacks to report the history of a paper during one iteration
"""

from typing import List, Dict, Tuple
from sciencer.core import Callbacks
from sciencer.models import Paper
from sciencer.collectors import Collector
from sciencer.expanders import Expander
from sciencer.filters import Filter


class HistoryLog:
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

    @property
    def collectors(self) -> List[Collector]:
        """The collectors used to retrieve this paper
        """
        return self.__collected_from

    @property
    def expanders(self) -> List[Tuple[Paper, Expander]]:
        """The expanders that gathered this papers
        """
        return self.__expanded_from

    @property
    def filters(self) -> List[Tuple[Filter, bool]]:
        """The filters applied to this paper
        """
        return self.__filtered_by


class HistoryCallbacks(Callbacks):
    """Logs the history of all the papers
    """

    def __init__(self) -> None:
        self.__paper_logs: Dict[Paper, HistoryLog] = {}

    def on_paper_collected(self, paper: Paper, collector: Collector) -> None:
        if paper not in self.__paper_logs:
            self.__paper_logs[paper] = HistoryLog(paper)
        self.__paper_logs[paper].add_collector_source(collector)

    def on_paper_expanded(self, new_paper: Paper, expander: Expander, source_paper: Paper) -> None:
        if new_paper not in self.__paper_logs:
            self.__paper_logs[new_paper] = HistoryLog(new_paper)
        self.__paper_logs[new_paper].add_expander_source(
            expander, source_paper)

    def on_paper_filtered(self, paper: Paper, filter_executed: Filter, result: bool) -> None:
        if paper not in self.__paper_logs:
            self.__paper_logs[paper] = HistoryLog(paper)
        self.__paper_logs[paper].add_filter_tested(filter_executed, result)

    @property
    def papers_history(self) -> Dict[Paper, HistoryLog]:
        """The history of all papers mentioned during the expansion
        Returns:
            Dict[Paper, HistoryLog]: A dictionary mapping each paper and respective log
        """        """"""
        return self.__paper_logs

    def dump(self) -> None:
        """Dumps the history of all the papers registered in the callback
        """
        for paper, log in self.__paper_logs.items():
            print(f"# {paper.title}")
            if len(log.collectors) > 0:
                print("## Collectors:")
                for collector in log.collectors:
                    print(f" > {str(collector)}")
            if len(log.expanders) > 0:
                print("## Expanders:")
                for expander in log.expanders:
                    print(f" > {str(expander[1])} + {str(expander[0])}")
            if len(log.filters) > 0:
                print("## Filters:")
                for m_filter in log.filters:
                    print(f" > {str(m_filter[0])} => {m_filter[1]}")
            print()
