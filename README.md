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
         alt="License: GPL-3.0"></a>

</p>
            
<p align="center">
  <a href="#about">About</a> •
  <a href="#usage">Usage</a> •
  <a href="#features">Features</a> •
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
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin libero justo, varius ac nulla non, lacinia bibendum arcu. Sed quis tempus ligula. Morbi convallis neque et dui imperdiet, sit amet venenatis lacus congue. 

Quisque quis nunc mauris. Sed id justo risus. Mauris egestas gravida convallis. Vivamus tempor, arcu id maximus venenatis, ligula felis convallis ligula, quis sollicitudin libero tortor in magna. Donec semper nec odio et porta. 

Etiam fringilla placerat congue. Nullam rutrum purus eu augue finibus, non ullamcorper risus convallis. Praesent accumsan sed eros vitae efficitur. Sed non odio a nisl blandit consectetur sed nec velit. Integer gravida lorem nisl, eget luctus libero sit. 

## Usage

<p align="right">(<a href="#top">back to top</a>)</p>

## Features

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin libero justo, varius ac nulla non, lacinia bibendum arcu. Sed quis tempus ligula. 

- Main feature One
- Main feature Two
  - Sub feature TwoOne
  - Sub feature TwoTwo
- Main feature Three

<p align="right">(<a href="#top">back to top</a>)</p>

## Collectors

| Name         | Description |  Parameters  |
| -----------  | :---------: | ------------ |
| Author ID |             |              |
| Paper ID  |             |              |     

<p align="right">(<a href="#top">back to top</a>)</p>

## Expanders

| Name         | Description |  Parameters  |
| -----------  | :---------: | ------------ |
| Authors      |             |              |

<p align="right">(<a href="#top">back to top</a>)</p>

## Filters

| Name                | Description |  Parameters  |
| -----------         | :---------: | ------------ |
| By Year             |             |              |
| By Abstract Words   |             |              |     

<p align="right">(<a href="#top">back to top</a>)</p>

## Providers


| Name        | Provider    | Features    |
| ----------- | ----------- | ----------- |
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
