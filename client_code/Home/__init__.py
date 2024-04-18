from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
from anvil_extras import routing

@routing.route('')
class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_trendLanguage.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.refresh_dubs()
    self.refresh_ads()
    self.check_request_response_client()
    self.add_event_handler('x-refreshPage', self.refreshPage)
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False

  def refreshPage(self, **event_args):
    self.check_request_response_client()

  
  def refresh_dubs(self):
    """Load existing dubs from the Data Table, and display them in the RepeatingPanel"""
    dubRows = anvil.server.call('get_dubs')
    unblockedDubRows = [dub for dub in dubRows if dub['blocked'] == False]
    self.repeating_panel_trending.items = unblockedDubRows

  
  def refresh_ads(self):
    adsLinksAndPics = anvil.server.call('get_today_advertisement')
    linkAndPic = adsLinksAndPics[0]
    if linkAndPic['link'] is not None and linkAndPic['advertisementPicture'] is not None:
      self.link_ad1.url = linkAndPic['link']
      self.image_ad1.source = linkAndPic['advertisementPicture']
    linkAndPic = adsLinksAndPics[1]
    if linkAndPic['link'] is not None and linkAndPic['advertisementPicture'] is not None:
      self.link_ad2.url = linkAndPic['link']
      self.image_ad2.source = linkAndPic['advertisementPicture']
    linkAndPic = adsLinksAndPics[2]
    if linkAndPic['link'] is not None and linkAndPic['advertisementPicture'] is not None:
      self.link_ad3.url = linkAndPic['link']
      self.image_ad3.source = linkAndPic['advertisementPicture']
    
  
  def check_request_response_client(self):
    user = anvil.users.get_user()
    if user is not None:
      responded = anvil.server.call('check_request_response')
      if responded:
        self.link_your_dub_req.background = '#ff5f15'
      else:
        self.link_your_dub_req.background = 'default'
    else:
      self.link_your_dub_req.background = 'default'

  def check_request_response_client(self):
    responded = anvil.server.call('check_ads_accepted_approved')
    if responded:
      self.link_advertise.background = '#ff5f15'
    else:
      self.link_advertise.background = 'default'
  
  def drop_down_trendLanguage_change(self, **event_args):
    """This method is called when an item is selected"""
    selectedLanguage = self.drop_down_trendLanguage.selected_value
    dubRows = anvil.server.call('get_dubs', selectedLanguage)
    unblockedDubRows = [dub for dub in dubRows if dub['blocked'] == False]
    if len(unblockedDubRows) > 0:
      self.column_panel_noAvailableDubs.visible = False
      self.repeating_panel_trending.items = unblockedDubRows
    else:
      self.column_panel_noAvailableDubs.visible = True
      self.label_noAvailableDubs.text = 'Sorry. No available dubs for ' + selectedLanguage
      self.repeating_panel_trending.items = unblockedDubRows


  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()
  
  
  def link_liked2_click(self, **event_args):
    """This method is called when the link is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      homePage = get_open_form()
      homePage.link_liked_click()

  
  def link_trending2_click(self, **event_args):
    """This method is called when the link is clicked"""
    routing.set_url_hash('trending')
    # homePage = get_open_form()
    # homePage.link_trending2_click()

  
  def link_your_dub_req_click(self, **event_args):
    """This method is called when the link is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      homePage = get_open_form()
      homePage.link_your_dub_req_click()

  
  def link_public_request_click(self, **event_args):
    """This method is called when the link is clicked"""
    homePage = get_open_form()
    homePage.link_public_request_click()

  
  def link_content2_click(self, **event_args):
    """This method is called when the link is clicked"""
    homePage = get_open_form()
    homePage.link_content_click()

  def link_advertise_click(self, **event_args):
    """This method is called when the link is clicked"""
    homePage = get_open_form()
    homePage.link_advertise_click()
    

  
    