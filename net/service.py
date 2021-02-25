"""
父类：有三个方法需要被重写。
功能：下载html和媒体文件。


"""

import requests
from bs4 import BeautifulSoup
import time
from .config import *

DEBUG_MSG = True

class Service:

  def __init__(self, callback_func = None):
    self.html_dir = HTML_PATH
    self.audio_dir = AUDIO_PATH
    self.pic_dir = PIC_PATH
    for dir in [self.html_dir, self.audio_dir, self.pic_dir]:
      if not os.path.isdir(dir):
        os.makedirs(dir)

    self.callback_func = callback_func

  # Abstract method
  def modify(self, text: str):
    """ modify text  """
    raise NotImplemented

  # Abstract method
  def parser(self, html: str):
    """ parse html  """
    raise NotImplemented

  def valid_search(self, soup: BeautifulSoup):
    "Determine whether the searched word is valid"
    raise NotImplemented

  # abstract method
  def run(self, word: str):
    """
    Run the downloader
    :param word: The word to look up
    :return: result
    """
    raise NotImplemented

  def download_html(self, url: str, filename: str,
                    headers = None, delay = 5) -> str:
    """

    :param url: target url e.g. url = "https://dictionary.cambridge.org/dictionary/english/dog"
    :param filename: filename (without suffix) to store as file, e.g. filename = "person"
    :param headers: headers to request.
    :param delay: sleeping
    :return: the path where html was stored
    """
    path = "{0}/{1}.html".format(self.html_dir, filename)
    if os.path.isfile(path):
      #print("{0}.html exists!".format(filename))
      pass
    else:
      #print("Downloading {0}.html".format(filename))
      html = requests.get(url, headers=headers)
      time.sleep(delay)
      with open(path, "w", encoding='utf8') as f:
        f.write(html.text)
      #print("{0}.html downloaded".format(filename))

    return path

  def download_media(self, url: str, filename: str, dest_folder = AUDIO_PATH, suffix = "mp3",
                    headers = None, delay = 5) -> str:
    """
    Download media file
    :param url:  target url to download
    :param filename: filename (without suffix) to store as file, e.g. filename = "person"
    :param headers: headers to request.
    :param delay: sleeping
    :param suffix: suffix, e.g. mp3, svg, png.....
    :return: the path where html was stored
    """
    assert url is not None
    path = "{0}/{1}.{2}".format(dest_folder, filename, suffix)
    if os.path.isfile(path):
      #print("{0}.{1} exists!".format(filename, suffix))
      pass
    else:
      #print("Downloading {0}_{1}.html".format(filename, suffix))
      res = requests.get(url, headers=headers)
      time.sleep(delay)
      with open(path, "wb") as f:
        f.write(res.content)
      #print("{0}.html downloaded".format(filename))
    return path

