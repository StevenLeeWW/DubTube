from ._anvil_designer import ChannelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AccountEdit import AccountEdit
from ..LinkEdit import LinkEdit
from ..ChannelContent import ChannelContent
from ..Profile import Profile
from anvil_extras import routing

@routing.route('channel', url_keys=['channel'])
class Channel(ChannelTemplate):
  def __init__(self, **properties):
    try:
      if properties['channelowner'] != '':
        pass
      else:
        properties = self.get_channel_owner_client(properties)
        if properties is None:
          Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
          return None
    except:
      properties = self.get_channel_owner_client(properties)
      if properties is None:
        Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
        return None
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.add_event_handler('x-refreshPage', self.refreshPage)
    self.refresh_channel()
    self.showContent()
    # Any code you write here will run before the form opens.


  @property
  def channelowner(self):
    return self._channelowner

  @channelowner.setter
  def channelowner(self, user):
    self._channelowner = user
  

  def showContent(self):
    channelowner = {'channelowner': self._channelowner}
    self.column_panel_content.add_component(ChannelContent(**channelowner))

  def refreshPage(self, **event_args):
    self.refresh_channel()
    self.showContent()
  
  def refresh_channel(self):
    user = self._channelowner
    if user['profilePicture'] is not None:
      self.channel_picture.source = user['profilePicture']
    else:
      self.channel_picture.source = '_/theme/userDefault.jpg'
    self.label_profileName.text = user['profileName']
    self.label_subscribers.text = str(user['subscribers']) + ' subscribers'
    self.label_dubs.text = str(user['dubs']) + ' dubs'
    if user['profileDescription'] is None:
      self.label_description.text = 'None'
    else:
      self.label_description.text = user['profileDescription']
    links = anvil.server.call('get_links', user)
    if len(links) == 0:
      self.column_panel_noLinks.visible = True
      self.repeating_panel.visible = False
    else:
      self.column_panel_noLinks.visible = False
      self.repeating_panel.items = links
      self.repeating_panel.visible = True
    self.checkSubscription()


  def get_channel_owner_client(self, properties):
    try:
      profileName = routing.get_url_dict()['channel']
      # print(profileName)
      channelOwner = anvil.server.call('get_channel_owner', profileName)
      if channelOwner is not None:
        properties['channelowner'] = channelOwner
        return properties
      else:
        # Notification('This channel does not exist.', title='Alert', style='warning', timeout=3).show()
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    except:
      routing.set_url_hash('')
      routing.clear_cache()
      return None
  
  def checkSubscription(self):
    currentUser = anvil.users.get_user()
    if currentUser is not None:
      subscribed = anvil.server.call('checkSubscription', self._channelowner)
      if subscribed:
        self.label_subscribeStatus.text = 'Subscribed'
        self.label_subscribeStatus.visible = True
        self.button_subscribe.text = 'Unsubscribe'
      else:
        self.label_subscribeStatus.visible = False
        self.button_subscribe.text = 'Subscribe'
    else:
        self.label_subscribeStatus.visible = False
        self.button_subscribe.text = 'Subscribe'
    
  
  def button_subscribe_click(self, **event_args):
    """This method is called when the button is clicked"""
    loggedIn = get_open_form().checkLogin()
    if loggedIn:
      currentUser = anvil.users.get_user()
      if currentUser == self._channelowner:
        content_panel = get_open_form().content_panel
        content_panel.clear()
        content_panel.add_component(Profile())
      else:
        self.checkSubscription()
        success = anvil.server.call('subscribeUnsubscribe', self._channelowner)
        if success:
          self.refresh_channel()
        else:
          Notification('Sorry. Something is wrong.', style='warning', timeout=3).show()

  
      


  
