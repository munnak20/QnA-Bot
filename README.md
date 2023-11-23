# QnA-Bot

### Table of Contents

- [Description](#description)
- [Technologies](#technology)
- [References](#references)

---

## Description
This Project aims to create a versatile chat-bot capable of processing natural language queries(English) and providing answer based on the relevant information from a CSV data source. 


#### Technologies

- Python
- Langchain
- Qdrant
- Docker 
- openai

---


#### Steps to run
Download docker
Before you start, please ensure Docker is installed and running on your system.
Make sure you have Python and pip is installed on your system.


#Download and Run
First, download the latest Qdrant image from Dockerhub:
```pip
docker pull qdrant/qdrant
```

Then, run the service:
```pip
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

Now Qdrant is accesible on:
```pip
localhost:6333/dashboard
```

Clone this repository to your system:
```pip
git clone https:
```
Install requirements:
```pip
pip install -r requirements.txt
```

Now run database_setup.py file:
```pip
python database_setup.py
```

Make sure you are in the same directory.

Now get your Openai key  from [link](https://platform.openai.com/api-keys) and put it in "neural_searcher.py" file:
```pip
OPENAI_API_KEY="your openai key"
```

Now run service.py file:
```pip
python service.py
```

Now your backend server is running on:
```pip
http://localhost:8000/api/search
```

Finally run "queries.py" file:
```pip
python queries.py
```









## References
[Qdrant](https://qdrant.tech/documentation/quick-start/)
---
[Qdrant_Neural_search](https://qdrant.tech/documentation/tutorials/neural-search/)
---
[Langchain](https://python.langchain.com/docs/modules/chains/foundational/llm_chain)
---


