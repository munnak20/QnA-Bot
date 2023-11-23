from QnA import qna


def outputQuery(query):
    print("########################")
    print(f"User: \"{query}\"")
    output = qna(query)
    print(f"AI: {str(output.text)}")
    print("########################")
    print()

query1 = "Which product contains garlic oil?"

query2 = "Tell me something about Pudina Chutney Masala"

query3 = "Tell me the best perfume for men "

outputQuery(query1)
outputQuery(query2)
outputQuery(query3)
