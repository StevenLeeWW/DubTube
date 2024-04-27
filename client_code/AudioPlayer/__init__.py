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
    # Any code you write here will run before the form opens.
    # Set Form properties and Data Bindings.
    self._source = ''
    self.init_components(**properties)

  
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
    """Method that is called from the Javascript when the audio player is played in the video page"""
    if self.parent.tag == 'videoPlayer':
      videoPlayerForm = self.parent.parent.parent
      videoPlayerForm.raise_event('x-playVideo')
      # If the 'playFirstTime' variable in the video page is true
      if videoPlayerForm.playFirstTime:
        # Increase the number of 'listens' of the dub and add the dub to the history table of the logged in user
        anvil.server.call('listen_dub', videoPlayerForm._audioid)
        listOfDubInfoBars = videoPlayerForm.repeating_panel.get_components()
        for DubInfoBar in listOfDubInfoBars:
          if DubInfoBar.item['audioID'] == videoPlayerForm._audioid:
            listensLabelText = DubInfoBar.label_listens.text
            # Increase the number of 'listens' of the dub and display it on the dub info bar
            DubInfoBar.label_listens.text = str(int(listensLabelText.split(' ')[0]) + 1) + " listens"
        videoPlayerForm.playFirstTime = False

  
  def vpause(self):
    """Method that is called from the Javascript when the audio player is paused in the video page"""
    if self.parent.tag == 'videoPlayer':
      self.parent.parent.parent.raise_event('x-pauseVideo')

