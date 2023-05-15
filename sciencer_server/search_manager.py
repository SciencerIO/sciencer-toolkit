from search import SearchConfiguration, SearchStatus, SearchCls
from typing import Optional


# create a search class manager
class SearchManager:
    def __init__(self):
        self.searches: list[SearchCls] = []
        self.search_id = 0

    def create_search(self, config: SearchConfiguration) -> Optional[SearchCls]:
        self.search_id += 1
        search = SearchCls(
            id=self.search_id, config=config
        )
        self.searches.append(search)
        return search

    def get_search(self, search_id: int) -> Optional[SearchCls]:
        for search in self.searches:
            if search.id == search_id:
                return search
        return None

    def delete_search(self, search_id: int) -> Optional[SearchCls]:
        for search in self.searches:
            if search.id == search_id:
                search.cancel()
                self.searches.remove(search)
                return search
        return None

    def delete_all_searches(self):
        for search in self.searches:
            search.cancel()
        self.searches = []
        return None
