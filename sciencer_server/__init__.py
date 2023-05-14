"""Sciencer Toolkit REST API Server.
See https://github.com/SciencerIO/sciencer-toolkit/ for more information.
"""
__version__ = "0.1.0"

from .server import server
from .search import SearchConfiguration, SearchStatus, Search, SearchCls
from .search_manager import SearchManager