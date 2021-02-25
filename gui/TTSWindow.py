from PyQt5.Qt import QPushButton, QLabel, QLineEdit, QComboBox
import PyQt5.Qt as qt
from .GUIEvent import *
from .Signal import Signal

WIN_WIDTH = 500
WIN_HEIGHT = 500

class TTSWindow(qt.QDialog):

  audio_trigger = qt.pyqtSignal(int)
  download_trigger = qt.pyqtSignal(int)

  def __init__(self, fields = None, words = None,
               service_audio = None, service_detail = None,
               callback_func = None):
    """

    :param fields: field names
    """
    super().__init__()
    self.fields = [None] + fields
    self.words = words # a list of words
    self.service_audio = service_audio
    self.service_detail = service_detail
    self.callback_func = callback_func
    self.field_indexes = list()

    self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
    self.setWindowTitle('English Vocabulary TTS')
    self.setMinimumWidth(WIN_WIDTH)
    self.setMinimumHeight(WIN_HEIGHT)

    self.initUI()
    self.initThreads()

    self.show()

  def initUI(self):
    vertical_position = 0
    # Font
    font1 = qt.QFont('Arial', 12, qt.QFont.Bold)  # used for field names
    font2 = qt.QFont('Arial', 30, qt.QFont.Bold)  # used for field names

    # Create labels
    self.label_pho_uk = QLabel(self)
    self.label_pho_uk.setText("英标")
    #l = "<a href=\"http://example.com/\">Click Here!</a>"
    self.label_pho_uk.setOpenExternalLinks(True)
    self.label_pho_us = QLabel(self)
    self.label_pho_us.setText("美标")
    self.label_mean = QLabel(self)
    self.label_mean.setText("释义")
    self.label_sentence = QLabel(self)
    self.label_sentence.setText("例句")
    self.label_audio = QLabel(self)
    self.label_audio.setText("音频")
    left = 50
    labels = [self.label_pho_uk, self.label_pho_us, self.label_sentence, self.label_mean, self.label_audio]
    for i, lab in enumerate(labels):
      vertical_position = 80+50*i
      lab.setGeometry(left, vertical_position, 50, 50)
      lab.setFont(font1)

    # Create comboboxes for fields
    left = 150
    self.__create_label("目标字段", (left, 20, 100, 50))
    self.comb_pho_uk = QComboBox(self)
    self.comb_pho_us = QComboBox(self)
    self.comb_sentence = QComboBox(self)
    self.comb_mean = QComboBox(self)
    self.comb_audio = QComboBox(self)

    comboboxes = [self.comb_pho_uk, self.comb_pho_us, self.comb_sentence, self.comb_mean, self.comb_audio]
    for i, com in enumerate(comboboxes):
      vertical_position = 90+50*i
      com.setGeometry(left, vertical_position, 100, 30)
      com.addItems(self.fields)
      # com.currentIndexChanged.connect(lambda: self.onComboboxInxChanged(com))
      com.currentIndexChanged.connect(self.onComboboxInxChanged)
      com.setCurrentIndex(i%(len(self.fields)-1) + 1)

    self.__update_field_indexes()

    # Create LineEdit
    left = 50
    vertical_position += 60
    #self.__create_label("单词测试", (left, vertical_position, 100, 50))
    self.lineedit_vocab = QLineEdit(self)
    self.lineedit_vocab.setGeometry(left, vertical_position, 200, 30)
    self.lineedit_vocab.setPlaceholderText("请输入一个单词进行测试")

    self.btn_test = QPushButton(self)
    self.btn_test_content = "测试"
    self.btn_test.setText(self.btn_test_content)
    self.btn_test.setGeometry(left+220, vertical_position, 80, 30)
    self.btn_test.clicked.connect(self.onButtonClicked)

    self.check_box_phonetic = qt.QCheckBox(self)
    self.check_box_phonetic.setText("美式发音")
    self.check_box_phonetic.setGeometry(left+220, 390-70, 100, 20)

    # Create result labels
    left = 260
    self.__create_label("结果", (left, 20, 50, 50))
    self.label_res_pho_uk = QLabel(self)
    self.label_res_pho_uk.setText("")
    self.label_res_pho_us = QLabel(self)
    self.label_res_pho_us.setText("")
    self.label_res_mean = QLabel(self)
    self.label_res_mean.setText("")
    self.label_res_sentence = QLabel(self)
    self.label_res_sentence.setText("")
    labels = [self.label_res_pho_uk, self.label_res_pho_us, self.label_res_sentence,
              self.label_res_mean]
    for i, lab in enumerate(labels):
      vertical_position = 80+50*i
      lab.setGeometry(left, vertical_position, 100, 50)
      #lab.setFont(font1)

    # create buttons
    left = 380
    vertical_position = 25
    self.btn_start = QPushButton(self)
    self.btn_start.setText("Start")
    self.btn_stop = QPushButton(self)
    self.btn_stop.setText("Stop")
    self.btn_pause = QPushButton(self)
    self.btn_pause.setText("Pause")
    btns = [self.btn_start, self.btn_pause, self.btn_stop]
    for i, b in enumerate(btns):
      b.setFont(font1)
      b.setGeometry(left, vertical_position+i*70, 100, 40)
      b.clicked.connect(self.onButtonClicked)

    self.textedit = qt.QTextEdit(self)
    self.textedit.setGeometry(left, 230,100,150)
    self.textedit.setText("")

    # Information Label
    self.label_info = self.__create_label("No infos", (10, self.height()-40, 400, 30))
    self.lable_word = self.__create_label("", (40, 400, self.width()*0.8, 50))
    self.lable_word.setFont(font2)
    self.lable_word.setAlignment(QtCore.Qt.AlignHCenter)


  """   EVENTS    """
  def onComboboxInxChanged(self):
    self.__update_field_indexes()


  def onButtonClicked(self):
    btn = self.sender()
    if btn is self.btn_test:
      us_pho = self.check_box_phonetic.isChecked()
      event_test_word_button(self, us_pho)
    elif btn is self.btn_start:
      us_pho = self.check_box_phonetic.isChecked()
      event_start_download_button(self, us_pho)
    elif btn is self.btn_stop:
      event_stop_download_button(self)
    elif btn is self.btn_pause:
      event_pause_download_button(self)

    print(btn.text())

  """   Threads  and Signals  """
  def initThreads(self):
    self.play_audio_thread = PlayAudioThread(self)
    self.download_thread = DownloadThrad(self, self.words, callback_func=self.callback_func)
    self.audio_trigger.connect(self.audio_trigger_handle)
    self.download_trigger.connect(self.download_trigger_handle)

  def audio_trigger_handle(self, val):
    # Signal.ENABLE_BUTTON_START
    #print("Signal from Audio")
    if val == Signal.AUDIO_FINISHED:
      self.btn_test.setText(self.btn_test_content)
      self.btn_test.setEnabled(True)
      result = self.play_audio_thread.result_audio
      url_text = "UK: \n{0}\nUS:\n{1}".format(result["url_uk"], result["url_us"])
      self.textedit.setText(url_text)

    if val == Signal.UPDATE_INFO_LABELS:
      update_info_labels(self, self.play_audio_thread.result_detail)

  def download_trigger_handle(self, val):
    # print("download_triggerhandle", val)
    #print("Signal from Download")
    if val == Signal.ENABLE_COMBOBOXES:
      self.__enable_comboboxes(True)
    if val == Signal.DISABLE_COMBOBOXES:
      self.__enable_comboboxes(False)
    if val == Signal.UPDATE_PROGRESS_LABEL:
      self.__update_progress_label()
    if val == Signal.UPDATE_INFO_LABELS:
      update_info_labels(self, self.download_thread.result_detail)
    if val == Signal.UPDATE_FAIL_WORDS:
      self.__update_text_edit(self.download_thread.fail_words)
    if val == Signal.DOWNLOAD_FINSISHED:
      self.btn_start.setEnabled(True)

  """  OTHERS   """
  def __create_label(self, text, geom):
    """ Fast Create a Label"""
    label = QLabel(self)
    label.setText(text)
    label.setGeometry(geom[0], geom[1], geom[2], geom[3])
    return label

  def __enable_comboboxes(self, enable):
    comboboxes = [self.comb_pho_uk, self.comb_pho_us,
                  self.comb_mean, self.comb_sentence, self.comb_audio]
    for cb in comboboxes:
      cb.setEnabled(enable)

  def __update_progress_label(self):
    count, total, word, fail_cnt  = self.download_thread.progress
    percent = count*100//total
    info = "Progress: {0}% - Downloading: [{1}/{2}] {3} \nFail: {4}".format(percent, count, total, word, fail_cnt)
    self.label_info.setText(info)
    self.lable_word.setText("- {0} -".format(word))

  def __update_text_edit(self, fail_words):
    content = ""
    for w in fail_words:
      content += (w + "\n")
    self.textedit.setText(content)
    #self.textedit.setPlainText(content)

  def __update_field_indexes(self):
    self.field_indexes = [self.comb_pho_uk.currentIndex(),
          self.comb_pho_us.currentIndex(),
          self.comb_sentence.currentIndex(),
          self.comb_mean.currentIndex(),
          self.comb_audio.currentIndex()]
