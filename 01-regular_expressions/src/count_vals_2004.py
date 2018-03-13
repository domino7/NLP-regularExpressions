import io
import re
import json
import os
from glob import glob

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
                    if '2004' in item['judgmentDate']:
                        text_content = item['textContent']
                        results.write(text_content)
                        results.write("\n")

jsons_dir_full = '../data/json/'
output_full = "../data/full-results/full-content2004.txt"
# getContent(jsons_dir_full, output_full)

def getValues(pattern, input_file):
    i = 0
    with io.open(input_file,'r') as text:
        for line in text:
            results = re.findall(pattern, line, re.MULTILINE)
            for result in results:
               i = i+1
    return i

pattern1 = r"(\d+)((?:\d|\.|,|\s)*)(?=(?:(?:\((?:.*?)\))?)(\s?)(?:zł|zl|pln|PLN))"
values_file = "../data/json-trial/values.txt"

output_full = "../data/full-results/full-content2004.txt"

num1 = getValues(pattern1, output_full)

# print(num)

full_results_shortcuts = "../data/full-results/full-values2015-shortcuts.txt"
pattern_all_shortcuts_zl = r"(\d+)((?:(?:\.|,)(?:\d+))?)(\s?)(tys|tyś|mln|mld)(?=(?:(?:\.?)(?:\s)(?:zł|zl|pln|PLN)))"
num2 = getValues(pattern_all_shortcuts_zl, output_full)


num = num1 + num2

print(num)