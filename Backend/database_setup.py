import pandas as pd
import numpy as np
import csv
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm.auto import tqdm
from typing import List
from langchain import  PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from qdrant_client.models import PointStruct
file_path = 'bigBasketProducts.csv'
df = pd.read_csv(file_path, encoding="utf8")

columns_to_check = ['product', 'description']  #if product or description has null value then remove that cell
df = df.dropna(subset=columns_to_check)

value_to_replace = 0  #if rating has null value then replace it with 0
df['rating'].fillna(value_to_replace, inplace=True)


#API_KEY = "hkVu34x5uMUBeQASgjNLPyVakYs9LLtJQVGOOUxRazCjh1hZ4uOz8A"
client = QdrantClient("http://localhost:6333")

#with open("bigBasketProducts.csv", encoding="utf8") as csvfile:
#    reader = csv.DictReader(csvfile)
#    document = list(reader)

#setup the collection
collection_name = "big_basket_product"
collections = client.get_collections()
if collection_name not in [c.name for c in collections.collections]:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        ),
    )
collections = client.get_collections()
print(collections)    


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")



 
"""
client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=embedding_model.encode(doc["description"]).tolist(),
                payload=doc
                )
            for idx, doc in enumerate(document)
            ]
        )
"""
batch_size = 512 
for index in tqdm(range(0, len(df), batch_size)):
    i_end = min(index + batch_size, len(df))  # find end of batch
    batch = df.iloc[index:i_end]  # extract batch
    emb = embedding_model.encode(batch["description"].tolist())  # generate embeddings for batch
    meta = batch.to_dict(orient="records")  # get metadata
    ids = list(range(index, i_end))  # create unique IDs for each vector
    # upsert to qdrant
    client.upsert(
        collection_name=collection_name,
        points=models.Batch(ids = ids, vectors=emb, payloads=meta)
        #points=[
        #    PointStruct(
        #        id=ids,
        #        vector = emb,
        #        payload=meta
        #    )
        #]
    )

collection_vector_count = client.get_collection(collection_name=collection_name).vectors_count
print(f"Vector count in collection: {collection_vector_count}")
assert collection_vector_count == len(df)


print("All is well")
