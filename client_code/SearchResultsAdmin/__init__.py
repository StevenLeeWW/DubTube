from ._anvil_designer import SearchResultsAdminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..RequestEdit import RequestEdit
from anvil_extras import routing


@routing.route('searchadmin', url_keys=['ytid', 'keyword', routing.ANY])
class SearchResultsAdmin(SearchResultsAdminTemplate):
  def __init__(self, **properties):
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      # print(loggedIn)
      if loggedIn:
        if anvil.users.get_user()['admin']:
          pass
        else:
          routing.set_url_hash('')
          routing.clear_cache()
          return None
      else:
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    try:
      if properties['videourl'] == '' and properties['videotitlekeyword'] != '':
        pass
      elif properties['videourl'] != '' and properties['videotitlekeyword'] == '':
        pass
      else:
        properties = self.get_properties(properties)
        if properties is None:
          Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
          return None
    except Exception:
      properties = self.get_properties(properties)
      if properties is None:
        Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
        return None
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_searchLanguage.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_searchAccent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.refresh_dubs()

  
  @property
  def videourl(self):
    return self._videourl

  
  @videourl.setter
  def videourl(self, value):
    self._videourl = value

  
  @property
  def videotitlekeyword(self):
    return self._videotitlekeyword

  
  @videotitlekeyword.setter
  def videotitlekeyword(self, value):
    self._videotitlekeyword = value

  
  def get_properties(self, properties):
    """Get the properties from the url"""
    try:
      videoid = routing.get_url_dict()['ytid']
      if videoid != '':
        videourl = 'https://www.youtube.com/watch?v=' + videoid
        properties['videourl'] = videourl
        properties['videotitlekeyword'] = ''
      else:
        properties['videourl'] = ''
        keyword = routing.get_url_dict()['keyword']
        properties['videotitlekeyword'] = keyword
      return properties
    except Exception:
      routing.set_url_hash('')
      routing.clear_cache()
      return None

  
  def refresh_dubs(self):
    """Get existing dubs from the Data Table, and display them in the RepeatingPanel"""
    dubRowsAtLeastOneDub = anvil.server.call('get_search_dubs', self._videourl, self._videotitlekeyword)
    dubRows = dubRowsAtLeastOneDub[0]
    atLeastOneDub = dubRowsAtLeastOneDub[1]
    if atLeastOneDub:
      self.column_panel_noAvailableDubs.visible = False
      self.repeating_panel_searchResults.items = dubRows
    else:
      self.column_panel_noAvailableDubs.visible = True
      if self._videotitlekeyword == '':
        self.label_noAvailableDubs.text = 'Sorry. No available dubs yet for this video.'
      else:
        self.label_noAvailableDubs.text = 'Sorry. No matching videos are found in DubTube.'
      self.repeating_panel_searchResults.items = dubRows

  
  def drop_down_change(self):
    """Filter the search result based on the language and accent"""
    selectedLanguage = self.drop_down_searchLanguage.selected_value
    selectedAccent = self.drop_down_searchAccent.selected_value
    dubRowsAtLeastOneDub = anvil.server.call('get_search_dubs', self._videourl, self._videotitlekeyword, selectedLanguage, selectedAccent)
    dubRows = dubRowsAtLeastOneDub[0]
    atLeastOneDub = dubRowsAtLeastOneDub[1]
    if atLeastOneDub:
      if len(dubRows) > 0:
        self.column_panel_noAvailableDubs.visible = False
        self.repeating_panel_searchResults.items = dubRows
      else:
        self.column_panel_noAvailableDubs.visible = True
        self.label_noAvailableDubs.text = 'Sorry. No available dubs yet for ' + selectedLanguage + ' and ' + selectedAccent + ' accent.'
        self.repeating_panel_searchResults.items = dubRows
    else:
      self.column_panel_noAvailableDubs.visible = True
      if self._videotitlekeyword == '':
        self.label_noAvailableDubs.text = 'Sorry. No available dubs yet for this video.'
      else:
        self.label_noAvailableDubs.text = 'Sorry. No matching videos are found in DubTube.'
      self.repeating_panel_searchResults.items = dubRows

  
  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()


  def drop_down_searchLanguage_change(self, **event_args):
    """This method is called when an item in the language drop down list is selected"""
    self.drop_down_change()

  
  def drop_down_searchAccent_change(self, **event_args):
    """This method is called when an item in the accent drop down list is selected"""
    self.drop_down_change()

  
  def button_request_click(self, **event_args):
    """This method is called when the 'request' button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      new_request = {}
      request = alert(
        content=RequestEdit(item=new_request),
        large=True,
        buttons=[("Cancel", False)],
      )
      if request:
        message = anvil.server.call('add_request', new_request)
        if message == 'success':
          Notification('Request created successfully!', style='success').show()
        elif message == 'fail':
          Notification('Sorry. Request fail.', style='warning', timeout=3).show()
        elif message == 'exist':
          Notification('Requested in the past.', style='warning', timeout=3).show()

  
  def button_create_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().link_create_click()
