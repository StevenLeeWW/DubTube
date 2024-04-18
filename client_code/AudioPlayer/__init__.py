from ._anvil_designer import AudioPlayerTemplate
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

class AudioPlayer(AudioPlayerTemplate):
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
      self.dom_nodes['audioSource'].src = audio.url
      

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

