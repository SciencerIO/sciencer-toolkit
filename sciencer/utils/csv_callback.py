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
    row['authors_s2_id'] =  "["+''.join([f"{author_id};" for author_id in paper.authors])[:-1]+"]"
    return row

field_names = ['title', 'authors_s2_id', 'year', 'accepted']

class WriteToCSVCallbacks(Callbacks):
    """Class that writes to a csv file
       The csv file includes all the papers considered during the expansion
       Each entry includes the paper's title, authors (S2 Ids), year, and if it was accepted
    """
    def __init__(self, file_path: str) -> None:
        self.__path = file_path
        with open(self.__path, mode='w', newline='', encoding="utf-8") as file:
            self.__writer = csv.DictWriter(file, fieldnames=field_names)
            self.__writer.writeheader()

    def on_paper_accepted(self, paper: Paper) -> None:
        row_paper = convert_to_row(paper)
        row_paper['accepted'] = 'true'
        with open(self.__path, mode='a', newline='', encoding="utf-8") as file:
            self.__writer = csv.DictWriter(file, fieldnames=field_names)
            self.__writer.writerow(row_paper)

    def on_paper_rejected(self, paper: Paper) -> None:
        row_paper = convert_to_row(paper)
        row_paper['accepted'] = 'false'
        with open(self.__path, mode='a', newline='', encoding="utf-8") as file:
            self.__writer = csv.DictWriter(file, fieldnames=field_names)
            self.__writer.writerow(row_paper)
