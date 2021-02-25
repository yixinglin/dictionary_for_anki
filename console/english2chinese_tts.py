import yaml
from tools.anki_tools import *
from net.cambridge import Cambridge
from net.dict_cn import DictCN
import os

Collection_PATH = "C:\\Users\\Yixing Lin\\AppData\\Roaming\\Anki2\\用户1\\collection.anki2"

def __write_content(note, field, value, overwrite):
    if overwrite == True:
        note[field] = value


def edit_note(note, result_detail, result_audio, cfg_fields,  overwrite = True, us_audio = False):
    # cfg_fields = {field_word,
    #               field_phonetic_uk,
    #               field_phonetic_us,
    #               field_sentence, field_meaning,
    #               field_audio}
    succ_detail = result_detail["succeed"]
    phonetic_uk = result_detail["phonetic_uk"]
    phonetic_us =  result_detail["phonetic_us"]
    sentence =  result_detail["sentence"]
    meaning =  result_detail["meaning"]

    if succ_detail == True:
        print("succ_detail")
        #note[cfg_fields[1]] = phonetic_uk
        #note[cfg_fields[2]] = phonetic_us
        #note[cfg_fields[3]] = sentence
        #note[cfg_fields[4]] = meaning
        __write_content(note, cfg_fields[1], phonetic_uk, overwrite)
        __write_content(note, cfg_fields[2], phonetic_us, overwrite)
        __write_content(note, cfg_fields[3], sentence, overwrite)
        __write_content(note, cfg_fields[4], meaning, overwrite)

    audio_uk =  result_audio["path_uk"]
    audio_us = result_audio["path_us"]
    succ_audio_uk = result_audio["succeed_uk"]
    succ_audio_us = result_audio["succeed_us"]
    if succ_audio_uk == True:
        print("succ_audio_uk")
        # note[cfg_fields[5]] = audio_uk
        __write_content(note, cfg_fields[5], audio_uk, overwrite)
        print(note[cfg_fields[5]])

    if succ_audio_us == True and us_audio == True:
        print("succ_audio_us")
        # note[cfg_fields[5]] = audio_us
        __write_content(note, cfg_fields[5], audio_us, overwrite)

    note.flush()

def test1():


    with open("english2chinese_tts_config.yaml", 'r', encoding="utf-8") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        print(cfg)

    deck_name = cfg["deck"]
    field_word = cfg["word"]
    field_phonetic_uk = cfg["target_fields"]["phonetic_uk"]
    field_phonetic_us = cfg["target_fields"]["phonetic_us"]
    field_sentence = cfg["target_fields"]["sentence"]
    field_meaning = cfg["target_fields"]["meaning"]
    field_audio = cfg["target_fields"]["audio"]
    us_audio_used = cfg["target_fields"]["us_audio_used"]
    overwrite = cfg["target_fields"]["overwrite"]
    cfg_fields = [field_word, field_phonetic_uk, field_phonetic_us, field_sentence, field_meaning, field_audio]

    col = Collection(Collection_PATH)   # 目录会改变到collection那里
    print(os.getcwd())
    # 获取卡片和笔记
    cids = find_cards_by_deckname(col, deck_name)
    notes = [get_note_by_cid(col, cid) for cid in cids]

    # 获取字段
    fields = get_fieldname_by_nid(col, notes[0].id)
    print("Field name: ", fields)
    print("Config: ", cfg_fields)
    issubset = set(cfg_fields).issubset(fields)
    print("这个是包含关系?", issubset)

    # 建立一个映射 word -> note
    word2note = dict()
    for note in notes:
        word = note[field_word]
        word2note[word] = note

    print("笔记数量", len(notes))
    # 下载音频和意思
    cambridge = Cambridge()
    dictcn = DictCN()

    for i, (w, n) in enumerate(word2note.items()):
        if i > 10:
            return

        result_audio = cambridge.run(w)
        result_detail = dictcn.run(w)
        percent = i * 100 // len(word2note)
        info = "{0}% [{1}/{2}] --> {3}".format(percent, i, len(word2note), w)
        print(info)

        # edit_note(n, result_detail, result_audio, cfg_fields, overwrite, us_audio_used)
        n["音标us"] = "6666"
        n.flush()
        print(n["音标us"], type(n))

    # print(notes)
    #col.close()

test1()