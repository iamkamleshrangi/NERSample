# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup, Comment
from nltk.tag.stanford import StanfordNERTagger
import os, re 
from nltk.corpus import stopwords
from nltk.corpus import names

#PreTrain DataSet of Standford
nlp_model = 'stanford-ner/english.all.3class.distsim.crf.ser.gz'
standford_jar = 'stanford-ner/stanford-ner.jar'
st = StanfordNERTagger( nlp_model, standford_jar, encoding='utf-8')

#Clean text for the process
def cleaner(raw_str):
    strng = ''
    if type(raw_str) != type(""):
        raw_str = raw_str.encode(encoding='UTF-8', errors='strict')
    raw_str = re.sub('[^a-zA-Z0-9-_*.]', ' ', raw_str)
    raw_str = re.sub('[ áá âââââââââââââ¯âãï»¿]+', ' ', raw_str)
    for word in raw_str.split(" "):
        strng += "%s " % (word.strip())
    return strng.strip()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#It can clean HTML, script tag and stop words as well
def basicClean(file_path):
    text = open( file_path, 'r').read() 
    soup = BeautifulSoup(text, 'html.parser')
    soup = soup.body
    [s.decompose() for s in soup('script')]
    [s.decompose() for s in soup('select')]
    selects = soup.findAll("style", {"type":"text/css"})
    for match in selects:
        match.decompose()
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    text = str(soup)
    text = re.sub("""</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>""",'\n', text)
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub('\n+','\n', text)
    return text

#Main function
def main(file_path):
    filtered = basicClean(file_path)

    removed = [ i.strip() for i in filtered.split('\n') if i and len(i.strip(' ')) > 1 ]
    filtered = list(set(removed))

    stop_words = set(stopwords.words('english'))
    stop_word = [ i.lower() for i in stop_words ]

    possible_names = [ i.strip() for i in removed if len(i) < 40 ]
    possible_names = [ i.strip() for i in possible_names if re.sub('\W+|\d+','', i)]
    possible_names = list(set(possible_names))

    word_token = [ w for w in possible_names if not w.lower() in stop_words and w[0].isupper() ]
    possible_names = [ i.strip() for i in possible_names if len(i.split(' ')) < 9 ] 
    possible_names  = [ i.replace('\u2004',' ') for i in possible_names ]
    
    possibles = [ re.sub('\W+|\s+',' ', i) for i in possible_names ]
    raw_string = '. '.join(possibles)

    raw_tag = word_tokenize(raw_string)
    records = st.tag(raw_tag)
    found_names = [ other[0] for other in records if other[1] == 'PERSON'  and len(re.sub('\W+','',other[0])) > 2]
    found_names = list(set(found_names))
    found_names.sort()

    keywords = [ key for key in found_names]
    keywords = '\s{1,}|'.join(keywords)
    check_name = re.compile(keywords)

    #Collect All Possible Names
    p_name = []
    for name in possible_names:
        if check_name.search(name) and hasNumbers(name) == False:
            p_name.append(name)
    return p_name
