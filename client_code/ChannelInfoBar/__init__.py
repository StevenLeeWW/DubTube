from ._anvil_designer import ChannelInfoBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing
from ..Channel import Channel


class ChannelInfoBar(ChannelInfoBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    
  
  def link_channel_click(self, **event_args):
    """This method is called when the link to the channel is clicked"""
    channelOwner = self.item['userID']
    currentUser = anvil.users.get_user()
    get_open_form().reset_links()
    property = {'channelowner': channelOwner}
    routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)
    

  def link_channel2_click(self, **event_args):
    """This method is called when the link to the channel is clicked"""
    self.link_channel_click()
  
  
  def button_unsubscribe_click(self, **event_args):
    """This method is called when the 'unsubscribe' button is clicked"""
    success = anvil.server.call('subscribeUnsubscribe', self.item['userID'])
    if success:
      self.parent.parent.parent.refresh_subscription()
    else:
      Notification('Sorry. Something is wrong.', style='warning', timeout=3).show()
