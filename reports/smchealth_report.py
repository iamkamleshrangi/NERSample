from pymongo import MongoClient
import getNames
import csv 

conn = MongoClient('127.0.0.1', 27017)
db = conn['in']
col = db['smchealth']

file_names = col.distinct('file_path')
csv_data = []
csv_header = ['domain', 'url', 'file_name', 'parsed_data', 'nlp_data', 'not_in_nlp', 'length']
csv_data.append(csv_header)
for file_path in file_names:
    #Domain => Parsed
    parsed_names = []
    for record in col.find({'file_path': file_path}):
        domain = record['domain']
        url = record['url']
        parsed_names.append(record['doctor_name'])
    parsed_names.sort()
    #GetByNLP 
    nlp_names = getNames.main(file_path)
    nlp_names.sort()
    if len(parsed_names) > len(nlp_names):
        not_in = list(set(parsed_names) - set(nlp_names))
    else:
        not_in = list(set(nlp_names) - set(parsed_names))

    parsed_data = '; '.join(parsed_names)
    nlp_data = '; '.join(nlp_names)
    not_in_data = '; '.join(not_in)
    length_data = len(not_in)
    csv_data.append([domain, url, file_path, parsed_data, nlp_data, not_in_data, length_data])

#Create CSV file
with open('smchealth.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csv_data)

