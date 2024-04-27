from ._anvil_designer import TempDubViewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..VideoPlayer import VideoPlayer
from ..Channel import Channel
from ..Profile import Profile
from anvil_extras import routing


class TempDubView(TempDubViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.


  def button_play_click(self, **event_args):
    """This method is called when the 'play in sync' button is clicked"""
    if self.button_play.text == 'Play in sync':
      self.youtube_video.play()
      self.audio_player.dom_nodes['audio'].play()
      self.button_play.text = 'Pause in sync'
    elif self.button_play.text == 'Pause in sync':
      self.youtube_video.pause()
      self.audio_player.dom_nodes['audio'].pause()
      self.button_play.text = 'Play in sync'

  
  def link_channel_click(self, **event_args):
    """This method is called when the link to the channel is clicked"""
    channelOwner = self.item['createdBy']
    currentUser = anvil.users.get_user()
    homepage = get_open_form()
    homepage.reset_links()
    if currentUser is None:
      property = {'channelowner': channelOwner}
      routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)
    else:
      if currentUser == channelOwner:
        routing.set_url_hash('profile')
      else:
        property = {'channelowner': channelOwner}
        routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)

  
  def button_download_dub_click(self, **event_args):
    """This method is called when the 'download' button is clicked"""
    Notification('Please wait...', timeout=5).show()
    unpublishedDub = self.item['dub']
    if unpublishedDub is not None:
      anvil.media.download(unpublishedDub)
    else:
      Notification('Something is wrong...', style='warning', title='Alert', timeout=3).show()
