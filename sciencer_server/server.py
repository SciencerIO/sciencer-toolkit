from fastapi import FastAPI
from search import SearchConfiguration, Search
from search_manager import SearchManager

manager = SearchManager()
server = FastAPI()


@server.get("/")
def read_root():
    return {"Hello": "World"}


@server.get("/searches")
def get_searches():
    searches = [Search.from_cls(search) for search in manager.searches]
    return {"searches": searches, "count": len(searches)}


@server.delete("/searches")
def delete_searches():
    manager.delete_all_searches()
    return {"message": "All searches deleted"}


@server.post("/search")
def create_search(config: SearchConfiguration):
    # TODO: validate config
    search = manager.create_search(config)
    return {"search": Search.from_cls(search)}


@server.get("/search/{search_id}")
def get_search(search_id: int):
    search = manager.get_search(search_id)
    if search is None:
        return {"error": "Search not found"}
    return {"search": Search.from_cls(search)}


@server.delete("/search/{search_id}")
def delete_search(search_id: int):
    search = manager.delete_search(search_id)
    if search is None:
        return {"error": "Search not found"}
    return {"search": Search.from_cls(search), "message": "Search deleted"}


@server.post("/search/{search_id}/run")
def run_search(search_id: int):
    search = manager.get_search(search_id)
    if search is None:
        return {"error": "Search not found"}
    search.run()
    return {"search": Search.from_cls(search)}


@server.post("/search/{search_id}/cancel")
def cancel_search(search_id: int):
    search = manager.get_search(search_id)
    if search is None:
        return {"error": "Search not found"}
    search.cancel()
    return {"search": Search.from_cls(search)}
