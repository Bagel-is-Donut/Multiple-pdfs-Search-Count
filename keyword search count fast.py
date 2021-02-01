# inputs: a directory with pdfs: "folder_name", a txt of keywords: "keywords.txt"
# the txt of keywords should be separated by "\n" or "\t", depending on the words
# outputs: a txt with keywords matched with pdf names & occurrances counts
# README.txt

### packages
import os
import PyPDF2
import textract
import string
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

### files (CHANGE FILE PATHS HERE!!!)
directory = "/Users/yuewu/Desktop/paper testing"
scrapper_directory = "/Users/yuewu/Desktop/pdf scrapper/"
keywords_path = scrapper_directory + "keywords.txt"
output_file_path = scrapper_directory + "keywords search & count.txt"

### Inputs Helper
def init_keywords_dict(keywords_path):
    # open keywords_path txt
    # initiate an empty dictionary for keywords
    # dict = {"keyword1" : [],...}
    dict = {}
    f = open(keywords_path,"r")
    for line in f.readlines():
        temp = line.strip().split("\t")
        dict[temp[0]] = []
        if len(temp) != 1:
            vrnt = temp[1:]
            dict[temp[0]] += [len(vrnt)] + vrnt
        # e.g. {"FinTech" : [2,"fintech","Fintech"],...}
    return dict

### pdf keyword search & count
def variant(word):
    # to save run time, must input all lowercase, except for particular namings
    # e.g. imput key as "key" -> ["key","Key"]
    # for ordinary name (only one cap at the beginning), input as it is
    # particular names such as FinTech is not handled here, but in the func "keyword_search_count"
    if word.lower() == word:
        # print([word, string.capwords(word)])
        return [word, string.capwords(word)]
    else:            #string.capwords(word) == word, like "Alice"
        # print([word])
        return [word]

def searchInPDF(directory, pdf, variant_dict, keywords_dict):         # variant_dict
    print (pdf)
    path = directory + "/" + pdf
    # read pdf, turn into a string called "keywords"
    pdfFileObj = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count_page = 0
    text = ""
    while count_page < num_pages:
        pageObj = pdfReader.getPage(count_page)
        count_page +=1
        text += pageObj.extractText()
    if text != "":
       text = text
    else:
       text = textract.process(path, method='tesseract', language='eng')
    tokens = word_tokenize(text)
    punctuation = ['(',')',';',':','[',']',',']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and not word in punctuation]
    # word occurrance count
    word_occurrance_dict = {}
    for key in keywords_dict:
        word_occurrance_dict[key] = 0
    # update variant_dict
    for k in keywords:
        for key in variant_dict:
            if k in variant_dict[key]:
                word_occurrance_dict[key] += 1
    for key in word_occurrance_dict:
        keyword_occurrance = word_occurrance_dict[key]
        if word_occurrance_dict[key] != 0:
            keywords_dict[key].append([pdf,keyword_occurrance])
    return keywords_dict


def keyword_search_count(directory, pdf_files, keywords_dict):
    # returns dictionary {"keyword1" : [[filename = "", count = 0]],...}
    variant_dict = {}
    for word in keywords_dict:
        if keywords_dict[word] != []:       # word has hand-written variants
            if isinstance(keywords_dict[word][0], int) == True:
                num_variants = keywords_dict[word][0]
                variants = [word] + keywords_dict[word][1 : num_variants + 1]
                keywords_dict[word] = keywords_dict[word][num_variants + 1 : ]
        else:       # word has no hand-written variants
            variants = variant(word)
        variant_dict[word] = variants
    print (variant_dict)
    # {'economics': ['economics', 'Economics'], 'Crisis': ['Crisis'], 'fintech': ['fintech', 'Fintech', 'FinTech']}
    for pdf in pdf_files:
        path = directory + "/" + pdf
        keywords_dict = searchInPDF(directory, pdf, variant_dict, keywords_dict)
    #print(keywords_dict)
    return keywords_dict

def results(keywords_dict_complete, output_file_path):
    # record results into a txt file
    rslt = "word\tfile\tfrequency\n"
    for key in keywords_dict_complete:
        temp = key + "\t"
        files = keywords_dict_complete[key]
        if files != []:
            for f in files:
                rslt += temp + f[0] + "\t" + str(f[1]) + "\n"
    rslt.strip()
    with open(output_file_path, 'w') as f:
        f.write(rslt)


### Run code
# run time
start = time.time()
print("timer starts")
print ("PROCESSING ...........")

# the list of ".pdf" files in the (direct) directory
file_in_directory = os.listdir(directory)
pdf_files = [x for x in file_in_directory if x[-4:] == ".pdf"] # pdf names

# call Inputs Helper
keywords_dict = init_keywords_dict(keywords_path)
# print ("keywords dictionary: " + str(keywords_dict))

# call keyword_search_count, write results into a txt file
keywords_dict_complete = keyword_search_count(directory, pdf_files, keywords_dict)
results(keywords_dict_complete, output_file_path)

# run time
print ("DONE!")
end = time.time()
print ("timer ends:" + str(end - start) + "seconds")

