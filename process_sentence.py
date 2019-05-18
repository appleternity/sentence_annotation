import json
import csv
from pprint import pprint
from uuid import uuid4
import random

# from nltk.stem import WordNetLemmatizer
# from interface import tokenize_pos
# from nltk.tree import Tree

def parse_csv():
    with open("sentences.csv", 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        data = [row for row in reader]
        header = data[0]
        data = data[1:]
        data = [ 
            [
                {
                    "sentence": data[r][c].strip(),
                    "id": str(uuid4()),
                }
                for r in range(len(data))
            ]
            for c in range(0, len(data[0]))
        ]
        sentences = {
            h:d
            for h, d in zip(header, data)
        }
    
    wordsets = [(w1, w2) for w1, w2 in zip(header[0::2], header[1::2])]

    sentences = {
        "|".join(wordset) : {
            word : sentences[word]
            for word in wordset
        }
        for wordset in wordsets
    }

    with open("sentences.json", 'w', encoding='utf-8') as outfile:
        json.dump(sentences, outfile, indent=4)

def mix_tokenization():
    with open("sentences.json", 'r', encoding='utf-8') as infile:
        sentences = json.load(infile)
    
    with open("sentences_processed.json", 'r', encoding='utf-8') as infile:
        tokenization_info = json.load(infile)
        sentence_token_info = {}
        for key, val_list in tokenization_info.items():
            for token_info in val_list:
                sentence_token_info[token_info["sentence"].strip()] = {
                    "tokens":token_info["tokens"],
                    "target_index":token_info["target_index"]
                }

    for wordsets, sent_info_dict in sentences.items():
        for word in wordsets.split("|"):
            sent_info = sent_info_dict[word]
            sent_info = [
                {
                    "sentence":sent["sentence"],
                    "id":sent["id"],
                    "tokens":sentence_token_info[sent["sentence"]]["tokens"],
                    "target_index":sentence_token_info[sent["sentence"]]["target_index"]
                }
                for sent in sent_info
            ]
            sent_info_dict[word] = sent_info

    with open("sentences_all_info.json", 'w', encoding='utf-8') as outfile:
        json.dump(sentences, outfile, indent=4)

def display_sent(sent):
    return sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        '<span class="highlighted">{}</span>'.format(sent["tokens"][sent["target_index"]][0])
    )

def display_question(sent):
    return sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        '<span class="blank">{}</span>'.format("_______")
    )

def display_answer(sent):
    return sent["sentence"].replace(
        sent["tokens"][sent["target_index"]][0],
        '<span class="blank">{}</span>'.format("_______")
    )

def generate_html_sentence():
    with open("sentences_all_info.json", 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    wordset = "postpone|delay"    
    sentence_dict = data[wordset]
    results = []
    for word in wordset.split("|"):
        sentences = sentence_dict[word]
        for sent in sentences:
            results.append('<div class="not_selected sentence" id="{}">{}</div>'.format(
                sent["id"], display_sent(sent)
            ))
        results.append("\n")
    
    with open("sentences.txt", 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(results))

def generate_html_question():
    with open("sentences_all_info.json", 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    # print ("hello!")
    wordset = "destroy|spoil"
    sentence_dict = data[wordset]
    results = []
    for word in wordset.split("|"):
        sentences = sentence_dict[word]
        for sent in sentences:
            question = """<tr><td>{}</td><td><input type="radio" name="{}" value="{}" class="form-radio" /></td><td><input type="radio" name="{}" value="{}" class="form-radio" /></td></tr>""".format(
                display_question(sent), sent["id"], "destroy", sent["id"], "spoil"
            )
            results.append(question)
        # results.append("\n")
    
    random.shuffle(results)
    with open("questions.txt", 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(results))

def generate_html_answer():
    with open("sentences_all_info.json", 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    # print ("hello!")
    wordset = "destroy|spoil"
    sentence_dict = data[wordset]
    results = []
    for word in wordset.split("|"):
        sentences = sentence_dict[word]
        for sent in sentences:
            answer = """<div class="not_selected sentence" id="{}">{}</div>""".format(
                sent["id"],display_answer(sent)
            )
            results.append(answer)
        # results.append("\n")
    
    # random.shuffle(results)
    with open("destroy-spoil.txt", 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(results))    

def main():
    # parse_csv()
    # generate_html_sentence()
    # generate_html_question()
    generate_html_answer()
    # mix_tokenization()

if __name__ == "__main__":
    main()

