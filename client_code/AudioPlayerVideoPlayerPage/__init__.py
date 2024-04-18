from ._anvil_designer import AudioPlayerVideoPlayerPageTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
import base64
from anvil.js.window import navigator
# import anvil.http

class AudioPlayerVideoPlayerPage(AudioPlayerVideoPlayerPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._source = ''
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @property
  def source(self):
    return self._source

  @source.setter
  def source(self, audio):
    if audio:
      self._source = audio
      # browser = self.call_js('get_browser_name')
      # response = anvil.http.request("https://dubtube.anvil.app/#")
      # print(response.get_bytes())
      # self.dom_nodes['audioSource'].src = audio.get_url(False)
      # encoded_audio_data = base64.b64encode(anvil.media.open(audio).getvalue()).decode('utf-8')
      try:
        print(navigator.userAgent)
        if 'Firefox' in str(navigator.userAgent):
          # print('I am a firefox')
          self.dom_nodes['audioSource'].src = audio.url
          print(audio.url)
        else:
          # print('I am not a firefox')
          encoded_audio_data = base64.b64encode(audio.get_bytes()).decode('utf-8')
          self.dom_nodes['audioSource'].src = f'data:audio/wav;base64,{encoded_audio_data}'
      except:
        print('Something wrong')
        encoded_audio_data = base64.b64encode(audio.get_bytes()).decode('utf-8')
        self.dom_nodes['audioSource'].src = f'data:audio/wav;base64,{encoded_audio_data}'


  @property
  def audioid(self):
    return self._audioid

  @audioid.setter
  def audioid(self, value):
    self._audioid = value

  @property
  def currenttime(self):
    return self._currenttime

  @currenttime.setter
  def currenttime(self, value):
    self._currenttime = value
    self.dom_nodes['audio'].currentTime = value

  def vplay(self):
    if self.parent.tag == 'videoPlayer':
      videoPlayerForm = self.parent.parent.parent
      videoPlayerForm.raise_event('x-playVideo')

      if videoPlayerForm.playFirstTime:
        anvil.server.call('listen_dub', videoPlayerForm._audioid)
        listOfDubInfoBars = videoPlayerForm.repeating_panel.get_components()
        for DubInfoBar in listOfDubInfoBars:
          if DubInfoBar.item['audioID'] == videoPlayerForm._audioid:
            listensLabelText = DubInfoBar.label_listens.text
            DubInfoBar.label_listens.text = str(int(listensLabelText.split(' ')[0]) + 1) + " listens"
        videoPlayerForm.playFirstTime = False

  def vpause(self):
    if self.parent.tag == 'videoPlayer':
      self.parent.parent.parent.raise_event('x-pauseVideo')

  # def jumpToTime(self, timeInSeconds):
  #   self.call_js('jumpToTime', timeInSeconds)
  #   print("aaaaaaaaaaa")

  # def vtimeupdate(self):
  #   print(self._source)
