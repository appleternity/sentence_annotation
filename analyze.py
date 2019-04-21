import json
import re
import os, os.path
import pandas as pd
import xlsxwriter

def analyze():
    dir_path = "/home/appleternity/workspace/lab/NLPSA/annotation/result"
    filenames = [f for f in os.listdir(dir_path) if ".swp" not in f]
    
    question_pattern = re.compile("<QuestionIdentifier>(?P<q_name>.*?)</QuestionIdentifier>")
    answer_pattern = re.compile("<FreeText>(?P<q_name>.*?)</FreeText>")

    results = {}
    for filename in filenames:
        with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            for d in data:
                questions = question_pattern.findall(d["Answer"])
                answers = answer_pattern.findall(d["Answer"])
                temp = {}
                for question, answer in zip(questions, answers):
                    temp[question] = answer

                if temp["memo"] not in results:
                    results[temp["memo"]] = []
                results[temp["memo"]].append(int(temp["q1"]))

    with open("result.json", 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, indent=4)
   
    # integrate sentences into result
    with open("wordset.json", 'r', encoding='utf-8') as infile:
        wordsets = json.load(infile)

    with open("sentences_processed.json", 'r', encoding='utf-8') as infile:
        sent_data = json.load(infile)

    with open("useful.json", 'r', encoding='utf-8') as infile:
        useful = json.load(infile)

    sentences = [display_sent(s) for w1, w2 in wordsets for s in sent_data[w1]+sent_data[w2]]
     
    # turn result into table form
    keys = sorted([k for k in results.keys()], key=lambda x: int(x.split("|")[-1]))
    table = [[key] + results[key]  for key in keys]

    # useful column
    useful_column = [useful[key] for key in keys]

    df = pd.DataFrame(table)
    df["mean"] = df.mean(axis=1, numeric_only=True)
    df["usefulness"] = useful_column
    df["sentence"] = sentences
    df.rename(columns={0:'setting'}, inplace=True)

    df.to_excel("result.xlsx", sheet_name="mturk_result")

def display_sent(sent):
    result = sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        #"<strong>{}</strong>".format(sent["tokens"][sent["target_index"]][0])
        sent["tokens"][sent["target_index"]][0],
    )
    return result

def get_my_result():
    # missing one item "skillful|skilled|skillful|48": 2

    dir_path = "/home/appleternity/workspace/lab/NLPSA/annotation/my_result"
    filenames = [f for f in os.listdir(dir_path) if ".swp" not in f]

    question_pattern = re.compile("<QuestionIdentifier>(?P<q_name>.*?)</QuestionIdentifier>")
    answer_pattern = re.compile("<FreeText>(?P<q_name>.*?)</FreeText>")
    
    results = {}
    for filename in filenames:
        with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            for d in data:
                questions = question_pattern.findall(d["Answer"])
                answers = answer_pattern.findall(d["Answer"])
                temp = {}
                for question, answer in zip(questions, answers):
                    temp[question] = answer

                results[temp["memo"]] = int(temp["q1"])
    
    #with open("result.json", 'w', encoding='utf-8') as outfile:
    #    json.dump(results, outfile, indent=4)
    
    keys = sorted([k for k in results.keys()], key=lambda x: int(x.split("|")[-1]))
    print(keys)


def main():
    analyze()
    #get_my_result()

if __name__ == "__main__":
    main()
