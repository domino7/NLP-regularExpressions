import os
import io
import json
from glob import glob
import re


def getContent(jsons_dir, output_dir):
    pattern = os.path.join(jsons_dir, 'judgments*.json')
    with io.open(output_dir, 'w') as results:
        i = 0
        for file_name in glob(pattern):
            i = i+1
            if i%50 == 0:
                print("already done files: ", i)
            with open(file_name) as f:
                curr_json = json.load(f)
                items = curr_json['items']
                for item in items:
                    if '2015' in item['judgmentDate']:
                        text_content = item['textContent']
                        #to lower case
                        text_content = str.lower(text_content)
                        #remove html marks
                        text_content = re.sub('<[^>]*>', ' ', text_content)
                        #remove text dividing
                        text_content = re.sub('-[\s]*\n]', ' ', text_content)
                        #remove new lines
                        text_content = re.sub('\n', ' ', text_content)
                        #remove numbers
                        text_content = re.sub('[0-9]+', ' ', text_content)
                        #remove roman numerals
                        text_content = re.sub('[^\w](i|x|v|c|m|d|l)+[^\w]', ' ', text_content)
                        #remove single letters
                        text_content = re.sub('[^\w]\w[^\w]', ' ', text_content)
                        #remove all non letters
                        text_content = re.sub('[^\w]+', ' ', text_content)
                        text_content = re.sub('[^\w]\w[^\w]', ' ', text_content)
                        results.write(text_content)
                        results.write("\n")

# get text
jsons_dir_sample = '../../data/json-basic/'
output_sample = "../../data/json-basic/content2015_norm.txt"
# getContent(jsons_dir_sample, output_sample)

jsons_dir_full = '../../data/json/'
output_full = "../data/content2015_norm.txt"
# getContent(jsons_dir_full, output_full)


# get frequency list

def getFrequencyList(file_dir, results_file):
    wordcount = {}
    with open(file_dir) as infile:
        for line in infile:
            for word in line.split():
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

    wordcount_sorted_keys = sorted(wordcount, key=wordcount.get, reverse=True)
    with io.open(results_file, 'w') as results:
        for pos in wordcount_sorted_keys:
            results.write(pos+","+str(wordcount[pos])+"\n")


results_sample_dir = "../data/results2015_trial.csv"
# getFrequencyList(output_sample, results_sample_dir)

results_full_dir = "../data/results2015.csv"
# getFrequencyList(output_full, results_full_dir)

