import spacy
import re
from collections import Counter
from tqdm import tqdm

remove_words = ['about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'could', 'did', 'didn', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'how', 'if', 'in', 'into', 'is', 'isn', 'just', 'me', 'more', 'most', 'mustn', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'out', 'over', 'own', 'PRON', 'same', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with']

def clean(item):
    # if item.is_stop:
    #     return None
    lem_item = item.lemma_
    rep_item = re.sub("[^a-zA-Z]","", lem_item)
    if len(rep_item) < 2:
        return None
    # if rep_item in remove_words:
    #     return None
    return rep_item

def clean_entity(txt):
    txt = txt.replace("’s", '').replace('I.','').lower()
    txt = re.sub("[^a-zA-Z]","", txt)
    if len(txt) <2:
        return None
    return txt

def recog_sen(sentence):
    allowed_ents = ['PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT', 'WORK_OF_ART']
    tmp = []
    tx = ''
    for item in sentence:
        if item.ent_iob ==1 and item.ent_type_ in allowed_ents:
            tx += item.text
        elif item.ent_iob ==3 and item.ent_type_ in allowed_ents:
            if tx:
                clean_tx = clean_entity(tx)
                if clean_tx:
                    tmp.append(clean_tx)
            tx = item.text
        else:
            if tx:
                clean_tx = clean_entity(tx)
                if clean_tx:
                    tmp.append(clean_tx)
                tx = ''
            cleaned = clean(item)
            if cleaned:
                tmp.append(cleaned)
    return tmp



def process_chunk(chunk, nlp):
    doc = nlp(chunk)
    sent_array = []
    for sent in doc.sents:
        # *** Normal
        w_array = []
        for item in sent:
            cleaned = clean(item)
            if cleaned:
                w_array.append(cleaned)
        # *** End normal

        # *** with recognition
        # w_array = recog_sen(sent)
        # *** End with recoginition

        if len(w_array) > 1:
            sent_array.append(w_array)
    return sent_array


def tokenizex(text):
    nlp = spacy.load('en_core_web_sm')
    max_char_count = 999999
    chunks = [text[i:i+max_char_count] for i in range(0,len(text), max_char_count)]
    print('Total Chunks : {}'.format(len(chunks)))
    sentences = []
    pbar = tqdm(chunks)
    for chunk in pbar: sentences.extend(process_chunk(chunk, nlp))
    print('There are {} sentences'.format(len(sentences)))
    print('{} tokens found'.format(sum([len(sentence) for sentence in sentences])))
    print('There are {} unique words'.format(len(Counter([word for sent in sentences for word in sent]).keys())))
    return sentences
    