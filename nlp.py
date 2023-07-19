import jisho_api.word, jisho_api.sentence;
import sudachipy;

import requests;
from bs4 import BeautifulSoup;

import json;
import utils;
import re;

#import gui.interface as interface;

tokenizer = sudachipy.Dictionary().create();
mode = sudachipy.Tokenizer.SplitMode.A;

cached_sentence = [];

def nlp_sentence(sentence, callback=None):
    global cached_sentence;

    cached_sentence = [m for m in tokenizer.tokenize(sentence, mode=mode)];
    for word in cached_sentence:
        word = Word(word);
        if(callback != None): callback(word);

def tokenize(sentence: str):
    '''Tokenize sentence into words'''
    global cached_sentence;

    sentence = re.sub(r"[%s]+" %utils.punc, "", sentence);
    print(sentence);

    cached_sentence = [m for m in tokenizer.tokenize(sentence, mode=mode)];
    return [m.surface() for m in tokenizer.tokenize(sentence, mode=mode)];

def get_example_sentences(word):

    # Get e4xamples from site, api not working
    url = "https://jisho.org/search/"+word+"%23sentences"
    response = requests.get(url).text;
    soup = BeautifulSoup(response, 'html.parser');

    found = soup.find("span", attrs={'class': 'furigana'});
    if found: found.decompose();

    contents = soup.find_all("div", attrs={'class': 'sentence_content'});

    return_obj = [];
    for sentence in contents[:5]:

        parsed = [line for line in sentence.text.split("\n") if line.strip() != ""];
        return_obj.append({
            "japanese": parsed[0],
            "en_translation": parsed[1]
        });

    return return_obj;

def find_word_meaning(word: str):
    '''Find the word's meaning using jisho web scrapping api'''
    if len(cached_sentence) == 0: return None;

    match_word = [match for match in cached_sentence if match.surface() == word][0];
    my_word: Word = Word(match_word);

    return my_word if my_word.meaning else None;

class Word:

    origin = "";
    dictform = "";
    reading = "";
    grammar = "";
    wtype = "";
    details = "";

    meaning = False;

    jlpt = [];
    common = False;
    senses = [];
    tags = [];

    def __init__(self, data):
        
        self.origin = data.surface();
        self.dictform = data.dictionary_form();
        self.reading = data.reading_form();

        pos = data.part_of_speech();

        self.grammar = pos[0] if pos[0] != "*" else None;
        
        self.wtype = pos[2] if pos[2] != "*" else None;
        self.details = pos[3] if pos[3] != "*" else None;
    
        if(pos[1] != "*"): self.fetch_meaning();

    def fetch_meaning(self):

        try:            

            self.meaning = True;
            data = jisho_api.word.Word.request(self.origin).json();
            data = json.loads(data)["data"][0];

            self.jlpt = data["jlpt"];
            self.common = data["is_common"];
            self.senses = data["senses"];
            self.tags = data["tags"];

            #interface.my_gui.append_meaning(word=self);
        except:
            pass;        