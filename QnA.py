import requests
def qna(query):
    try:
        return requests.get(f"http://localhost:8000/api/search?q={query}")
    except:
        print("Server Error!")
