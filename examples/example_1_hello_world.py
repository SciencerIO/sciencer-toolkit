""" 1. Basic Example

Showcase of the Basic components of Sciencer:
- Collectors
- Expanders
- Filters
- Providers
"""
from typing import List
from datetime import datetime
import sciencer

# Add callbacks


class custom_callbacks(sciencer.Callbacks):
    def on_paper_collected(self, paper: sciencer.Paper, collector: sciencer.collectors.Collector) -> None:
        print(f"Paper {paper} collected by {collector} !")

    def on_paper_expanded(self, new_paper: sciencer.Paper, expander: sciencer.expanders.Expander, source_paper: sciencer.Paper) -> None:
        print(
            f"Paper {new_paper} was expanded by {expander} from {source_paper}")

    def on_paper_filtered(self, paper: sciencer.Paper, filter_executed: sciencer.filters.Filter, result: bool) -> None:
        print(
            f"Paper {paper} was filtered by {filter_executed} and got {result}")

    def on_paper_accepted(self, paper: sciencer.Paper) -> None:
        print(f"Paper {paper} accepted!")

    def on_paper_rejected(self, paper: sciencer.Paper) -> None:
        print(f"Paper {paper} rejected!")


if __name__ == "__main__":

    # Providers
    s2_provider = sciencer.providers.SemanticScholarProvider(api_key="")

    # Collect
    col_doi = sciencer.collectors.CollectByDOI("10.1093/mind/LIX.236.433")
    col_author_id = sciencer.collectors.CollectByAuthorID("2262347")
    col_terms = sciencer.collectors.CollectByTerms(
        terms=['social', 'intelligence', 'machines', 'cognition', 'emotional', 'human'], max_papers=125)

    # Expanders
    exp_author = sciencer.expanders.ExpandByAuthors()
    exp_references = sciencer.expanders.ExpandByReferences()
    exp_citations = sciencer.expanders.ExpandByCitations()

    # Filters
    # After 2010
    filter_year = sciencer.filters.FilterByYear(min_year=2010, max_year=2030)

    # Has 'social' word
    filter_social_in_abstract = sciencer.filters.FilterByAbstract("social")

    # Setup sciencer
    s = sciencer.Sciencer()
    s.add_provider(s2_provider)
    s.add_collector(col_doi)
    s.add_collector(col_author_id)
    s.add_collector(col_terms)
    s.add_expander(exp_author)
    s.add_expander(exp_references)
    s.add_expander(exp_citations)
    s.add_filter(filter_year)
    s.add_filter(filter_social_in_abstract)

    callbacks = custom_callbacks()

    print("📚 Processing papers...")

    # Iterate once
    start_time = datetime.now()
    print("1. Starting first iteration...")
    first_batch = s.iterate(
        remove_source_from_results=True, callbacks=[callbacks])
    print(
        f" 📜 First iteration collected {len(first_batch)} papers in {(datetime.now() - start_time).total_seconds()} seconds"
    )

    # Iterate Again
    start_time = datetime.now()
    print("2. Starting second iteration...")
    second_batch = s.iterate(source_papers=first_batch)
    print(
        f" 📜 Second iteration collected {len(first_batch)} papers in {(datetime.now() - start_time).total_seconds()} seconds"
    )
