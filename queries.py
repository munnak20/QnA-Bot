from QnA import qna


def outputQuery():
    while(True):
        query= input("Please enter your query or to quit type q: ")
        if query=="q":
            break;
        output = qna(query)
        print(f"AI: {str(output.text)}")
        print("########################")
        print()
outputQuery()
