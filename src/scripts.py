import json
import os.path
from glob import glob

import os
import re
import io



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
                        results.write(text_content)
                        results.write("\n")

# get text
jsons_dir_sample = '../data/json-trial/'
output_sample = "../data/json-trial/content2015.txt"
# getContent(jsons_dir_sample, output_sample)


jsons_dir_full = '../data/json/'
output_full = "../data/full-results/full-content2015.txt"
# getContent(jsons_dir_full, output_full)


# get monetary value

def getValues(pattern, input_file, output_file):
    with io.open(output_file, 'w') as values:
        with io.open(input_file,'r') as text:
            for line in text:
                results = re.findall(pattern, line, re.MULTILINE)
                for result in results:
                    # print(result)
                    str_res = "".join(result).replace(" ", "") + ";"
                    values.write(str_res)

pattern1 = r"(\d+)((?:\d|\.|,|\s)*)(?=(?:(?:\((?:.*?)\))?)(\s?)(?:zł|zl))"
values_file = "../data/json-trial/values.txt"
# getValues(pattern, output_sample, values_file)

output_full_values = "../data/full-results/full-values2015.txt"
# getValues(pattern1, output_full, output_full_values)


# ALL monetary values in format digit (...) zl/zł
pattern_all_digits_zl = r"\d+.{0,20}(?=(?:zl|zł)(?:\s))"
# getValues(pattern_all_digits_zl, output_sample, "../data/full-results/TEST-sample-values2015.txt")


# ALL monetary values with tys/tyś/mln/mld
full_results_shortcuts = "../data/full-results/full-values2015-shortcuts.txt"
pattern_all_shortcuts_zl = r"(\d+)((?:(?:\.|,)(?:\d+))?)(\s?)(tys|tyś|mln|mld)(?=(?:(?:\.?)(?:\s)(?:zł|zl)))"
# getValues(pattern_all_shortcuts_zl, output_full, full_results_shortcuts)


# normalization
def normalizeNumbers(input_file, output_file):
    with io.open(input_file, "r") as input:
        with io.open(output_file, "w") as output:
            for line in input:
                new_line = line.replace(".", "").replace(",", ".")
                output.write(new_line)

values_file_norm = "../data/json-trial/values-norm.txt"
# normalizeNumbers(values_file, values_file_norm)

# normalize numbers
output_full_values_norm = "../data/full-results/norm-full-values2015.txt"
# normalizeNumbers(output_full_values, output_full_values_norm)


def reduceDotsAndSpaces(input_file, output_file):
    with io.open(input_file, "r") as input:
        with io.open(output_file, "w") as output:
            for line in input:
                values = line.split(";")
                for value in values:
                    new_value_dots = re.sub('\.(?=(?:(?:\d*)(?:\.)))', '', value)
                    new_value = re.sub('\s', '', new_value_dots)
                    output.write(new_value)
                    output.write(";")

output_full_values_norm = "../data/full-results/norm-full-values2015.txt"
output_full_values_norm_reduced = "../data/full-results/norm-full-values2015-reduced.txt"
reduceDotsAndSpaces(output_full_values_norm, output_full_values_norm_reduced)

# normalize numbers with shortcuts
def normalizeShortcuts(input_file, output_file):
    with io.open(input_file, "r") as input:
        with io.open(output_file, "w") as output:
            for line in input:
                new_line = line.replace(",", ".")
                values = new_line.split(";")
                for value in values:
                    dec = value[:-3]
                    shortcut = value[-3:]
                    if shortcut == "mld":
                        multiplier = 10e9
                    elif shortcut == "mln":
                        multiplier = 10e6
                    else:
                        multiplier = 10e3
                    try:
                        real_val = float(dec) * multiplier
                        output.write(str(real_val))
                        output.write(";")
                    except ValueError:
                        print("Could not multiply: ", dec, multiplier)

norm_full_results_shortcuts = "../data/full-results/norm-full-values2015-shortcuts.txt"
# normalizeShortcuts(full_results_shortcuts, norm_full_results_shortcuts)


# read values from 2 files
def getAllValues(values_files):
    i = 0
    final_values = []
    for file in values_files:
        with io.open(file, "r") as datafile:
            for line in datafile:
                values = line.split(";")
                for value in values:
                    try:
                        float_val = float(value)
                        final_values.append(float_val)
                    except ValueError:
                        i = i+1
                        print("Could not convert to float: ", value)
            print("Couldn't convert to float: ", i)
            return final_values

values_files = [output_full_values_norm, norm_full_results_shortcuts]
# all_values = getAllValues()



#histograms
import matplotlib.pyplot as plt
import numpy as np

def plotHistogram(values, range, bins):
    events, edges, patches = plt.hist(values, range=range, bins=bins, log=True)
    print(events)
    print(edges)
    print(patches)

    plt.xlabel('Cash values')
    plt.ylabel('number of occurrences')
    plt.title('Cash values in judgments for year 2015')

    plt.show(block=True)
    plt.interactive(False)

# plotHistogram(all_values, (1e6, 1e9), 20)

# TASK 3 - article 445

def articleMentionedInRegulations(regulations):
    for reg in regulations:
        if reg['journalNo'] == 16 and reg['journalYear'] == 1964 and reg['journalEntry'] == 93 and "445" in reg['text']:
            return True
    return False;

def getJudgmentsNumByArticle(jsons_dir, output_dir):
    pattern = os.path.join(jsons_dir, 'judgments*.json')
    with io.open(output_dir, 'w') as results:
        i = 0
        articles_num = 0
        for file_name in glob(pattern):
            i = i+1
            if i%50 == 0:
                print("already done files: ", i)
            with open(file_name) as f:
                curr_json = json.load(f)
                items = curr_json['items']
                # print(items)
                for item in items:
                    if '2015' in item['judgmentDate']:
                        regulations = item['referencedRegulations']
                        if articleMentionedInRegulations(regulations):
                            articles_num = articles_num + 1
    return articles_num


# articles_num = getJudgmentsNumByArticle(jsons_dir_full, "../data/json-trial/article-results.txt")
# print("articles_num: ", articles_num)
#articles_num:  2560


#TASK 4 - SZKODA

def contentContainsWord(text_content):
    regex = r"[^a-zA-Z](szkod[a|y|zie|ę|o|om|ami|ach]|szkód)[^a-zA-Z]"
    return bool(re.search(regex, text_content))



def getJudgmentsNumByWord(jsons_dir, output_dir):
    pattern = os.path.join(jsons_dir, 'judgments*.json')
    with io.open(output_dir, 'w') as results:
        i = 0
        articles_num = 0
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
                        if contentContainsWord(text_content):
                            articles_num = articles_num + 1
    return articles_num


# matchingJudgments = getJudgmentsNumByWord(jsons_dir_full, "../data/json-trial/article-results.txt")
# print("Judgements from 2015 containing word: ", matchingJudgments)
# Judgements from 2015 containing word:  17767

print("DONE")