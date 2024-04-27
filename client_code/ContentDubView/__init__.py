from ._anvil_designer import ContentDubViewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..VideoPlayer import VideoPlayer
from ..DubEdit import DubEdit
from ..Options import Options
from ..Channel import Channel
from ..Profile import Profile
import anvil.media
from anvil_extras import routing


class ContentDubView(ContentDubViewTemplate):
  def __init__(self, **properties):
    # Any code you write here will run before the form opens.
    self.playFirstTime = True
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.item['blocked']:
      self.label_blocked.visible = True
      self.column_panel.background = '#FFC300'
    

  def link_video_click(self, **event_args):
    """This method is called when the link is clicked. Go to the video page of the dub."""
    videoUrl = self.item['videoUrl']['videoUrl']
    videoID = self.item['videoUrl']['youTubeVideoID']
    audio = self.item['audio']
    audioID = self.item['audioID']
    homepage = get_open_form()
    homepage.reset_links()
    video_properties = {'videourl': videoUrl, 'audio': audio, 'audioid': audioID}
    routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID}, **video_properties)


  def button_play_click(self, **event_args):
    """This method is called when the 'play' button is clicked"""
    if self.button_play.text == 'Play in sync':
      self.youtube_video.play()
      self.audio_player.dom_nodes['audio'].play()
      self.button_play.text = 'Pause in sync'
      if self.playFirstTime:
        # If the dub is played for the first time since the page is loaded, add the dub to the History page and increase the number of listens
        anvil.server.call('listen_dub', self.item['audioID'])
        listensLabelText = self.label_listens.text
        self.label_listens.text = str(int(listensLabelText.split(' ')[0]) + 1) + " listens"
      self.playFirstTime = False
    elif self.button_play.text == 'Pause in sync':
      self.youtube_video.pause()
      self.audio_player.dom_nodes['audio'].pause()
      self.button_play.text = 'Play in sync'

  
  def button_more_click(self, **event_args):
    """This method is called when the 'More' button (3 dots) is clicked"""
    option = alert(
      content=Options(),
      title='Options', 
      large=True,
      buttons=[('Cancel', -1)]
    )
    if option != -1:
      if option == 'edit':
        audioRowCopy = dict(self.item)
        mode = {'mode': 'update'}
        save_clicked = alert(
          content=DubEdit(item=audioRowCopy, **mode),
          large=True,
          buttons=[("Cancel", False)],
        )
        if save_clicked:
          updateSuccessful = anvil.server.call('update_audio', self.item, audioRowCopy)
          if updateSuccessful:
            Notification('Update successfully.', title='Alert', style='success').show()
            self.parent.parent.refresh_contents()
          else:
            Notification('Dub does not exist. Update fail.', title='Alert', style='warning', timeout=3).show()
      elif option == 'delete':
        if confirm('Are you sure you want to delete this dub?', title='Warning'):
          self.parent.raise_event('x-delete-dub', audioRow=self.item)
      elif option == 'download':
        Notification('Please wait...', timeout=5).show()
        anvil.media.download(self.item['audio'])

  
  def link_channel_click(self, **event_args):
    """This method is called when the channel link is clicked"""
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
        