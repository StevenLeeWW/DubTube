from ._anvil_designer import DubViewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..Homepage import Homepage
from ..VideoPlayer import VideoPlayer
from ..Channel import Channel
from ..Profile import Profile
from anvil_extras import routing

class DubView(DubViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.playFirstTime = True
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    
  
  def link_video_click(self, **event_args):
    """This method is called when the link is clicked"""
    videoUrl = self.item['videoUrl']['videoUrl']
    videoID = self.item['videoUrl']['youTubeVideoID']
    audio = self.item['audio']
    audioID = self.item['audioID']
    homepage = get_open_form()
    homepage.reset_links()
    # homepage.content_panel.clear()
    video_properties = {'videourl': videoUrl, 'audio': audio, 'audioid': audioID}
    # video_properties = {'videourl': videoUrl, 'audioid': audioID}
    # homepage.content_panel.add_component(VideoPlayer(**video_properties))
    routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID}, **video_properties)

  def button_play_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.button_play.text == 'Play in sync':
      self.youtube_video.play()
      self.audio_player.dom_nodes['audio'].play()
      # print(self.audio_player.audioid)
      # self.audio_player_play()
      self.button_play.text = 'Pause in sync'
      if self.playFirstTime:
        anvil.server.call('listen_dub', self.item['audioID'])
        listensLabelText = self.label_listens.text
        self.label_listens.text = str(int(listensLabelText.split(' ')[0]) + 1) + " listens"
        self.playFirstTime = False
    elif self.button_play.text == 'Pause in sync':
      self.youtube_video.pause()
      self.audio_player.dom_nodes['audio'].pause()
      self.button_play.text = 'Play in sync'

  def link_channel_click(self, **event_args):
    """This method is called when the link is clicked"""
    channelOwner = self.item['createdBy']
    currentUser = anvil.users.get_user()
    homepage = get_open_form()
    homepage.reset_links()
    # homepage.content_panel.clear()
    if currentUser is None:
      property = {'channelowner': channelOwner}
      # homepage.content_panel.add_component(Channel(**property))
      routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)
    else:
      if currentUser == channelOwner:
        # homepage.content_panel.add_component(Profile())
        routing.set_url_hash('profile')
      else:
        property = {'channelowner': channelOwner}
        # homepage.content_panel.add_component(Channel(**property))
        routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)

  
  def youtube_video_state_change(self, state, **event_args):
    """This method is called when the video changes state (eg PAUSED to PLAYING)"""
    if state == 'PAUSED':
      self.audio_player.dom_nodes['audio'].pause()
    elif state == 'PLAYING':
      self.audio_player.dom_nodes['audio'].play()

        

  
