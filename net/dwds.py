from net.service import Service
from bs4 import BeautifulSoup
import sys
from net.tools.dwds_grammar import grammar_noun, grammar_verb, grammar_adjektiv
import traceback

import win32com.client

BASE_URL = "https://www.dwds.de"
class DWDS(Service):

    def __init__(self, callback_func = None):
        super().__init__(callback_func)
        self.word = ""

    # Abstract method
    def parser(self, html: str):
        """ parse html
            找不到对应字段就填入None
         """
        soup = BeautifulSoup(html, 'html.parser')

        # Get audio link
        try:
            sp_aud = soup.find("source", type = "audio/mpeg")  # 可能会有多个发音
            audio_url = "https:" + sp_aud['src']
        except Exception as e:
            sys.stderr.write(repr(e) + "audio " + self.word + "\n")
            audio_url = None
        #print(audio_url)

        # Get tendency, img ab 1946
        try:
            #sp = soup.find("div", attrs={"class": "tab-pane", "id": "plot-2"})
            sp = soup.find("img", alt = "Wortverlaufskurve ab 1946")
            img_url = sp["src"]
        except Exception as e:
            sys.stderr.write(repr(e) + "img_url " + self.word + "\n")
            img_url = None

        #print(img_url)

        # Get phonetic
        try:
            sp = soup.find("span", class_ = "dwdswb-ipa")
            phonetic = sp.text
        except Exception as e:
            sys.stderr.write(repr(e) + "phonetic " + self.word + "\n")
            phonetic = None
        #print(phonetic)

        # Get freqency
        try:
            freq = self.__get_frequency(soup)
        except Exception as e:
            sys.stderr.write(repr(e) + "frequency " + self.word + "\n")
            freq = None
        #print(freq)

        # Get grammar, and type
        try:
            sp = soup.find("span", class_ =  "dwdswb-ft-blocktext")
            grammar, content = self.__grammar_parser(sp)
            type = grammar["type"]
        except Exception as e:
            sys.stderr.write(repr(e) + "grammar " + self.word + "\n")
            content = None
            type = None
        #print(type, "\n", content)

        # Get article
        try:
            if type == "noun":
                sp = soup.find("div", class_ = "dwdswb-ft")
                sp = sp.find("h1", class_ = "dwdswb-ft-lemmaansatz")
                article = sp.text[-3:]
            else:
                article = None
        except Exception as e:
            sys.stderr.write(repr(e) + "article " + self.word + "\n")
            article = None

        #print(article)

        # Get sentence
        try:
            sp = soup.find("div", class_ = "dwds-gb-list")
            sp_all = sp.find_all("div", class_="sans")
            sentences = ""
            for i, s in enumerate(sp_all):
                if i < 5:
                    sentences += "{0}. {1}\n".format(i+1, s.text)
        except Exception as e:
            sys.stderr.write(repr(e) + "sentences " + self.word + "\n")
            sentences = None

       # print(sentences)

        result = {
            "sentences": sentences,
            "audio_url": audio_url,
            "img_url": img_url,
            "phonetic": phonetic,
            "frequency":  freq,
            "type":  type,
            "article": article,
            "grammar": content,
            "succeed": self.valid_search(soup)
        }

        return result

    def valid_search(self, soup):
        valid = True
        try:
            content = soup.find("p", class_="bg-danger").text
            valid = "Kein Eintrag zu" not in content
        except:
            pass
        return valid

    # abstract method
    def run(self, word: str, delay = 12):
        """
        Run the downloader
        :param word: The word to look up
        :return: result
        """
        self.word = word
        html_url = "{0}/wb/{1}".format(BASE_URL, word)
        print(html_url)
        filename = "{0}_{1}".format(word, "dwds")
        print(filename)
        html_path = self.download_html(html_url, filename, delay = delay/3)
        print(html_path)

        html_text = ""
        with open(html_path, "r", encoding="utf-8") as f:
            for l in f.readlines():
                html_text += l

        result = self.parser(html_text)

        # download media
        try:
            path_audio = self.download_media(result["audio_url"], filename, dest_folder = self.audio_dir,
                                          delay=delay/3, suffix="mp3")
        except:
            path_audio = None

        try:
            path_img = self.download_media(result["img_url"], filename, dest_folder = self.pic_dir,
                                          delay=delay/3, suffix="svg")
        except:
            path_img = None

        # result = {
        #     "sentences": sentences,
        #     "audio_url": audio_url,
        #     "img_url": img_url,
        #     "phonetic": phonetic,
        #     "frequency":  freq,
        #     "type":  type,
        #     "article": article,
        #     "grammar": content,
        #     "succeed": self.valid_search(soup)
        # }

        result["path_audio"] = path_audio
        result["succeed_audio"] = path_audio is not None
        result["path_img"] = path_img
        result["succeed_img"] = path_img is not None

        if self.callback_func is not None:
            self.callback_func(result)

        return result

    """    Other function     """

    def __get_frequency(self, soup):

        sp = soup.find_all("td", style = "text-align:center")
        freq = 0
        for t in sp:
            div = t.find("div")
            if "background" in div["style"]:
                freq += 1
        return freq

    def __grammar_parser(self, soup):
        # adj, verb, noun
        sp = soup.find("span")
        word_class = sp.text # Adjektiv; Verb; Substantiv (Maskulinum); Substantiv (Neutrum); Substantiv (Femininum)

        if "Substantiv" in word_class:
            grammar, content = grammar_noun(soup)
        elif "Verb" in word_class:
            grammar, content = grammar_verb(soup)
        elif "Adjektiv" in word_class:
            grammar, content = grammar_adjektiv(soup)
        else:
            content = None
            grammar = None

        return grammar, content

if __name__ == "__main__":

    dwds = DWDS()
    # Hund, Obst, bringen
    # words1 = ["Hund", "Obst", "wasser"]
    # words2 = ["geben", "bringen", "liegen", "fliegen"]
    # words3 = ["rot", "fertig", "hoch", "rosa", "lila", "Stift", "LL"] zerstören, Topfschwamm
    result = dwds.run("rot")
    for k, v in result.items():
        print("{0}: {1}".format(k, v))


    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak("Jumpman Jumpman Jumpman Them boys up to something!")