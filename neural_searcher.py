import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm.auto import tqdm
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 


OPENAI_API_KEY="Enter your openai API key here"

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")


    def search(self, text: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,  
            limit=5  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        payloads = [hit.payload for hit in search_result]
        return payloads
    
    def get_response_from_openai(self, query):
        query_prompt = """\
        For the following query \
        that is delimited by triple backticks \
        do the following task:
        task1: if it is a question then answer it in a complete sentence  \
        according to the context of documents \
        that is delimited by triple backticks \

        if you do not know the answer then output as "I don't Know"

        please format your output in following manner:
        answer: response to task1





        query:```{query}```
        documents : ```{docs}```

        """
        docs=self.search(query)
        prompt = PromptTemplate(template=query_prompt, input_variables=["query","docs"])
        llm_chain = LLMChain(prompt=prompt,
                        llm=ChatOpenAI(api_key=OPENAI_API_KEY,
                                        model_name="gpt-3.5-turbo")
                        )
        return llm_chain.run({"query":query,'docs':docs})

