from fastapi import FastAPI

app = FastAPI()


@app.get("/{test}")
async def root(test: int):
    return {"message": "Hello World", "test_value": test}
