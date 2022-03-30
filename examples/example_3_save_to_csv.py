""" 3. Save to CSV
"""
import sciencer

if __name__ == "__main__":

    # Providers
    s2_provider = sciencer.providers.SemanticScholarProvider()

    # Collect
    col_information_theory = sciencer.collectors.CollectByTerms(terms=['information', 'theory'], max_papers=1)

    # Expanders
    exp_author = sciencer.expanders.ExpandByAuthors()

    # Filters
    filter_year = sciencer.filters.FilterByYear(min_year=2018, max_year=2020)

    # Setup sciencer
    s = sciencer.Sciencer()
    s.add_provider(s2_provider)
    s.add_collector(col_information_theory)
    s.add_expander(exp_author)
    s.add_filter(filter_year)

    # Setup
    csv_callback = sciencer.utils.WriteToCSVCallbacks("data.csv")
    first_batch = s.iterate(remove_source_from_results=True, callbacks=csv_callback)
    second_batch = s.iterate(source_papers=first_batch, callbacks=csv_callback)