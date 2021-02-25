from net.config import *
import os
from net.cambridge import Cambridge
from net.dict_cn import DictCN
from threading import Thread
import winsound

print("current work path", os.getcwd())

class AudioThread(Thread):

    def __init__(self, words):
        super().__init__()
        self.words = words
        self.cambridge = Cambridge()

    def run(self) -> None:
        for i, w in enumerate(self.words):
            percent = (i + 1) * 100 // len(self.words)
            info = "Audio: {0}% [{1}/{2}] --> {3}".format(percent, i, len(self.words), w)
            result_cam = self.cambridge.run(w)
            print(info)


class DictThread(Thread):

    def __init__(self, words):
        super().__init__()
        self.words = words
        self.dict_cn = DictCN()

    def run(self) -> None:
        for i, w in enumerate(self.words):
            percent = (i + 1) * 100 // len(self.words)
            info = "Dict: {0}% [{1}/{2}] --> {3}".format(percent, i, len(self.words), w)
            result_dict = self.dict_cn.run(w)
            print(info)

# download a word to default folders
def download_one_word(word, show_info = False):
    # download audio from cambridge
    cambridge = Cambridge()
    result_cam = cambridge.run(word)

    # get meaning fron dict.cn
    dict_cn = DictCN()
    result_cn = dict_cn.run(word)
    print(result_cn)

    if show_info:
        for k, v in result_cam.items():
            print("->>", k, ":", v)
        for k, v in result_cn.items():
            print("->>", k, ":", v)


def get_word_list():
    list_word_html = os.listdir(HTML_PATH)
    words = list()
    for html in list_word_html:
        sp = html.split("_")
        words.append(sp[0])

    words = list(set(words))
    words.sort()
    print(words[0:50])
    return words


""" run program  """
try:
    words = get_word_list()
    for i, w in enumerate(words):
        if i < 0:  #4730
            continue
        percent = (i+1) * 100 // len(words)
        info = "{0}% [{1}/{2}] --> {3}".format(percent, i, len(words), w)
        download_one_word(w)
        print(info)
except:
    duration = 1000  # millisecond
    freq = 520  # Hz
    winsound.Beep(freq, duration)

"""    run threads     """
# words = get_word_list()
# #dict_t = DictThread(words).start()
# AudioThread(words).start()


""" Test one word if bug comes  """
# error: foregone, flexibly, evaporator, entrepreneurship, enervation
# elaborateness, edibility, echoic, adventurist, harshness, flexibly, asymmetrical, flexibly
# harshness, dazzling, entrepreneurship,inverted commas
# dazzling entrepreneurship, inverted commas, sightseer stunned superbly the tropics
# flexibly harshness spectacularly, spray gun, wipe off, wipe up

# download_one_word("asymmetrical", True)
# path = os.path.dirname(__file__)
# print(path)

#file = "D://anki/audio/woman_Cambridge_uk.mp3"
#print(os.path.access(file))

