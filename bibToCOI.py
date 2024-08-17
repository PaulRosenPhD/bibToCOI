import bibtexparser
import os
import csv
from operator import itemgetter
import sys


def process_bib( input_bib, author_csv_data = {} ):
    
    with open(input_bib) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for entry in bib_database.entries:

        # entry['author'] = entry['author'].replace('\\\\','\\').replace('\\textbf{','').replace('}','')
        print( entry['ID'] + " -> " + entry['ENTRYTYPE'] )
        

        authors = bibtexparser.customization.author(entry)['author']
        for i, a in enumerate(authors):
            if ',' in a:
                last,first = a.split(", ")
            else:
                t = a.split(" ")
                last = t[-1]
                first = " ".join(t[:-1])

            name = last + ", " + first
            year = int(entry['year'])
            
            if name in author_csv_data and int(author_csv_data[name]['Year']) > year:
                continue

            author_csv = {}
            author_csv['Last'] = last
            author_csv['First'] = first
            author_csv['Year'] = int(entry['year'])
            author_csv_data[name] = (author_csv)
    
    return author_csv_data
            

def csv_to_dict(file_path):
    result_dict = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result_dict[row['Last'] + ", " + row['First']] = row
    return result_dict



if len(sys.argv) > 2:
    filter_year = int(sys.argv[1])
    input_file = sys.argv[2]
elif len(sys.argv) > 1:
    filter_year = 2020
    input_file = sys.argv[1]
else:
    print("Usage: python bibToCOI.py <year> <bibfile>")
    sys.exit(1)

fields = ['Last', 'First', 'Year']

author_csv_data = {}
if os.path.exists(input_file+".csv"):
    author_csv_data = csv_to_dict(input_file+".csv")

author_csv_data = process_bib(input_file, author_csv_data)
    
with open(input_file+".csv", 'w') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames = fields) 
    writer.writeheader() 
    list_of_authors = author_csv_data.values()
    list_of_authors = filter( lambda x: int(x['Year']) >= filter_year, list_of_authors )
    list_of_authors = sorted(list_of_authors, key=itemgetter('Last') )
    writer.writerows( list_of_authors ) 

