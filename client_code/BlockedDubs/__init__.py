from ._anvil_designer import BlockedDubsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from anvil.js.window import navigator
from anvil_extras import routing

@routing.route('blockeddub')
class BlockedDubs(BlockedDubsTemplate):
  def __init__(self, **properties):
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      print(loggedIn)
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
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    self.today = datetime.now().date()
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.refresh_blocked_dubs()
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False

  
  def refresh_blocked_dubs(self):
    """Load existing histories from the Data Table, and display them in the RepeatingPanel"""
    blocked_dubs = anvil.server.call('get_blocked_dubs')
    self.refresh_blocked_dubs_helper(blocked_dubs)


  def refresh_blocked_dubs_helper(self, blocked_dubs):
    """Load existing histories from the Data Table, and display them in the RepeatingPanel"""
    if len(blocked_dubs) > 0:
      self.repeating_panel.items = blocked_dubs
      self.repeating_panel.visible = True
      self.column_panel_noBlockedDubs.visible = False
    else:
      self.repeating_panel.visible = False
      self.column_panel_noBlockedDubs.visible = True
  

  def drop_down_language_change(self, **event_args):
    """This method is called when an item is selected"""
    language = self.drop_down_language.selected_value
    accent = self.drop_down_accent.selected_value
    blocked_dubs = anvil.server.call('get_blocked_dubs', language, accent)
    self.refresh_blocked_dubs_helper(blocked_dubs)
    

  def drop_down_accent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_language_change()

  def searchBlockedDubs(self):
    if self.text_box_searchBlockedDub.text != '':
      if anvil.server.call('get_video_id_from_url', self.text_box_searchBlockedDub.text) is not None:
        videoUrl = self.text_box_searchBlockedDub.text
        keyword = ''
      else:
        videoUrl = ''
        keyword = self.text_box_searchBlockedDub.text
      dubRowsAtLeastOneDub = anvil.server.call('get_search_dubs', videoUrl, keyword)
      dubRows = dubRowsAtLeastOneDub[0]
      atLeastOneDub = dubRowsAtLeastOneDub[1]
      relatedDubs = []
      if atLeastOneDub:
        blocked_dubs = anvil.server.call('get_blocked_dubs')
        for dubRow in dubRows:
          if dubRow in blocked_dubs:
            relatedDubs.append(dubRow)
      self.repeating_panel.items = relatedDubs

  def text_box_searchBlockedDub_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.searchBlockedDubs()

  def button_searchBlockedDub_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.searchBlockedDubs()

  def button_showAll_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.drop_down_language.selected_value = 'Any language'
    self.drop_down_accent.selected_value = 'Any accent'
    self.text_box_searchBlockedDub.text = ''
    self.refresh_blocked_dubs()
