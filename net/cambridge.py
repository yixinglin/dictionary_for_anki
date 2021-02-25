# Download audios from https://dictionary.cambridge.org
from . import service
from bs4 import BeautifulSoup
import traceback
import json
import os
DOWNLOAD_UK = True
DOWNLOAD_US = True

BASE_URL = "https://dictionary.cambridge.org"

class Cambridge(service.Service):

  def __init__(self, callback_func = None):
    super().__init__(callback_func)
    self.headers = self.__get_request_header()


  def parser(self, html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
      # Get mp3 url of uk pronunciation
      soup_uk = soup.find("span", attrs={"class", "uk dpron-i"})
      soup_uk = soup_uk.find("source", type="audio/mpeg")
      url_uk = BASE_URL + soup_uk["src"]
    except:
      url_uk = None

    #print("uk: ", url_uk)
    # Get mp3 url of us pronunciation
    try:
      soup_us = soup.find("span", attrs={"class", "us dpron-i"})
      soup_us = soup_us.find("source", type="audio/mpeg")
      url_us = BASE_URL + soup_us["src"]
    except:
      url_us = None
    #print("us: ", url_us)
    return url_uk, url_us

  def run(self, word, delay = 6):
    """
    Run the downloader
    :param word: The word to look up
    :return: result
    """
    # Download HTML file
    # e.g. url = "https://dictionary.cambridge.org/dictionary/english/dog"
    url = "{0}/dictionary/english/{1}".format(BASE_URL, word)
    filename = "{0}_{1}".format(word, "cambridge")
    html_path = self.download_html(url, filename,
                       headers = self.headers,
                       delay = delay/2)
    html_text = ""
    with open(html_path, "r", encoding="utf-8") as f:
      for l in f.readlines():
        html_text += l


    uk_pho_url, us_pho_url = self.parser(html_text)

    # Download MP3
    try:
      filename_uk = word + "_cambridge_uk"
      path_uk = self.download_media(uk_pho_url, filename_uk, headers = self.headers,
                            delay = delay/2, suffix="mp3")
    except:
      path_uk = None

    try:
      filename_us = word + "_cambridge_us"
      path_us = self.download_media(us_pho_url, filename_us, headers = self.headers,
                            delay = delay/2, suffix="mp3")
    except:
      path_us = None

    result = dict()
    result["path_uk"] = path_uk
    result["url_uk"] = uk_pho_url
    result["path_us"] = path_us
    result["url_us"] = us_pho_url
    result["succeed"] = path_uk is not None and path_us is not None
    result["succeed_uk"] = path_uk is not None
    result["succeed_us"] = path_us is not None

    if self.callback_func is not None:
      self.callback_func(result)

    return result

  def __get_request_header(self):
    path = os.path.dirname(__file__)
    with open(path + "/cambridge_header.json") as f:
      data = json.load(f)
    return data

