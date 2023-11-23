from fastapi import FastAPI
# The file where NeuralSearcher is stored
from neural_searcher import NeuralSearcher

app = FastAPI()

# Create a neural searcher instance
neuralSearcher = NeuralSearcher(collection_name='big_basket_product')

@app.get("/api/search")
def search_startup(q: str):
    answer = neuralSearcher.get_response_from_openai(q)
    return answer[8:]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
