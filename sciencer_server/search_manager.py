from search import SearchConfiguration, SearchStatus, SearchCls


# create a search class manager
class SearchManager:
    def __init__(self):
        self.searches = []
        self.search_id = 0

    def create_search(self, config: SearchConfiguration):
        self.search_id += 1
        search = SearchCls(
            id=self.search_id,
            status=SearchStatus.created,
            config=config,
            results=[]
        )
        self.searches.append(search)
        return search

    def get_search(self, search_id: int):
        for search in self.searches:
            if search.id == search_id:
                return search
        return None

    def delete_search(self, search_id: int):
        for search in self.searches:
            if search.id == search_id:
                # TODO: stop search if running
                self.searches.remove(search)
                return search
        return None
    
    def delete_all_searches(self):
        # TODO: stop all searches then delete all
        self.searches = []
        return None