import uvicorn
import server

if __name__ == "__main__":
    uvicorn.run('server:server', host="0.0.0.0", port=8000, reload=True)