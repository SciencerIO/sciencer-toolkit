import uvicorn
import server

if __name__ == "__main__":
    uvicorn.run('server:server', host="127.0.0.1", port=8000, reload=True)