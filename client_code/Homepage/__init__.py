from ._anvil_designer import HomepageTemplate
from ..DubEdit import DubEdit
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

from anvil_extras import routing
routing.logger.debug = False # Toggle this setting for logging print statements

from ..Home import Home
from ..History import History
from ..Liked import Liked
from ..SearchResults import SearchResults
from ..Trending import Trending
from ..Content import Content
from ..Requests import Requests
from ..PublicRequests import PublicRequests
from ..AccountOptions import AccountOptions
from ..AdminOptions import AdminOptions
from ..Profile import Profile
from ..Subscriptions import Subscriptions
from ..ProfileNameSetter import ProfileNameSetter
from ..Flag import Flag
from ..FlagAdmin import FlagAdmin
from ..BlockedDubs import BlockedDubs
from ..SearchResultsAdmin import SearchResultsAdmin
from ..Advertisements import Advertisements
from ..AdvertisementsAdmin import AdvertisementsAdmin
from ..Earn import Earn
from ..Channel import Channel
from ..CreateDub import CreateDub
from ..VideoPlayer import VideoPlayer
from ..ErrorForm import ErrorForm

# @routing.main_router
@routing.template(path="", priority=0, condition=None)
class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.showProfilePicture()
    self.link_home.role = 'selected'
    # self.content_panel.clear()
    # self.content_panel.add_component(Home())
    self.link_DubTube.width = 190
    self.button_search.width = 50
    

  def showProfilePicture(self):
    '''Show the profile picture when user logged in. If user is an admin, make the admin options link on the left menu visible.'''
    user = anvil.users.get_user()
    if user is not None:
      self.channel_picture.source = user['profilePicture']
      self.column_panel_profilePic.visible = True
      self.column_panel_signIn.visible = False
      if user['admin']:
        self.link_admin.visible = True
      else:
        self.link_admin.visible = False
      # check whether there are any unread received flags
      self.unread_flags_client()
      # check whether there are any dubs blocked by admin
      self.check_block_client()
      # check whether there are any new released dubs by the subscribed channels that are not yet listened
      self.new_released_not_listened_client()
    else:
      self.column_panel_profilePic.visible = False
      self.column_panel_signIn.visible = True


  def unread_flags_client(self):
    '''Check whether there are any unread received flags'''
    if anvil.server.call('unread_flags'):
      self.link_flagged.foreground = '#D22B2B'
    else:
      self.link_flagged.foreground = '#000000'


  def check_block_client(self):
    '''Check whether there are any dubs blocked by the admin'''
    if anvil.server.call('check_block'):
      self.link_content.foreground = '#D22B2B'
    else:
      self.link_content.foreground = '#000000'


  def new_released_not_listened_client(self):
    '''Check whether there are any new released dubs from the subscribed channel'''
    if anvil.server.call('new_released_not_listened'):
      self.link_subscribed.foreground = '#D22B2B'
    else:
      self.link_subscribed.foreground = '#000000'
      
  
  def button_signIn_click(self, **event_args):
    '''Help the user to login when the signin button is clicked'''
    user = anvil.users.get_user()
    if user is None:
      loggedIn = self.checkLogin()
      self.showProfilePicture()
      if loggedIn:
        Notification('Log in successful.', style='success', title='Success').show()
        self.content_panel.raise_event_on_children('x-refreshPage')

  
  def checkLogin(self):
    '''Check whether the user is logged in. Call the method to set the profile name if user is signing up. If user is an admin, then make the admin options visible'''
    currentUser = anvil.users.get_user()
    if currentUser is None:
      loginReturn = anvil.users.login_with_form(allow_cancel=True)
      if loginReturn is not None:
        self.showProfilePicture()
        if loginReturn['userID'] is None:
          self.setProfileName(loginReturn)
        return True
      else:
        return False
    else:
      # Global.user = currentUser
      # self.showProfilePicture()
      if currentUser['admin']:
        self.link_admin.visible = True
      else:
        self.link_admin.visible = False
      if currentUser['userID'] is None:
        self.setProfileName(currentUser)
      return True

  
  def setProfileName(self, currentUser):
    '''Prompt user to set a profile name is they just signed up. Prompt them to provide a profile name that is not taken already.'''
    profileName = alert(
      content=ProfileNameSetter(),
      buttons=[("Cancel", -1)],
    )
    if profileName != -1:
      message = anvil.server.call('add_user', currentUser['email'], currentUser['password_hash'], profileName)
      if message != "Duplicated profile name":
        Notification('Profile name has been set successfully.', style='success').show()
    else:
      profileName = None
      anvil.server.call('add_user', currentUser['email'], currentUser['password_hash'], profileName)

  
  def reset_links(self, **event_args):
    '''Reset the links to default role'''
    self.link_home.role = ''
    self.link_history.role = ''
    self.link_liked.role = ''
    self.link_content.role = ''
    self.link_create.role = ''
    self.link_flagged.role = ''
    self.link_subscribed.role = ''

  
  def link_home_click(self, **event_args):
    '''Clear the content panel and add the Home page when the home link is clicked.'''
    self.text_box_search.text = ''
    self.reset_links()
    self.link_home.role = 'selected'
    # self.content_panel.clear()
    # self.content_panel.add_component(Home())
    routing.set_url_hash('')

  
  def link_history_click(self, **event_args):
    '''Triggered when the history link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the History page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      self.link_history.role = 'selected'
      # self.content_panel.clear()
      # self.content_panel.add_component(History())
      routing.set_url_hash('history')

  
  def link_liked_click(self, **event_args):
    '''Triggered when the liked link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the Liked page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      self.link_liked.role = 'selected'
      # self.content_panel.clear()
      # self.content_panel.add_component(Liked())
      routing.set_url_hash('liked')

  
  def link_create_click(self, **event_args):
    '''Triggered when the create link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the History page.'''
    self.link_create.role = 'selected'
    loggedIn = self.checkLogin()
    currentUser = anvil.users.get_user()
    if currentUser is not None:
      new_dub = {}
      mode = {'mode': 'create'}
      save_clicked = alert(
        content=DubEdit(item=new_dub, **mode),
        large=True,
        buttons=[("Cancel", False)],
      )
      if save_clicked:
        dubRow = anvil.server.call('check_dub_existed2', new_dub)
        if dubRow != False:
          if dubRow is not None:
            if confirm('You have a dub for the video with the same language and accent. Do you want to replace it?'):
              anvil.server.call('delete_audio', dubRow)
            else:
              return None
          success = anvil.server.call('add_audio', new_dub)
          if success:
            # self.content_panel.clear()
            # self.content_panel.add_component(Content())
            routing.set_url_hash('content')
            Notification('New dub created successfully!', title='Success', style='success', timeout=3).show()
          else:
            Notification('Sorry. Fail to create new dub', title='Alert', style='warning', timeout=3).show()
        else:
          Notification('Something is wrong...', title='Warning', style='warning', timeout=3).show()
    self.link_create.role = ''

  
  def link_content_click(self, **event_args):
    '''Triggered when the content link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the Content page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      self.link_content.role = 'selected'
      # self.content_panel.clear()
      # self.content_panel.add_component(Content())
      routing.set_url_hash('content')

  # def link_liked2_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   loggedIn = self.checkLogin()

  def link_flagged_click(self, **event_args):
    '''Triggered when the flag link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the Flag page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      self.link_flagged.role = 'selected'
      # self.content_panel.clear()
      # self.content_panel.add_component(Flag())
      routing.set_url_hash('flag')
  

  def link_subscribed_click(self, **event_args):
    '''Triggered when the subscribed link is clicked. Check whether the user has logged in. If yes, clear the content panel and add the Subscriptions page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      self.link_subscribed.role = 'selected'
      # self.content_panel.clear()
      # self.content_panel.add_component(Subscriptions())
      routing.set_url_hash('subscription')

  
  def link_DubTube_click(self, **event_args):
    '''Clear the content panel and add the Home page when the DubTube logo link is clicked.'''
    self.link_home_click()

  
  def text_box_search_pressed_enter(self, **event_args):
    '''Triggered when enter is pressed after the search text box gets focus. Check whether the input to the text box is a video url or a search keyword. Get the search results accordingly and display them on the Search Results page.'''
    if self.text_box_search.text != '':
      videoid = anvil.server.call('get_video_id_from_url', self.text_box_search.text)
      if videoid is not None:
        videoUrl = self.text_box_search.text
        # self.content_panel.clear()
        url_dict = {'ytid': videoid, 'keyword': ''}
        video_properties = {'videourl': videoUrl, 'videotitlekeyword': ''}
        if anvil.users.get_user() is not None:
          if anvil.users.get_user()['admin']:
            # self.content_panel.add_component(SearchResultsAdmin(**video_properties))
            routing.set_url_hash(url_pattern='searchadmin', url_dict=url_dict, **video_properties)
          else:
            # self.content_panel.add_component(SearchResults(**video_properties))
            routing.set_url_hash(url_pattern='search', url_dict=url_dict, **video_properties)
        else:
          # self.content_panel.add_component(SearchResults(**video_properties))
          routing.set_url_hash(url_pattern='search', url_dict=url_dict, **video_properties)
      else:
        keyword = self.text_box_search.text
        # self.content_panel.clear()
        url_dict = {'ytid': '', 'keyword': keyword}
        video_properties = {'videourl': '', 'videotitlekeyword': self.text_box_search.text}
        if anvil.users.get_user() is not None:
          if anvil.users.get_user()['admin']:
            # self.content_panel.add_component(SearchResultsAdmin(**video_properties))
            routing.set_url_hash(url_pattern='searchadmin', url_dict=url_dict, **video_properties)
          else:
            # self.content_panel.add_component(SearchResults(**video_properties))
            routing.set_url_hash(url_pattern='search', url_dict=url_dict, **video_properties)
        else:
          # self.content_panel.add_component(SearchResults(**video_properties))
          routing.set_url_hash(url_pattern='search', url_dict=url_dict, **video_properties)

  
  def button_search_click(self, **event_args):
    '''Triggered when the search button is clicked.'''
    self.text_box_search_pressed_enter()

  
  def link_trending2_click(self):
    '''Clear the content panel and add the Trending page when the trending link on the homepage is clicked.'''
    self.text_box_search.text = ''
    self.reset_links()
    # self.content_panel.clear()
    # self.content_panel.add_component(Trending())
    routing.set_url_hash('trending')

  
  def link_your_dub_req_click(self):
    '''Triggered when the request link on the home page is clicked. Check whether the user has logged in. If yes, clear the content panel and add the Request page.'''
    loggedIn = self.checkLogin()
    if loggedIn:
      self.text_box_search.text = ''
      self.reset_links()
      # self.content_panel.clear()
      # self.content_panel.add_component(Requests())
      routing.set_url_hash('request')

  
  def link_public_request_click(self):
    '''Clear the content panel and add the Public request page when the public request link on the Home page is clicked.'''
    self.text_box_search.text = ''
    self.reset_links()
    # self.content_panel.clear()
    # self.content_panel.add_component(PublicRequests())
    routing.set_url_hash('publicrequest')

  
  def link_advertise_click(self):
    '''Triggered when the advertise link on the Home page is clicked. Check whether user has logged in. If logged in user is not an admin, clear the content panel and add the Advertisement page.'''
    self.text_box_search.text = ''
    self.reset_links()
    loggedIn = self.checkLogin()
    if loggedIn:
      if anvil.users.get_user()['admin']:
        Notification('Admin is not allowed to post advertisements.', style='warning', timeout=3, title='Warning').show()
      else:
        # self.content_panel.clear()
        # self.content_panel.add_component(Advertisements())
        routing.set_url_hash('advertisement')
        

  def reset_links_color(self, **event_args):
    '''Reset the links to default role'''
    # self.link_home.foreground = 'black'
    # self.link_history.foreground = 'black'
    # self.link_liked.foreground = 'black'
    self.link_content.foreground = 'black'
    # self.link_create.foreground = 'black'
    self.link_flagged.foreground = 'black'
    self.link_subscribed.foreground = 'black'

  
  def link_profilePicture_click(self, **event_args):
    '''Triggered when the profile picture on the top right is clicked. Show the profile option, the logout option, and the delete account option.'''
    option = alert(
      content=AccountOptions(),
      title='Options', 
      large=True,
      buttons=[('Cancel', -1)]
    )
    if option != -1:
      # Clear the content panel and add the 
      if option == 'profile':
        self.text_box_search.text = ''
        self.reset_links()
        # self.content_panel.clear()
        # self.content_panel.add_component(Profile())
        routing.set_url_hash('profile')
      elif option == 'logout':
        logOut = confirm("Do you want to log out?")
        if logOut:
          anvil.users.logout()
          # Global.user = None
          self.reset_links_color()
          routing.clear_cache()
          self.link_admin.visible = False
          self.showProfilePicture()
          Notification("You are logged out.", style='success', title='Success').show()
          self.link_home_click()
      elif option == 'delete':
        delete = confirm("Do you want to delete your account?")
        if delete:
          delete = confirm('All created dubs and all info related to your account will be deleted if you delete your account. Are you sure you want to delete your account?', title='Warning')
          if delete:
            currentUser = anvil.users.get_user()
            anvil.users.logout()
            loginReturn = anvil.users.login_with_form(allow_cancel=True, show_signup_option=False)
            if loginReturn is not None:
              if currentUser == loginReturn:
                success = anvil.server.call('delete_user', currentUser)
                if success:
                  Notification('Account deleted.', style='success', title='Account deletion', timeout=3).show()
                  self.showProfilePicture()
                  routing.clear_cache()
                  self.link_home_click()
              else:
                Notification('Entered info does not belong to currently signed in account. Current account is logged out.', style='warning', title='Warning', timeout=3).show()
            else:
              Notification('This account does not exist. Current account is logged out.', style='warning', title='Attention', timeout=3).show()
          

  # def button_1_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.server.call('button_1')

  def link_admin_click(self, **event_args):
    """This method is called when the link is clicked"""
    if anvil.users.get_user()['admin']:
      option = alert(
        content=AdminOptions(),
        title='Admin Options', 
        large=True,
        buttons=[('Cancel', -1)]
      )
      if option != -1:
        if option == 'addAdmin':
          newAdmin = anvil.users.signup_with_form(allow_cancel=True)
          if newAdmin is not None:
            anvil.server.call('add_user', newAdmin['email'], newAdmin['password_hash'], None)
            anvil.server.call('make_admin', newAdmin)
        elif option == 'allFlags':
          self.text_box_search.text = ''
          self.reset_links()
          # self.content_panel.clear()
          # self.content_panel.add_component(FlagAdmin())
          routing.set_url_hash('flagadmin')
        elif option == 'blockedDubs':
          self.text_box_search.text = ''
          self.reset_links()
          # self.content_panel.clear()
          # self.content_panel.add_component(BlockedDubs())
          routing.set_url_hash('blockeddub')
        elif option == 'adsAdmin':
          self.text_box_search.text = ''
          self.reset_links()
          # self.content_panel.clear()
          # self.content_panel.add_component(AdvertisementsAdmin())
          routing.set_url_hash('advertisementadmin')
        elif option == 'topTen':
          self.text_box_search.text = ''
          self.reset_links()
          # self.content_panel.clear()
          # self.content_panel.add_component(Earn())
          routing.set_url_hash('earnadmin')

