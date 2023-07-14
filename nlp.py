import jisho_api.word;
import fugashi;
import json;
import threading;

import interface;

tagger = fugashi.Tagger('-Owakati');

def nlp_sentence(sentence):
    
    def parse_words():    
        for word in tagger(sentence):
            word = Word(word);
    
    words = threading.Thread(target=parse_words);
    words.start();

class Word:

    origin = "";
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
        
        self.origin = data.surface;
        self.reading = data.feature.kana;

        pos = data.pos.split(",");

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

            interface.my_gui.append_meaning(word=self);
        except:
            pass
        
        