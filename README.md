<div id="top"></div>
<h1 align="center">
  <br>
  Sciencer Toolkit
</h1>

<h4 align="center">A smarter way to find articles.</h4>

<p align="center">
    <a href="https://pypi.org/project/sciencer/">
    <img src="https://img.shields.io/pypi/dm/sciencer.svg?style=flat-square"
         alt="GitHub pull requests"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/issues">
    <img src="https://img.shields.io/github/issues-raw/SciencerIO/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/SciencerIO/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/LICENSE">
    <img src="https://img.shields.io/github/license/SciencerIO/sciencer-toolkit.svg?style=flat-square"
         alt="License: MIT License"></a>

</p>

<p align="center">
  <a href="#about">About</a> -
  <a href="#usage">Usage</a> -
  <a href="#roadmap">Roadmap</a> -
  <a href="#contributing">Contributing</a>
</p>
<p align="center">
  <a href="#collectors">Collectors</a> -
  <a href="#expanders">Expanders</a> -
  <a href="#filters">Filters</a> -
  <a href="#providers">Providers</a>
</p>

---

## About
Sciencer Toolkit enables researchers to **programmatically conduct a literature review** using an intuitive yet flexible interface.

At its core, Sciencer collects sets of papers.
The initial set of papers is created through the use of **Collectors** (e.g. paper doi, author name).
Then, Sciencer iteratively finds new papers using **Expanders** (e.g. authors, citations, references).
Finally, new found papers need to satisfy a series of **Filters** in order to be accepted into the current set.
Being iterative in nature, Sciencer allows you to repeat the above steps has many times as you'd like.

This project was motivated by the absence of tools to automate systematic reviews using clear and well-defined criteria.
Still, for literature reviews that do not need to follow specific criteria, there are a several tools that can help to discover new papers.

## Usage

```python
# Create the Sciencer Core Component
sciencer = Sciencer()

# Define provider
sciencer.add_provider(SemanticScholarProvider())

# Define collectors
## this collector will gather all known papers authored by "John Doe" into de set
sciencer.add_collector(sciencer.collectors.CollectByAuthorID("John Doe"))
## this collector will collect the paper with DOI "1234567890" into the set
sciencer.add_collector(sciencer.collectors.CollectByDOI("1234567890"))

# Define expanders
## this expander will gather all known papers written by authors in the current set.
sciencer.add_expander(sciencer.expanders.ExpandByAuthors())

# Define filters
## this filter will reject papers that were published before 2010 and after 2030
sciencer.add_filter(sciencer.filters.FilterByYear(min_year=2010, max_year=2030))
## this filter will reject all the appers that do not have the word social on the abstract
sciencer.add_filter(sciencer.filters.FilterByAbstract("social"))

# Run one iteration
results = sciencer.iterate()

```

For more examples on how to use the Sciencer toolkit, please check the directory `examples/`.

<p align="right">(<a href="#top">back to top</a>)</p>

## Collectors

| Name      | Description                                  | Parameters                   |
| --------- | :------------------------------------------- | :--------------------------- |
| Author ID | Collects all the papers written by an author | Authors's SemanticScholar ID |
| Paper DOI | Collects a paper by its DOI                  | Paper's DOI                  |

<p align="right">(<a href="#top">back to top</a>)</p>

## Expanders

| Name    | Description                    |
| ------- | :----------------------------- |
| Authors | Expands a paper by its authors |

<p align="right">(<a href="#top">back to top</a>)</p>

## Filters

| Name              | Description                     | Parameters                                                                          |
| ----------------- | :------------------------------ | ----------------------------------------------------------------------------------- |
| By Year           | Filters a paper by its year     | The lowest acceptable year (inclusive) <br> The highest acceptable year (inclusive) |
| By Abstract Words | Filters a paper by its abstract | The collection of words the abstract should include (at least one)                  |

<p align="right">(<a href="#top">back to top</a>)</p>

## Providers


|       Name       |                                      Provider                                      | Features                                                                                                   |
| :--------------: | :--------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------- |
| Semantic Scholar | [Semantic Scholar Academic Graph API](https://www.semanticscholar.org/product/api) | **Search by Author** (Name, S2ID) <br> **Search By Paper ID** (S2ID, DOI, ArXiv, MAG, ACL, PubMed, Corpus) |
|       DBLP       |    [DBLP Search API](https://dblp.org/faq/How+to+use+the+dblp+search+API.html)     | *Work in Progress*                                                                                         |

<p align="right">(<a href="#top">back to top</a>)</p>

## Roadmap

- [ ] Create Paper's and Author's Cache
- [x] Add Bulk Expanders (to avoid redundancy)
- [ ] Add support for multithreading
- [ ] Add Collectors
  - [ ] Add Collect by Venue/Proceedings
- [ ] Add Expanders
  - [ ] Add Expand by Citations
  - [ ] Add Expand by References
  - [ ] Add Expand by Venue/Proceedings
- [ ] Add Filters
  - [ ] Add Filter by Number of Citations
  - [ ] Add Filter by Topic
  - [ ] Add Filter by Keywords
- [ ] Add Compound Filters
- [ ] Add utility to write results to a *.csv

See the [open issues](https://github.com/SciencerIO/sciencer-toolkit/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Want to **add a new provider, filter or expander**?
Looking to improve **the core functionality of sciencer toolkit**.
We look forward to include your contributions in the toolkit!
If you have a suggestion that would improve the toolkit just send us a Pull Request!

If you are looking for an additional collector/filter/expander/provider or just want to report a bug, you can also simply open an issue with the tag "enchament" or "bug", respectively.

<p align="right">(<a href="#top">back to top</a>)</p>
