from net.cambridge import Cambridge
from net.dict_cn import DictCN
import PyQt5.Qt as qt
from gui.TTSWindow import TTSWindow

example_fields = ["meaning", "word", "mp3", "sentence"]
example_words = ["cat", "dog", "pig", "cook2", "chicken", "mdd3", "computer", "mom2", "happy"]

def callback_func(result1, result2, field_indexes):
  #print("callback")
  print(result1, result2)
  # print(field_indexes)
  for i in field_indexes:
    print(example_fields[i])

if __name__ == "__main__":
  app = qt.QApplication([])

  win = TTSWindow(fields = example_fields,
                  words = example_words,
                  service_audio=Cambridge(),
                  service_detail = DictCN(),
                  callback_func = callback_func)
  exit(app.exec())


