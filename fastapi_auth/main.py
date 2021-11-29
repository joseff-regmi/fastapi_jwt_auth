import uvicorn

if __name__ == "__main__":
    uvicorn.run("blogs.app:app", reload = True)