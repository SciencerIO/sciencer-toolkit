""" Provider wrapper for Semantic Scholar API
"""
from typing import List, Optional
import time
import requests
from ..policies import Policy
from .provider import Provider
from ..models import Paper, PaperIDs


S2_FIELDS = ["title", "externalIds", "authors",
             "abstract", "year", "fieldsOfStudy"]
S2_NESTED_FIELDS = [
    "references.paperId", "citations.paperId"]
S2_URL_SINGLE_FIELDS = "".join([f"{field}," for field in S2_FIELDS])[:-1]
S2_URL_GROUP_FIELDS = "".join(
    [f"{field}," for field in S2_FIELDS + S2_NESTED_FIELDS])[:-1]

S2_MAXIMUM_PAPER_RESULTS_SEARCH = 9999


def add_external_ids(paper: Paper, external_ids_json) -> None:
    """Add external ids to a paper

    Args:
        paper (_type_): paper to receive the external ids
        external_ids_json (_type_): the external ids to add
    """
    # External IDS
    if "DOI" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.DOI,
                                  external_ids_json["DOI"])

    if "MAG" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.MAG,
                                  external_ids_json["MAG"])

    if "CorpusId" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.CORPUS,
                                  external_ids_json["CorpusId"])

    if "PubMed" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.PUBMED,
                                  external_ids_json["PubMed"])

    if "DBLP" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.DBLP,
                                  external_ids_json["DBLP"])

    if "ArXiv" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.ARXIV,
                                  external_ids_json["ArXiv"])

    if "ACL" in external_ids_json:
        paper.external_ids.add_id(PaperIDs.LABEL.ACL,
                                  external_ids_json["ACL"])


def create_paper_from_json(paper_json) -> Paper:
    """Create a Paper Object based on available json dictionary

    Args:
        paper_json (str): json data

    Returns:
        Paper: Paper model based on json data
    """
    paper = Paper(paper_json["paperId"])

    paper.title = paper_json["title"]

    if "externalIds" in paper_json:
        add_external_ids(paper, paper_json["externalIds"])

    if "authors" in paper_json:
        for author in paper_json["authors"]:
            paper.authors_ids.add(author["authorId"])

    if "abstract" in paper_json:
        paper.abstract = paper_json["abstract"]

    if "year" in paper_json and paper_json["year"] is not None:
        paper.year = paper_json["year"]

    if "references" in paper_json and len(paper_json["references"]) > 0:
        for ref in paper_json["references"]:
            paper.references_ids.add(ref['paperId'])

    if "citations" in paper_json and len(paper_json["citations"]) > 0:
        for ref in paper_json["citations"]:
            paper.citations_ids.add(ref['paperId'])

    if "fieldsOfStudy" in paper_json \
            and paper_json["fieldsOfStudy"] is not None \
            and len(paper_json["fieldsOfStudy"]) > 0:
        for field in paper_json["fieldsOfStudy"]:
            paper.fields_of_study.add(field)

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
            + f"fields={S2_URL_GROUP_FIELDS}"
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

        if response.status_code != 200:
            print(
                f"🚫 Error {response.status_code} has occured: {response.text}"
            )
            return None

        return create_paper_from_json(response.json())

    def get_papers_by_author(self, author_id: str = "") -> List[Paper]:
        resulting_papers = set()
        offset = 0

        while True:

            url = (
                f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?"
                + f"fields={S2_URL_GROUP_FIELDS}"
                + f"&offset={offset}"
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

            if response.status_code != 200:
                print(
                    f"🚫 Error {response.status_code} has occured: {response.text}"
                )
                break

            response_json = response.json()

            resulting_papers.update([create_paper_from_json(
                paper_json) for paper_json in response_json["data"]])

            if "next" not in response_json:
                break

            offset = response_json["next"]

        return list(resulting_papers)

    def get_paper_by_terms(self, terms: List[str], max_papers: int) -> List[Paper]:
        resulting_papers = set()
        offset = 0
        term_query = ''.join([f"{term}+"for term in terms])[:-1]
        remaining_papers = max_papers

        while True:
            if remaining_papers <= 0:
                break

            if offset >= S2_MAXIMUM_PAPER_RESULTS_SEARCH:
                break

            papers_to_retrieve = min(
                100, remaining_papers, S2_MAXIMUM_PAPER_RESULTS_SEARCH-offset)

            url = (
                f"https://api.semanticscholar.org/graph/v1/paper/search?query={term_query}"
                + f"&offset={offset}"
                + f"&limit={papers_to_retrieve}"
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

            if response.status_code != 200:
                print(
                    f"🚫 Error {response.status_code} has occured: {response.text}"
                )
                break

            response_json = response.json()

            resulting_papers.update([create_paper_from_json(
                paper_json) for paper_json in response_json["data"]])

            remaining_papers = max_papers - len(resulting_papers)

            if "next" not in response_json:
                break

            offset = response_json["next"]

        return list(resulting_papers)
