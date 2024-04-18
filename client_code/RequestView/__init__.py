from ._anvil_designer import RequestViewTemplate
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
from anvil_extras import routing


class RequestView(RequestViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.listenedOn = ''
    self.playFirstTime = True
    self.init_components(**properties)
    if self.item['responded']:
      self.column_panel_1.background = '#c0e9ff'
    if self.item['checked'] or self.item['responded']:
      self.label_responded.visible = True
      self.button_watch.enabled = True
    else:
      self.label_responded.visible = False
      self.button_watch.enabled = False
    # Any code you write here will run before the form opens.


  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('delete_request', self.item)
    self.parent.parent.refresh_requests()

  def button_watch_click(self, **event_args):
    """This method is called when the button is clicked"""
    videoUrl = self.link_video.url
    language = self.item['requestLanguage']
    accent = self.item['requestAccent']
    audioRow = anvil.server.call('dub_for_request', videoUrl, language, accent)
    audio = audioRow['audio']
    audioID = audioRow['audioID']
    videoID = audioRow['videoUrl']['youTubeVideoID']
    homepage = get_open_form()
    homepage.reset_links()
    homepage.content_panel.clear()
    video_properties = {'videourl': videoUrl, 'audio': audio, 'audioid': audioID}
    routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID}, **video_properties)
