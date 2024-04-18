from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Channel import Channel

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_channel_click(self, **event_args):
    """This method is called when the link is clicked"""
    channelOwner = self.item['creator']
    homepage = get_open_form()
    homepage.reset_links()
    homepage.content_panel.clear()
    property = {'channelowner': channelOwner}
    homepage.content_panel.add_component(Channel(**property))
    
