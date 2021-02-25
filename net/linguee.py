from net.service import Service
from bs4 import BeautifulSoup
import os, sys
# BASE_URL = "https://www.linguee.com/english-german/translation/person.html"
BASE_URL = "https://www.linguee.com"

class Linguee(Service):

    def __init__(self, callback_func=None):
        super().__init__(callback_func)
        self.word = ""


    def __parser_playsoud(self, text, opt = "EN_UK"):
        assert opt in text
        strings = text.split(",")
        for i, substr in enumerate(strings):
            if opt in substr:
                break
        url = strings[i].replace("\"", "")
        return url

    # Abstract method
    def parser(self, html: str):
        """ parse html  """

        soup = BeautifulSoup(html, 'html.parser')

        sp = soup.find("a", class_="audio")
        try:
            onclick = sp["onclick"]
            url = self.__parser_playsoud(onclick, opt = "EN_UK")
            url_uk = "{0}/mp3/{1}".format(BASE_URL, url)
        except AssertionError as ass_error:
            url_uk = None
            sys.stderr.write(repr(ass_error) + self.word)

        try:
            onclick = sp["onclick"]
            url = self.__parser_playsoud(onclick, opt = "EN_US")
            url_us = "{0}/mp3/{1}".format(BASE_URL, url)
        except AssertionError as ass_error:
            url_us = None
            sys.stderr.write(repr(ass_error) + self.word)

        return url_uk, url_us

    # abstract method
    def run(self, word: str):
        """
        Run the downloader
        :param word: The word to look up
        :return: result
        """
        self.word = word
        url = "{0}/english-german/translation/{1}.html".format(BASE_URL, word)
        filename = "{0}_{1}".format(word, "linguee")
        print(filename, url)
        html_path = self.download_html(url, filename)
        print(html_path)
        html_text = ""
        with open(html_path, "r", encoding="utf-8") as f:
            for l in f.readlines():
                html_text += l


        url_uk, url_us = self.parser(html_text)
        print(url_uk)
        print(url_us)

        return 0


if __name__ == "__main__":

    linguee = Linguee()
    # "going" "presumable"
    linguee.run("going")
