"""WriteToCSV Callbacks
"""
import csv
from typing import Dict

from sciencer.core import Callbacks
from sciencer.models import Paper


def convert_to_row(paper: Paper) -> Dict[str, str]:
    """Converts a paper into a dictionary

    Args:
        paper (Paper): paper to conver

    Returns:
        Dict[str, str]: paper's properties
    """
    row = {}
    row['title'] = paper.title if paper.title is not None else ""
    row['year'] = str(paper.year) if paper.year is not None else ""
    return row

class WriteToCSVCallbacks(Callbacks):
    """Class that writes to a csv file
    """
    def __init__(self, file_path: str) -> None:
        field_names = ['title', 'year', 'accepted']
        self.__file = open(file_path, mode='w', newline='', encoding="utf-8")
        self.__writer = csv.DictWriter(self.__file, fieldnames=field_names)
        self.__writer.writeheader()

    def on_paper_accepted(self, paper: Paper) -> None:
        row_paper = convert_to_row(paper)
        row_paper['accepted'] = 'true'
        self.__writer.writerow(row_paper)
