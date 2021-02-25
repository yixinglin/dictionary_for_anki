from . import service
from bs4 import BeautifulSoup
import traceback
import sys
BASE_URL = "http://dict.cn"
DEBUG_MSG = False

class DictCN(service.Service):

  def __init__(self, callback_func = None):
    super().__init__(callback_func)
    self.word = ""


  def parser(self, html):
    """
    HTML parser
    :param html: text of html
    :return:
        text of meanings
        text of examples
    """
    soup = BeautifulSoup(html, 'html.parser')

    try:
      mean = soup.find("ul", attrs={"class": "dict-basic-ul"})
      if mean is None:
        mean = soup.find("div", attrs={"class": "basic clearfix"})
      lis = mean.find_all("li")
      lis.pop()
      meaning = ""
      for li in lis:  # anki <br>换行
        if li.span != None and li.strong != None:
          if DEBUG_MSG:
            print(li.span.text,  # 词性
                  li.strong.text  # 词义
                  )
          meaning += li.span.text + li.strong.text + "\n"
    except:
      meaning = None

    try:
      example = ""
      sentence = soup.find("div", attrs={"class": "layout sort"})
      if sentence == None:
        sentence = soup.find("div", attrs={"class": "layout patt"})

      if sentence != None:
        lis = sentence.find_all("li")
        for i, li in enumerate(lis):
          if i < 3:
            if DEBUG_MSG:
              print(li.text)
            example += li.text + "\n"
    except:
      example = None

    try:
      sp = soup.find("div", class_ = "phonetic")
      phonetic = sp.find_all("bdo", lang = "EN-US")
      phonetic_uk = phonetic[0].text
      phonetic_us = phonetic[1].text
    except:
      phonetic_uk = None
      phonetic_us = None

    return meaning, example, phonetic_uk, phonetic_us


  def run(self, word, delay=5):

    # Download HTML file
    # e.g. url = "https://dictionary.cambridge.org/dictionary/english/dog"
    self.word = word
    url = "{0}/{1}".format(BASE_URL, word)
    print(url)
    filename = "{0}_{1}".format(word, "dictcn")
    print(filename)
    html_path = self.download_html(url, filename,
                                   delay=delay)
    html_text = ""
    with open(html_path, "r", encoding="utf-8") as f:
      for l in f.readlines():
        html_text += l

    meaning, example, phonetic_uk, phonetic_us = self.parser(html_text)

    succeed = meaning is not None and example is not None and phonetic_uk is not None and phonetic_us is not None

    result = {
      "word": word,
      "meaning": meaning,
      "sentence": example,
      "phonetic_uk": phonetic_uk,
      "phonetic_us": phonetic_us,
      "succeed": succeed
    }

    return result
