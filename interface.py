import requests
import ujson as json

def tokenize_pos(sent):
    res = requests.post(
        "http://localhost:9000", 
        params={
            "properties": json.dumps({
                "annotators":"tokenize,pos",
                "outputFormat":"json"
            })
        },
        data=sent.encode("utf-8"),
    )
    res = json.loads(res.text)
    return res

# dep json format
def dep_str(data):
    return "\n".join(
        "{}({}-{}, {}-{})".format(
            d["dep"],
            d["governorGloss"],
            d["governor"],
            d["dependentGloss"],
            d["dependent"]
        )
        for d in data        
    )

# sentence_info
def get_sentence(data, sent):
    start = data["tokens"][0]["characterOffsetBegin"]
    end = data["tokens"][-1]["characterOffsetEnd"]
    return sent[start:end]

def parsed_dep(sent):
    res = requests.post(
        "http://localhost:9000", 
        params={
            "properties": json.dumps({
                "annotators":"parse,depparse",
                "outputFormat":"json"
            })
        },
        data=sent.encode("utf-8"),
    )
    res = json.loads(res.text)
    return res

def test():
    from pprint import pprint

    res = tokenize_pos("There are three endpoints provided by the server, which we’ll describe in more detail below.")
    res = parsed_dep("          There are three endpoints provided by the server, which we’ll describe in more detail below.")
    sent = "          There are three endpoints provided by the server, which we’ll describe in more detail below."
    pprint(res)
    s = dep_str(res["sentences"][0]["enhancedPlusPlusDependencies"])
    print(s)
    print(res["sentences"][0]["parse"])

if __name__ == "__main__":
    test()

