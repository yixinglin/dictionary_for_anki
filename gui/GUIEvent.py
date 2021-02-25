from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import time
# from english_chinese_tts.gui.TTSWindow import TTSWindow
#import english_chinese_tts.gui.ErrorDisplayGUI as errgui
from .Signal import Signal

#import tempfile

def update_info_labels(mw, content):
  info_labels = [(mw.label_res_pho_uk, content["phonetic_uk"]),
                (mw.label_res_pho_us, content["phonetic_us"]),
                (mw.label_res_mean,   content["meaning"]),
                (mw.label_res_sentence, content["sentence"])]
  for box, text in info_labels:
    if text is not None:
      box.setText(text[0:16])

class PlayAudioThread(QtCore.QThread):

  def __init__(self, mw, accent = 'uk'):
    QtCore.QThread.__init__(self)
    self.mw = mw
    self.accent = accent
    self.result_audio = None
    self.result_detail = None

  def play_audio(self, audio_path):
    print(audio_path)
    content = QMediaContent(QtCore.QUrl.fromLocalFile(audio_path))
    player = QMediaPlayer()
    player.setMedia(content)
    player.play()
    time.sleep(2)

  def run(self):
    #tmpdir = tempfile.mkstemp()
    print("event_test_word_button")
    word = self.mw.lineedit_vocab.text()  # get word from LineEdit
    print("Start Test ", word)
    try:
      self.result_audio = self.mw.service_audio.run(word, delay = 0.2)  # get mp3 from web or local
      self.result_detail = self.mw.service_detail.run(word, delay = 0.2) # get detail from web or local

      # play vedio
      audio_path = self.result_audio["path_{0}".format(self.accent)]
      self.play_audio(audio_path)

      # now inform the main thread with the output
      self.mw.audio_trigger.emit(Signal.AUDIO_FINISHED)
      self.mw.audio_trigger.emit(Signal.UPDATE_INFO_LABELS)

    except:
      self.mw.audio_trigger.emit(Signal.AUDIO_FINISHED)

class DownloadThrad(QtCore.QThread):

  def __init__(self, mw, words, callback_func = None):
    QtCore.QThread.__init__(self)
    self.mw = mw
    self.words = words
    self.save_pause = 0  # index
    self.fail_cnt = 0
    self.fail_words = list()
    self.result_detail = None
    self.result_audio = None
    self.progress = list()
    self.callback_func = callback_func
    self.accent = 'uk'

  def run(self):
    print("thread_start_download")
    self.fail_words = list()
    self.mw.download_trigger.emit(Signal.DISABLE_COMBOBOXES)
    start = self.save_pause
    for i, w in enumerate(self.words):
      if i < start:
        continue
      self.save_pause = i

      self.result_detail = self.mw.service_detail.run(w, delay=0.2)  # get detail from web or local

      if self.result_detail["succeed"] == False:
        self.fail_cnt += 1
        self.fail_words.append(w)
        self.update_progress(i + 1, len(self.words), w, self.fail_cnt)
        self.mw.download_trigger.emit(Signal.UPDATE_PROGRESS_LABEL)
        self.mw.download_trigger.emit(Signal.UPDATE_FAIL_WORDS)
        continue

      self.result_audio = self.mw.service_audio.run(w, delay=5)  # get mp3 from web or local

      self.update_progress(i + 1, len(self.words), w, self.fail_cnt)
      self.mw.download_trigger.emit(Signal.UPDATE_INFO_LABELS)
      self.mw.download_trigger.emit(Signal.UPDATE_PROGRESS_LABEL)

      if self.callback_func is not None:
        self.callback_func(self.result_detail, self.result_audio, self.mw.field_indexes, self.accent)

    self.mw.download_trigger.emit(Signal.DOWNLOAD_FINSISHED)
    self.mw.download_trigger.emit(Signal.ENABLE_COMBOBOXES)
    self.save_pause = 0
    self.fail_cnt = 0

    self.mw.download_trigger.emit(Signal.UPDATE_FAIL_WORDS)

  def update_progress(self, count, total, word, fail_cnt):
    self.progress = [count, total, word, fail_cnt]

  def stop(self):

    self.mw.download_trigger.emit(Signal.DOWNLOAD_FINSISHED)
    self.mw.download_trigger.emit(Signal.ENABLE_COMBOBOXES)
    self.terminate()

    self.save_pause = 0
    self.fail_cnt = 0

  def pause(self):
    self.mw.download_trigger.emit(Signal.DOWNLOAD_FINSISHED)
    self.mw.download_trigger.emit(Signal.ENABLE_COMBOBOXES)
    self.terminate()

def event_start_download_button(mw, use_us_phonetic = False):
  btn = mw.btn_start
  btn.setEnabled(False)

  if use_us_phonetic:
    mw.download_thread.accent = 'us'
  else:
    mw.download_thread.accent = 'uk'

  mw.download_thread.start()

def event_stop_download_button(mw):
  mw.download_thread.stop()

def event_pause_download_button(mw):
  mw.download_thread.pause()

def event_test_word_button(mw, use_us_phonetic = False):
  btn = mw.btn_test
  btn.setText("Wait")
  btn.setEnabled(False)

  if use_us_phonetic:
    mw.play_audio_thread.accent = 'us'
  else:
    mw.play_audio_thread.accent = 'uk'

  mw.play_audio_thread.start()