import requests      # Для запросов по API
import json          # Для обработки полученных результатов
import time          # Для задержки между запросами
import os            # Для работы с файлами
import re
import pandas as pd  # Для формирования датафрейма с результатами
from bs4 import BeautifulSoup
from razdel import tokenize, sentenize

from navec import Navec
import slovnet
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

# import spacy
import json
from pymorphy2 import MorphAnalyzer
from transliterate import translit, get_available_language_codes

from natasha import (
    Segmenter,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    MorphVocab,
    Doc
)

navec = Navec.load("navec_news_v1_1B_250K_300d_100q.tar")
syntax = slovnet.Syntax.load("slovnet_syntax_news_v1.tar")

syntax. navec(navec)

def seg_text(doc):
    if isinstance(doc, str):
        doc = {"text": doc}

    doc["tokens"] = []

    for sent in sentenize(doc["text"]):
        doc["tokens"].append([_.text for _ in tokenize(sent.text)])

    return doc

import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

nltk.download("stopwords")
analyzer = MorphAnalyzer()
stop_words = stopwords.words("russian")
pos = {'NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'PRTF', 'PRTS'}

# Загрузка модели языка
# nlp = spacy.load("en_core_web_sm")
pattern  = r'([A-ZА-Я][a-zа-яA-ZА-Я\s\/\,]+[\:|\?|\-])\ *\n'
pattern1 = r'(требован)|(хотели.+видеть)|(ждем.+от)|(ожидаем)|(ожидания.+от)|(ждем.+)|(стек.+)'
pattern2 = r'(знан.+)|(опыт.*)|(навык.+)|(уме.+)|(.+сть)|(образов.+)|(работ.+)|(владе.+)|(понима.+)|(принци.+)|(стек.+)'\
           r'|(.+ний)|(.+чие)|(фрейм.+)|(.+ом)|(человек.+)|(уров.+)|(лет)|(рекл.+)|(вакан.+)|(получ.+)|(пользовате.+)|'\
           r'(предостав.+)|(труд.+)|(услов.+)|(откл.+)|(час.+)|(чел)|(чу.+)|(федер.+)'
pattern3 = r'[^\w]([a-zа-яA-ZА-Я]+[^;]+)[^\n+]'
pattern4 = r"[\s\w\d]"
pattern5 = r"[\s\,\.\+\/]+"
pattern6 = r"[a-zA-Z\d\s]+"

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
# Выполняем сегментацию текста
segmenter = Segmenter()
morph = MorphAnalyzer()

def get_vacancy(query = 'ML'):
    params = {
        'text': query,         # Поиск текста
        # 'area': area,         # Поиск в зоне
        # 'page': page,         # Номер страницы
        'per_page': 100       # Кол-во вакансий на 1 странице
    }   
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = json.loads(req.content.decode())
    req.close()
    return data

def get_skills(vacancy):
    req = requests.get(vacancy['url'])
    data = json.loads(req.content.decode())
    req.close()
    result = []
    for i in data['key_skills']:
        result.append(i['name'])
    return result

def get_desc(vacancy):
    req = requests.get(vacancy['url'])
    data = json.loads(req.content.decode())
    req.close()
    soup = BeautifulSoup(data['description'], 'html.parser')

    # Извлекаем текст из HTML
    text = soup.get_text()
    return text

def get_requirements(vacancy):
    text1 = vacancy['snippet']['requirement']
    text2 = vacancy['snippet']['responsibility']
    pattern = r'( и т\.?\s?д\.?| и др\s?\.?|и\/или|или| и )'
    cleaned_text1 = re.sub(pattern, ' ', text1, flags=re.IGNORECASE)
    cleaned_text2 = re.sub(pattern, ' ', text2, flags=re.IGNORECASE)
    pattern = r'(\.\.\.\n\.\.\.)'
    cleaned_text1 = re.sub(pattern, ' ', cleaned_text1, flags=re.IGNORECASE)
    cleaned_text2 = re.sub(pattern, ' ', cleaned_text2, flags=re.IGNORECASE)
    pattern = r'([A-ZА-Я]([^\.]|(\. [a-zа-я]))+)\.?\ ?'
    cleaned_text1 = re.findall(pattern, cleaned_text1, flags=re.IGNORECASE)
    cleaned_text2 = re.findall(pattern, cleaned_text2, flags=re.IGNORECASE)
    return cleaned_text1 + cleaned_text2

def extract_candidates(doc: dict, stop_words: list = stop_words, pos: set = pos) -> dict:

    res = set()
    for sent in doc["tokens"]:
        for token in sent:
            if token in stop_words or token in res:
                continue

            parsed = analyzer.parse(token) [0]

            if parsed.tag.POS not in pos:
                continue

            res.add(token)
    doc["candidates"] = res
    return doc

def syntax_collocations(doc: dict, syntax: slovnet.api.Syntax = syntax) -> dict:
    syntax_colloc = []
    for sent in doc["tokens"]:

        syntax_markup = syntax(sent)
        sent_word_id = {}
        for token in syntax_markup. tokens:
            sent_word_id[token.id] = token.text
            
        for token in syntax_markup. tokens:
            if token.head_id!='@' and token.text in doc["candidates"]:
                try:
                    syntax_colloc.append(sent_word_id[token.head_id] + ' ' + token.text)
                except :
                    pass
    doc["collocations"] = set(syntax_colloc)

    return doc

def get_tags_vacancy(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    blocks = re.findall(pattern, text.replace('\\n', ' '), re.MULTILINE)
    blocks = [i.lower() for block in blocks for i in block.split('\n')]
    req = [block for block in blocks if re.search(pattern1, block)]
    sec = None
    blk = []
    if len(req):
        for s in req:
            for j in range(blocks.index(s) + 1, len(blocks)):
                if not re.search(pattern2, blocks[j]):
                    sec = blocks[j]
            tmp = text.lower().split(s)[1].strip().strip(':').strip()
            if sec:
                blk.append(tmp.split(sec)[0].strip().strip(':').strip())
                sec = None
            else:
                blk.append(tmp)
    else:
        blk = [text.lower().strip()]

    
    tags = []
    tags1 = []
    tags2 = []
    for block in blk:    
        res = [j.replace('\n', ' ').replace('\t', ' ').replace('/', ', ') for j in re.findall(pattern3, block)]
        for text in res:
            doc = Doc(text)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            doc.parse_syntax(syntax_parser)
            for token in doc.tokens:
                tag = "".join(re.findall(pattern4, token.text, re.MULTILINE))
                # tag = token.text
                if not re.search(pattern2, token.text) and len(tag) > 0:
                    if token.pos == 'NOUN':
                        tags1.append(token.text)
                        tags1.append(translit(token.text, 'ru', reversed=True))
                    elif token.pos == 'X':
                        tags.append(token.text)
                        tags.append(translit(token.text, 'ru'))

            for word in text.split():
                if re.search(pattern6, "".join(re.findall(pattern4, word, re.MULTILINE))):
                    tags.append("".join(re.findall(pattern4, word, re.MULTILINE)))
                    tags.append(translit("".join(re.findall(pattern4, word, re.MULTILINE)), 'ru'))


            doc1 = seg_text(text)
            doc1 = extract_candidates(doc1)
            doc1 = syntax_collocations(doc1)
            for tag in doc1["collocations"]:
                if not re.search(pattern2, tag):
                    clear_tag = " ".join([morph.normal_forms(token)[0] for token in tag.split()])
                    tags2.append(clear_tag)
                    if len(re.split(pattern5, clear_tag)):
                        for pod_tag in re.split(pattern5, clear_tag):
                            tags2.append(pod_tag)

    if len(tags) > 0:
        keywords = set(tags + tags2)
    else:
        keywords = set(tags1 + tags2)
    return keywords

def get_courses():
    url = 'https://gb.ru/courses/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [i.get('href') for i in soup.find_all('a', class_='card_full_link')]
    name = [i.span.text.strip().replace("\xa0", " ") for i in soup.find_all('div', class_='direction-card__title')]
    decription = [i.text.strip().replace("\xa0", " ") for i in soup.find_all('div', class_='direction-card__text')]
    term = [i.span.text.strip().replace("\xa0", " ") for i in soup.find_all('div', class_='direction-card__info-text ui-text-body--6')]
    courses = [(name[i], links[i], decription[i], term[i]) for i in range(len(links))]
    
    return courses

def course_parsing(url):
    pattr = "\((.+)\)"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    skils = set()
    for description in soup.find_all('div', class_="promo-tech__item gkb-promo__tag _large ui-text-body--5"):
        tmp = set(description.span.text.strip().lower().split('/'))
        for tag in tmp:
            if len(re.findall(pattr, tag)):
                tmp = tmp | set([i.strip() for j in re.findall(pattr, tag) for i in j.split('/')]) | \
                      set([i.strip() for j in re.split(pattr, tag) for i in j.split('/')])
        skils = skils | tmp
    
    ignore_skills = set(['и другие', ''])
    return skils - ignore_skills

course_skils = [(i[0], i[1], course_parsing(i[1]), i[2], i[3]) for i in get_courses()]

df_course_skils = pd.DataFrame(course_skils, columns=["name", "url", "tags", "description", "term"])
without_tags = df_course_skils[df_course_skils["tags"] == set()]

another_tags = []
with open("tags.txt") as file:
    s = file.read().replace("\n", "").split(";")
    #print(s)
    #print(len(s))
    for i in range(0, len(s), 2):
        url = s[i].strip()
        tags = s[i+1].strip().replace("{", "").replace("}", "").replace("'", "").split(",")
        for i, t in enumerate(tags):
            tags[i] = t.strip()

        another_tags.append((url, set(tags)))
df_another_tags = pd.DataFrame(another_tags, columns=["url", "tags"])

df_courses = pd.DataFrame(course_skils, columns=["name", "url", "tags", "description", "term"])
df_courses["id"] = df_courses.index

df_all_courses = pd.merge(df_courses,df_another_tags, on='url', how='left')
df_all_courses.loc[df_all_courses["tags_x"] == set(), "tags_x"] = df_all_courses.loc[df_all_courses["tags_y"] != set(), "tags_y"]
df_all_courses = df_all_courses.drop(columns=["tags_y"]).dropna()
df_all_courses = df_all_courses.rename(columns={"tags_x": "tags"})
drop_id = []
for i in df_all_courses.values:
    if i[3] == "":
        drop_id = i[5]
df_all_courses = df_all_courses.drop(drop_id)

all_tags = set()
for i in course_skils:
    all_tags = all_tags | i[2]

with open("new_tags.txt") as file:
    s = set(file.read().replace("{", "").replace("}", "").replace("'", "").split(","))
    all_tags = all_tags | s

def check(input_tags):
    # Находим курс, который покрыват больше всего

    courses = df_course_skils.copy(deep=True)
    courses["id"] = courses.index
    
    best_id = []
    coverage = []
    input_tags = set(input_tags) & set(all_tags)
    
    input_tags_len = len(input_tags)
    indexes = set(courses.index)

    courses["coverage"] = [0]*len(indexes)
    while len(input_tags)!=0 and len(best_id)<4:
        max_tags_len = -1
        max_tags_id = -1
        min_unnecessary_tags_len = -1

        for i in indexes:
            course = courses.loc[i]
            tags_len = len(input_tags & course[2])
            unnecessary_tags = len(course[2] - input_tags)
            if max_tags_len < tags_len or ((max_tags_len == tags_len) and (unnecessary_tags < min_unnecessary_tags_len)):
                max_tags_len = tags_len
                max_tags_id = i
                min_unnecessary_tags_len = unnecessary_tags
        best_id.append(max_tags_id)
        courses.loc[max_tags_id, "coverage"] = round(max_tags_len/input_tags_len*100)
    
        input_tags = input_tags - courses.loc[max_tags_id][2]
        indexes = indexes - set([max_tags_id])
    
    success = len(best_id) != 0

    if not success:
        best_id = [1, 2, 3, 4]

    ans = courses[courses.index.isin (best_id)]
    ans = ans.drop(columns=["id"])
    ans = ans.sort_values("coverage", ascending=False)
    output_json = json.dumps({"success":str(success), "courses": json.loads(ans.to_json())})
    return output_json

