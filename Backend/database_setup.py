import pandas as pd
import numpy as np
import csv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm.auto import tqdm
from typing import List
from qdrant_client.models import PointStruct


file_path = 'bigBasketProducts.csv'
df = pd.read_csv(file_path, encoding="utf8")

columns_to_check = ['product', 'description']  #if product or description has null value then remove that cell
df = df.dropna(subset=columns_to_check)

value_to_replace = 0  #if rating has null value then replace it with 0
df['rating'].fillna(value_to_replace, inplace=True)


client = QdrantClient("http://localhost:6333")

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
    )

collection_vector_count = client.get_collection(collection_name=collection_name).vectors_count
print(f"Vector count in collection: {collection_vector_count}")
assert collection_vector_count == len(df)


