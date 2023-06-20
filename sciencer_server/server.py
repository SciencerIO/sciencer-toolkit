from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import SearchConfiguration, Search, ResultsIncludes
from search_manager import SearchManager

manager = SearchManager()
server = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    # for the development of the webapp locally.
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    # for production
    "http://www.sciencer.world",
    "https://www.sciencer.world",
    "http://www.sciencer.world:8080",
    "https://www.sciencer.world:8080",
]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def create_search(config: list[SearchConfiguration]):
    # TODO: validate config
    search = manager.create_search(config)
    if search is None:
        return {"error": "Search not created"}
    return {"search": Search.from_cls(search)}


@server.get("/search/{search_id}")
def get_search(search_id: int, include_results: list[ResultsIncludes] = []):
    search = manager.get_search(search_id)
    if search is None:
        return {"error": "Search not found"}
    return {"search": Search.from_cls(search, include_results)}


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
