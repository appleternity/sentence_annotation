import csv
import json
import sys
sys.path.append("/home/appleternity/tool/stanford-corenlp-full-2017-06-09")
import numpy as np
import os

from nltk.stem import WordNetLemmatizer
from interface import tokenize_pos

def parsing():
    with open("sentences.csv", 'r') as infile:
        reader = csv.reader(infile)
        data = [row for row in reader]
    data = np.array(data)
    data = data.transpose()

    result = {}
    for row in data:
        word = row[0].strip()
        result[word] = []
        for sent in row[1:]:
            sent = sent.strip()
            res = tokenize_pos(sent)
            result[word].append({
                "sentence":sent,
                #"tokenized":res["sentences"][0]["tokens"]
                "tokenized":[token for s in res["sentences"] for token in s["tokens"]],
            })

    with open("sentences.json", 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, indent=4)


def find_target_word_with_pos(stemmer, pos_list, word):
    for index, (w, pos) in enumerate(pos_list):
        if "V" in pos:
            stem_word = stemmer.lemmatize(w, "v")
        elif "NN" in pos:
            stem_word = stemmer.lemmatize(w, "n")
        elif "JJ" in pos:
            stem_word = stemmer.lemmatize(w, "a")
        elif "RB" in pos:
            stem_word = stemmer.lemmatize(w, "r")
        else:
            stem_word = stemmer.lemmatize(w)
        if stem_word == word:
            return index
    return -1

def preprocessing():
    stemmer = WordNetLemmatizer()

    with open("sentences.json", 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    for word, sent_list in data.items():
        print(word)
        result = []
        for sent in sent_list:
            tokens = [(t["word"], t["pos"]) for t in sent["tokenized"]]
            target_index = find_target_word_with_pos(stemmer, tokens, word)
            if target_index == -1:
                print("GGGGGGGGGGG")
            result.append({
                "tokens":tokens,
                "sentence":sent["sentence"],
                "target_index":target_index,
            }) 
        data[word] = result
   
    with open("sentences_processed.json", 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

def display_sent(sent, target, another_word):
    ori = sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        "<strong>{}</strong>".format(sent["tokens"][sent["target_index"]][0])
    )
    new = sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        "<strong>{}</strong>".format(another_word)
    )
    return ori, new

def generate_template(template, **kwargs):
    for key, val in kwargs.items():
        template = template.replace("{}{}{}".format("{{", key, "}}"), str(val))
    return template

def generate_html():
    with open("wordset.json", 'r', encoding='utf-8') as infile:
        wordsets = json.load(infile)

    with open("sentences_processed.json", 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    with open("index.html", 'r', encoding='utf-8') as infile:
        template = infile.read()

    count = 0
    for w1, w2 in wordsets:
        # w1
        sent_list = data[w1]
        for sent in sent_list:
            ori, new = display_sent(sent, w1, w2) 
            with open("html/{:0>4}.html".format(count), 'w', encoding='utf-8') as outfile:
                #outfile.write(template.replace("{{s1}}", ori).replace("{{s2}}", new))
                outfile.write(generate_template(
                    template=template,
                    s1=ori, s2=new, w1=w1, w2=w2, w=w1, id=count,
                ))
            count += 1

        # w2
        sent_list = data[w2]
        for sent in sent_list:
            ori, new = display_sent(sent, w2, w1) 
            with open("html/{:0>4}.html".format(count), 'w', encoding='utf-8') as outfile:
                #outfile.write(template.replace("{{s1}}", ori).replace("{{s2}}", new))
                outfile.write(generate_template(
                    template=template,
                    s1=ori, s2=new, w1=w1, w2=w2, w=w2, id=count, 
                ))
            count += 1

    # update static
    os.system("cp static/* html/static/")

def main():
    #parsing()
    #preprocessing()
    generate_html()

if __name__ == "__main__":
    main()
