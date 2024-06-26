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

  
  def refresh_dubInfoBar(self, **event_args):
    """Get the info needed for the dub info bar"""
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
    """This method is called when the link of the dub info bar is clicked"""
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
    

  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()
    

  def button_like_click(self, **event_args):
    """This method is called when the 'like' button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      anvil.server.call('like_dub', self.item)
      self.refresh_data_bindings()
      self.checkUserPastPreference()

  
  def button_dislike_click(self, **event_args):
    """This method is called when the 'dislike' button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      anvil.server.call('dislike_dub', self.item)
      self.refresh_data_bindings()
      self.checkUserPastPreference()

  
  def checkUserPastPreference(self):
    """Check whether the dub is liked/disliked/flagged by the current user in the past"""
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
    """Check whether the current user has subscribed to the channel and modify the 'subscribe' button accordingly"""
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
    """This method is called when the 'subscribe' button is clicked"""
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
    """This method is called when the link to the channel is clicked"""
    channelOwner = self.item['createdBy']
    currentUser = anvil.users.get_user()
    if currentUser is None:
      property = {'channelowner': channelOwner}
      routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)
    else:
      if currentUser == channelOwner:
        routing.set_url_hash('profile')
      else:
        property = {'channelowner': channelOwner}
        routing.set_url_hash(url_pattern='channel', url_dict={'channel': channelOwner['profileName']}, **property)

  
  def button_flag_click(self, **event_args):
    """This method is called when the 'flag' button is clicked"""
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
    """This method is called when the 'donate' button is clicked"""
    pass

  
  def link_paypal_click(self, **event_args):
    """This method is called when the 'paypal' link is clicked"""
    if self.link_paypal.url == '':
      Notification('Channel does not accept donation.', timeout=3)

  
  def button_share_click(self, **event_args):
    """This method is called when the 'share' button is clicked"""
    videoID = self.item['videoUrl']['youTubeVideoID']
    audioID = self.item['audioID']
    url_dict = 'ytid=' + videoID + '&audioid=' + audioID
    url_hash = 'video?' + url_dict
    link = 'https://dubtube.anvil.app/#' + url_hash
    link_dict = {'link': link}
    anvil.alert(
      content=CopyShareLink(item=link_dict),
      large=True,
      buttons=[('OK', None)]
    )
    

  
    
