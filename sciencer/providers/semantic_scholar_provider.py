""" Provider wrapper for Semantic Scholar API
"""
from typing import List, Optional
import time
import requests
from ..policies import Policy
from .provider import Provider
from ..models import Paper, PaperIDs


S2_FIELDS = ["title", "externalIds", "authors", "abstract", "year"]
S2_URL_SINGLE_FIELDS = "".join([f"{field}," for field in S2_FIELDS])[:-1]



def create_paper_from_json(paper_json) -> Paper:
    """Create a Paper Object based on available json dictionary

    Args:
        paper_json (str): json data

    Returns:
        Paper: Paper model based on json data
    """
    paper = Paper(paper_json["paperId"])

    # External IDS
    if "DOI" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.DOI, paper_json["externalIds"]["DOI"])

    if "MAG" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.MAG, paper_json["externalIds"]["MAG"])

    if "CorpusId" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.CORPUS, paper_json["externalIds"]["CorpusId"])

    if "PubMed" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.PUBMED, paper_json["externalIds"]["PubMed"])

    if "DBLP" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.DBLP, paper_json["externalIds"]["DBLP"])

    if "ArXiv" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.ARXIV, paper_json["externalIds"]["ArXiv"])

    if "ACL" in paper_json["externalIds"]:
        paper.set_external_id(PaperIDs.LABEL.ACL, paper_json["externalIds"]["ACL"])

    paper.set_title(paper_json["title"])

    if "authors" in paper_json:
        for author in paper_json["authors"]:
            paper.add_author(author["authorId"])

    if "abstract" in paper_json:
        paper.set_abstract(paper_json["abstract"])

    if "year" in paper_json and paper_json["year"] is not None:
        paper.set_year(paper_json["year"])

    return paper


class SemanticScholarProvider(Provider):
    """Provider for Semantic Scholar"""

    def __init__(self, api_key: str = "") -> None:
        self.__api_key: str = api_key
        super().__init__(policies=[Policy.BY_DOI,
                                   Policy.BY_AUTHOR,
                                   Policy.BY_QUERY])

    def get_paper_by_id(self, paper_id) -> Optional[Paper]:
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?"
            + f"fields={S2_URL_SINGLE_FIELDS}"
        )
        response = requests.get(url, headers={"x-api-key": self.__api_key})

        while response.status_code == 429:
            print(
                "⌛ Too many requests to Semantic Scholar. Waiting for 1 minute before restarting..."
            )
            for seconds in range(0, 1 * 60):
                print(f"{1*60 - seconds} seconds remaining", end="\r")
                time.sleep(1)

            response = requests.get(url, headers={"x-api-key": self.__api_key})

        return create_paper_from_json(response.json())

    def get_papers_by_author(self, author_id: str = "") -> List[Paper]:
        resulting_papers = set()
        offset_id = 0

        while True:

            url = (
                f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?"
                + f"fields={S2_URL_SINGLE_FIELDS}"
                + f"&offset={offset_id}"
            )

            response = requests.get(url, headers={"x-api-key": self.__api_key})

            while response.status_code == 429:
                print(
                    "⌛ Too many requests to Semantic Scholar. \
                    Waiting for 1 minute before restarting..."
                )
                for seconds in range(0, 1 * 60):
                    print(f"{1*60 - seconds} seconds remaining", end="\r")
                    time.sleep(1)

                response = requests.get(
                    url, headers={"x-api-key": self.__api_key})

            response_json = response.json()

            resulting_papers.update([create_paper_from_json(
                paper_json) for paper_json in response_json["data"]])

            if "next" not in response_json:
                break

            offset_id = response_json["next"]

        return list(resulting_papers)

    def get_paper_by_terms(self, terms: List[str], max_papers: int) -> List[Paper]:
        resulting_papers = set()
        offset_id = 0
        term_query = ''.join([f"{term}+"for term in terms])[:-1]

        while True:
            url = (
                f"https://api.semanticscholar.org/graph/v1/paper/search?query={term_query}"
                + f"&offset={offset_id}"
                + "&limit=100"
                + f"&fields={S2_URL_SINGLE_FIELDS}"
            )

            response = requests.get(url, headers={"x-api-key": self.__api_key})

            while response.status_code == 429:
                print(
                    "⌛ Too many requests to Semantic Scholar. \
                    Waiting for 1 minute before restarting..."
                )
                for seconds in range(0, 1 * 60):
                    print(f"{1*60 - seconds} seconds remaining", end="\r")
                    time.sleep(1)

                response = requests.get(
                    url, headers={"x-api-key": self.__api_key})

            response_json = response.json()

            resulting_papers.update([create_paper_from_json(
                paper_json) for paper_json in response_json["data"]])

            if "next" not in response_json:
                break

            if len(resulting_papers) > max_papers:
                break

            offset_id = response_json["next"]

        return list(resulting_papers)
