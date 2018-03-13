from elasticsearch import Elasticsearch

import json
import io
import os
from glob import glob

es = Elasticsearch()

INDEX = "judgements"
INDEX2 = "judgements6"

DOC_TYPE = "judgement"

# sample searching
# res = es.search(index=INDEX, body={"query":
#                                               { "query_string" :
#                                                     {"fields" : ["content"],
#                                                      "query" : "szukać"}
#                                                 }
#                                           })


test_content = {
    "content" : "telewizory i mecze z poziomu i porspektywy pythona",
    "date" : "2009-11-15",
    "judges" : ["judge2", "judge4"]
}


# sample data addition
# res = es.index(index=INDEX2, doc_type=DOC_TYPE, body=test_content)



def prepareJson(item):
    field_content = item['textContent']
    field_date = item['judgmentDate']
    field_judges = []
    for judge in item['judges']:
        field_judges.append(judge['name'])
    json_to_return = {
        "content": field_content,
        "date": field_date,
        "judges": field_judges
    }
    return json_to_return



def loadJsonsToES(jsons_dir):
    pattern = os.path.join(jsons_dir, 'judgments*.json')
    i = 0
    for file_name in glob(pattern):
        i = i+1
        if i%200 == 0:
            print("already done files: ", i)
        with open(file_name) as f:
            curr_json = json.load(f)
            items = curr_json['items']
            for item in items:
                if '2015' in item['judgmentDate']:
                    single_json = prepareJson(item)
                    es.index(index=INDEX2, doc_type=DOC_TYPE, body=single_json)


# loadJsonsToES
jsons_dir= '../data/json/'
loadJsonsToES(jsons_dir)








print("done")