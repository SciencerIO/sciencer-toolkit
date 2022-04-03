""" 3. Save to CSV
"""
import sciencer

if __name__ == "__main__":

    # Providers
    s2_provider = sciencer.providers.SemanticScholarProvider()

    # Collect
    col_author = sciencer.collectors.CollectByAuthorID("2262347")

    # Filters
    filter_year = sciencer.filters.FilterByYear(min_year=1920, max_year=1940)

    # Setup sciencer
    s = sciencer.Sciencer()
    s.add_provider(s2_provider)
    s.add_collector(col_author)
    s.add_filter(filter_year)

    # Setup
    csv_callback = sciencer.utils.WriteToCSVCallbacks("data.csv")
    first_batch = s.iterate(callbacks=csv_callback)
