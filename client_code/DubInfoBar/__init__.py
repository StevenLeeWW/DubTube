from ._anvil_designer import DubInfoBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Channel import Channel
from ..Profile import Profile
from ..FlagEdit import FlagEdit
from ..FlagOptions import FlagOptions
from ..CopyShareLink import CopyShareLink
from anvil.js.window import navigator
from anvil_extras import routing

class DubInfoBar(DubInfoBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.init_components(**properties)
    self.refresh_dubInfoBar()
    # self.add_event_handler('x-refreshPage', self.refresh_dubInfoBar)
    # self.checkSelectedAudio()
    # Any code you write here will run before the form opens.

  
  def refresh_dubInfoBar(self, **event_args):
    paypal_link = anvil.server.call('get_paypal_link', self.item['createdBy'])
    if paypal_link is None:
      self.link_paypal.url = ''
      self.button_donate.enabled = False
    else:
      self.link_paypal.url = paypal_link
      self.button_donate.enabled = True
    self.checkUserPastPreference()
    self.checkSubscription()
  
  def link_playSelect_click(self, **event_args):
    """This method is called when the link is clicked"""
    videoPlayerForm = self.parent.parent.parent
    language = 'Any language'
    accent = 'Any accent'
    if videoPlayerForm.drop_down_language.selected_value != language:
      language = videoPlayerForm.drop_down_language.selected_value
    if videoPlayerForm.drop_down_accent.selected_value != accent:
      accent = videoPlayerForm.drop_down_accent.selected_value
    videoUrl = self.item['videoUrl']['videoUrl']
    videoID = self.item['videoUrl']['youTubeVideoID']
    audio = self.item['audio']
    audioID = self.item['audioID']
    video_properties = {'videourl': videoUrl, 'audio': audio, 'audioid': audioID}
    if language == 'Any language' and accent == 'Any accent':
      routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID}, **video_properties) 
    elif language != 'Any language' and accent == 'Any accent':
      routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID, 'language': language}, **video_properties)
    elif language == 'Any language' and accent != 'Any accent':
      routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID, 'accent': accent}, **video_properties)
    else:
      routing.set_url_hash(url_pattern='video', url_dict={'ytid': videoID, 'audioid': audioID, 'language': language, 'accent': accent}, **video_properties)
    
    # listOfDubInfoBars = self.parent.get_components()
    # for item in listOfDubInfoBars:
    #   item.column_panel_dubInfoBar.background = '#ffffff'
    #   item.column_panel_dubInfoBar.foreground = '#000000'
    #   item.link_playSelect.foreground = '#000000'
    #   item.label_channelName.foreground = '#000000'
    # self.column_panel_dubInfoBar.background = '#808080'
    # self.column_panel_dubInfoBar.foreground = '#ffffff'
    # self.link_playSelect.foreground = '#ffffff'
    # # self.link_channel.foreground = '#ffffff'
    # self.label_channelName.foreground = '#ffffff'
    # videoPlayerForm = self.parent.parent.parent
    # videoPlayerForm._audio = self.item['audio']
    # videoPlayerForm._audioid = self.item['audioID']
    # videoPlayerForm.playFirstTime = True
    # videoPlayerForm.raise_event('x-refreshAudio')

  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()
    

  def button_like_click(self, **event_args):
    """This method is called when the button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      anvil.server.call('like_dub', self.item)
      self.refresh_data_bindings()
      self.checkUserPastPreference()

  def button_dislike_click(self, **event_args):
    """This method is called when the button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      anvil.server.call('dislike_dub', self.item)
      self.refresh_data_bindings()
      self.checkUserPastPreference()
    
  def checkUserPastPreference(self):
    currentUser = anvil.users.get_user()
    if currentUser is not None:
      self.button_like.role = 'tonal-button'
      self.button_dislike.role = 'tonal-button'
      self.button_flag.role = 'tonal-button'
      likeDislikeFlag = anvil.server.call('userPastPreference', self.item)
      if likeDislikeFlag[0]:
        self.button_like.role = 'filled-button'
      if likeDislikeFlag[1]:
        self.button_dislike.role = 'filled-button'
      if likeDislikeFlag[2]:
        self.button_flag.role = 'filled-button'
    
  def checkSubscription(self):
    self.button_subscribe.enabled = True
    currentUser = anvil.users.get_user()
    if currentUser is not None:
      if currentUser == self.item['createdBy']:
        self.button_subscribe.enabled = False
      else:
        subscribed = anvil.server.call('checkSubscription', self.item['createdBy'])
        if subscribed:
          self.button_subscribe.text = 'Unsubscribe'
        else:
          self.button_subscribe.text = 'Subscribe'
    else:
        self.button_subscribe.text = 'Subscribe'

  
  def button_subscribe_click(self, **event_args):
    """This method is called when the button is clicked"""
    currentUser = anvil.users.get_user()
    listOfDubInfoBars = self.parent.get_components()
    if currentUser is None:
      loggedIn = get_open_form().checkLogin()
      if loggedIn:
        for dubInfoBar in listOfDubInfoBars:
          dubInfoBar.checkSubscription()
    else:
      success = anvil.server.call('subscribeUnsubscribe', self.item['createdBy'])
      if success:
        for dubInfoBar in listOfDubInfoBars:
          dubInfoBar.checkSubscription()
      else:
        Notification('Sorry. Something is wrong.', style='warning', timeout=3).show()

  def link_channel_click(self, **event_args):
    """This method is called when the link is clicked"""
    channelOwner = self.item['createdBy']
    currentUser = anvil.users.get_user()
    contentPanel = get_open_form().content_panel
    # contentPanel.clear()
    if currentUser is None:
      property = {'channelowner': channelOwner}
      # contentPanel.add_component(Channel(**property))
      routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)
    else:
      if currentUser == channelOwner:
        # contentPanel.add_component(Profile())
        routing.set_url_hash('profile')
      else:
        property = {'channelowner': channelOwner}
        # contentPanel.add_component(Channel(**property))
        routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)

  def button_flag_click(self, **event_args):
    """This method is called when the button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      likeDislikeFlag = anvil.server.call('userPastPreference', self.item)
      if likeDislikeFlag[2]:
        option = alert(
          content=FlagOptions(),
          title='Options for the flag',
          large=True,
          buttons=[('Cancel', -1)]
        )
        if option == 'update':
          flag = anvil.server.call('get_flag', self.item)
          properties = {'mode': 'update', 'flagreason': flag['flagReason'], 'flagdetails': flag['flagDetails']}
        elif option == 'delete':
          if confirm('Do you want to remove the flag you raised for this dub?'):
            if anvil.server.call('delete_flag', self.item):
              Notification('Flag is removed.', style='success').show()
              self.checkUserPastPreference()
            else:
              Notification('Something is wrong...', style='warning').show()
            return None
        else:
          return None
      else:
        properties = {'mode': 'create'}
      flag_dict = alert(
        content=FlagEdit(**properties),
        large=True,
        buttons=[('Cancel', -1)]
      )
      if flag_dict != -1:
        if anvil.server.call('flag_dub', self.item, flag_dict):
          if likeDislikeFlag[2]:
            Notification('Updated successfully', style='success').show()
          else:
            Notification('Flag raised successfully', style='success').show()
        else:
          Notification('Something is wrong...', style='warning').show()
        self.checkUserPastPreference()

  def button_donate_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def link_paypal_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_paypal.url == '':
      Notification('Channel does not accept donation.', timeout=3)

  def button_share_click(self, **event_args):
    """This method is called when the button is clicked"""
    videoID = self.item['videoUrl']['youTubeVideoID']
    audioID = self.item['audioID']
    url_dict = 'ytid=' + videoID + '&audioid=' + audioID
    url_hash = 'video?' + url_dict
    # link = 'https://dubtube.anvil.app/#video?ytid=AypRHjT7e4g&audioid=a16&language=Malay&accent=Machine'
    link = 'https://dubtube.anvil.app/#' + url_hash
    # linkTextBox = TextBox(text=link)
    link_dict = {'link': link}
    anvil.alert(
      content=CopyShareLink(item=link_dict),
      large=True,
      buttons=[('OK', None)]
    )
    

  
    
