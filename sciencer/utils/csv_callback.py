from sciencer.core import Callbacks
from sciencer.models import Paper
from typing import Dict
import csv

def convert_to_row(paper: Paper) -> Dict[str, str]:
    row = {}
    row['title'] = paper.title
    row['year'] = paper.year
    return row

class WriteToCSVCallbacks(Callbacks):
    
    def __init__(self, file_path: str) -> None:
        field_names = ['title', 'year', 'accepted']
        self.__file = open(file_path, mode='w', newline='', encoding="utf-8")
        self.__writer = csv.DictWriter(self.__file, fieldnames=field_names)
        self.__writer.writeheader()
        
    def on_paper_accepted(self, paper: Paper) -> None:
        row_paper = convert_to_row(paper)
        row_paper['accepted'] = 'true'
        self.__writer.writerow(row_paper)
        
        