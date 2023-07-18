import json;

settings = {}
punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.．";

fonts = {
    "formal": "BIZ UDMincho Medium",
    "gothic": "Natsuzemi Maru Gothic Black",
    "handwriting": "left-handed_girlfriend"
}

def load_settings():
    global settings;

    f = open("./res/settings.json");
    settings = json.load(f);
    print(settings);

    f.close();

def get_font():
    global settings;
    return fonts[settings["font"]];