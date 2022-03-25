<div id="top"></div>
<h1 align="center">
  <br>
  Sciencer Toolkit
</h1>

<h4 align="center">A smarter way to find new articles.</h4>

<p align="center">
    <a href="https://pypi.org/project/sciencer-toolkit/">
    <img src="https://img.shields.io/pypi/dm/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/issues">
    <img src="https://img.shields.io/github/issues-raw/SciencerIO/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/SciencerIO/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests"></a>
    <a href="https://github.com/SciencerIO/sciencer-toolkit/LICENSE">
    <img src="https://img.shields.io/github/license/SciencerIO/sciencer-toolkit.svg?style=flat-square&logo=github&logoColor=white"
         alt="License: MIT License"></a>

</p>
            
<p align="center">
  <a href="#about">About</a> •
  <a href="#usage">Usage</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>
<p align="center">
  <a href="#collectors">Collectors</a> •
  <a href="#expanders">Expanders</a> •
  <a href="#filters">Filters</a> •
  <a href="#providers">Providers</a>
</p>

---

## About
Sciencer Toolkit enables researchers with the tools to **programmatically conduct a literature review** using an intuitive yet flexible interface.

Sciencer iteratively identifies a set of papers using **Expanders**. Each expander enlarges a set of papers to a larger set (e.g. using authors, citations, references, etc...). At the end of each iteration, each new paper needs to satisfy a series of **Filters** to be accepted. The initial set of papers is created using **Collectors** (e.g. by paper doi, author name).

This project was motivated by the absence of tools to automate systematic reviews using clear and well-defined criteria. Still, for literature reviews that do not need to follow specific criteria, there are a several tools that can help to discover new papers.

## Usage

```python
# Create the Sciencer Core Component
sciencer = Sciencer()

# Define provider
sciencer.add_provider(SemanticScholarProvider())

# Define collectors
sciencer.add_collector(sciencer.collectors.CollectByAuthorID(...))
sciencer.add_collector(sciencer.collectors.CollectByDOI(...))

# Define expanders
sciencer.add_expander(sciencer.expanders.ExpandByAuthors())

# Define filters
sciencer.add_filter(sciencer.filters.FilterByYear(min_year=2010, max_year=2030))
sciencer.add_filter(sciencer.filters.FilterByAbstract("social"))

# Run one iterations
results = sciencer.iterate()

```

For more examples on how to use the Sciencer toolkit, please check the directory `examples/`.

<p align="right">(<a href="#top">back to top</a>)</p>

## Collectors

| Name         | Description | Parameters |
| -----------  | :---------- | :--------- |           
| Author ID    | Collects all the papers written by an author | Authors's SemanticScholar ID |
| Paper DOI    | Collects a paper by its DOI | Paper's DOI |    

<p align="right">(<a href="#top">back to top</a>)</p>

## Expanders

| Name         | Description | 
| -----------  | :---------- | 
| Authors      | Expands a paper by its authors |

<p align="right">(<a href="#top">back to top</a>)</p>

## Filters

| Name                | Description |  Parameters  |
| -----------         | :---------: | ------------ |
| By Year             | Filters a paper by its year  | The lowest acceptable year (inclusive) <br> The highest acceptable year (inclusive) |
| By Abstract Words   | Filters a paper by its abstract | The collection of words the abstract should include (at least one)  |     

<p align="right">(<a href="#top">back to top</a>)</p>

## Providers


| Name        | Provider    | Features    |
| :----------: | :----------: | :----------- |
| Semantic Scholar      | [Semantic Scholar Academic Graph API](https://www.semanticscholar.org/product/api)       | **Search by Author** (Name, S2ID) <br> **Search By Paper ID** (S2ID, DOI, ArXiv, MAG, ACL, PubMed, Corpus)
| DBLP   |   [DBLP Search API](https://dblp.org/faq/How+to+use+the+dblp+search+API.html) | *Work in Progress*

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

Want to **add a new provider, filter or expander**? Looking to improve **the core functionality of sciencer toolkit**. We would look forward to include your contributions in the toolkit! If you have a suggestion that would improve the toolkit, please fork the repo and create a new pull request:
1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes 
4. Push to the Branch
5. Open a Pull Request

If you are looking for an additional collector/filter/expander/provider or just want to report a bug, you can also simply open an issue with the tag "enchament" or "bug", respectively.

<p align="right">(<a href="#top">back to top</a>)</p>
